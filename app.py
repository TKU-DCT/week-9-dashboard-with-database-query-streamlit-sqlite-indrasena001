import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Data Center Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top, rgba(14,165,233,0.25), transparent 45%),
                        radial-gradient(circle at 20% 20%, rgba(99,102,241,0.3), transparent 40%),
                        linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
            color: #e2e8f0;
        }
        .metric-card {
            padding: 1rem 1.5rem;
            border-radius: 1rem;
            border: 1px solid rgba(226, 232, 240, 0.2);
            box-shadow: 0 25px 55px rgba(15, 23, 42, 0.45);
            transition: transform 200ms ease, box-shadow 200ms ease;
        }
        .metric-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 35px 65px rgba(15, 23, 42, 0.55);
        }
        .metric-card h4 {
            color: rgba(226, 232, 240, 0.8);
        }
        .metric-card small {
            color: rgba(226, 232, 240, 0.65);
        }
        .metric-card.cpu {
            background: linear-gradient(135deg, rgba(248, 113, 113, 0.25), rgba(248, 113, 113, 0.05));
            border-color: rgba(248, 113, 113, 0.45);
        }
        .metric-card.memory {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.25), rgba(34, 197, 94, 0.05));
            border-color: rgba(34, 197, 94, 0.45);
        }
        .metric-card.disk {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(59, 130, 246, 0.05));
            border-color: rgba(59, 130, 246, 0.45);
        }
        .chart-card {
            padding: 1rem 1.5rem;
            border-radius: 1rem;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.2);
            backdrop-filter: blur(10px);
        }
        .latest-table {
            background: rgba(15, 23, 42, 0.8);
            padding: 1rem;
            border-radius: 1rem;
        }
        .gradient-heading {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            background: linear-gradient(90deg, #38bdf8, #a855f7, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .accent-subhead {
            font-size: 1.3rem;
            font-weight: 600;
            color: #7dd3fc;
            letter-spacing: 0.02em;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        .accent-subhead::after {
            content: "";
            display: block;
            width: 60px;
            height: 3px;
            margin-top: 0.35rem;
            border-radius: 999px;
            background: linear-gradient(90deg, #38bdf8, rgba(56,189,248,0));
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="gradient-heading">🏗️ Data Center Monitoring Dashboard</h1>',
    unsafe_allow_html=True,
)

if not os.path.exists(DB_NAME):
    st.warning("Database not found. Please run your logger (Week 7) first.")
else:
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM system_log ORDER BY datetime(timestamp)",
            conn
        )

        if df.empty:
            st.info("No records found in `system_log` yet.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            latest_five = df.sort_values("timestamp", ascending=False).head(5)
            st.markdown('<div class="accent-subhead">Latest 5 Entries</div>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="latest-table">', unsafe_allow_html=True)
                st.dataframe(latest_five, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

            status_options = ["All"] + sorted(df["ping_status"].dropna().unique().tolist())
            selected_status = st.selectbox("Filter by Ping Status", status_options)
            filtered_df = df if selected_status == "All" else df[df["ping_status"] == selected_status]

            st.write(f"Showing {len(filtered_df)} records")
            st.dataframe(
                filtered_df.sort_values("timestamp", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            if filtered_df.empty:
                st.warning("No records match this filter.")
            else:
                latest_row = filtered_df.sort_values("timestamp").iloc[-1]
                metric_cols = st.columns(3)
                metrics = [
                    ("CPU Usage (%)", f"{latest_row['cpu']:.1f}%", "cpu"),
                    ("Memory Usage (%)", f"{latest_row['memory']:.1f}%", "memory"),
                    ("Disk Usage (%)", f"{latest_row['disk']:.1f}%", "disk"),
                ]
                for col, (label, value, css_class) in zip(metric_cols, metrics):
                    with col:
                        st.markdown(
                            f"""
                            <div class="metric-card {css_class}">
                                <h4 style="margin-bottom:0.4rem;">{label}</h4>
                                <h2 style="margin:0;">{value}</h2>
                                <small>Live metric from latest record</small>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.markdown('<div class="accent-subhead">System Utilization Trends</div>', unsafe_allow_html=True)
                chart_cols = st.columns(3)
                metric_mapping = [
                    ("CPU Usage (%)", "cpu"),
                    ("Memory Usage (%)", "memory"),
                    ("Disk Usage (%)", "disk"),
                ]
                for (title, column), col in zip(metric_mapping, chart_cols):
                    with col:
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        st.caption(f"{title} (last {len(filtered_df)} records)")
                        st.line_chart(filtered_df.set_index("timestamp")[column])
                        st.markdown("</div>", unsafe_allow_html=True)
    finally:
        conn.close()
