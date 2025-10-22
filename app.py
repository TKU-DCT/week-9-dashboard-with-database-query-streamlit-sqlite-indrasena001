import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Data Center Dashboard", layout="wide")
st.title("🏗️ Data Center Monitoring Dashboard")

if not os.path.exists(DB_NAME):
    st.warning("Database not found. Please run your logger (Week 7) first.")
else:
    # TODO: Connect to SQLite

    # TODO: Read data from system_log table into a DataFrame
  
    # TODO: Show latest 5 entries

    # TODO: Add charts for CPU, Memory, Disk

    # Optional filter (Ping_Status)
    selected_status = st.selectbox("Filter by Ping Status", ["All", "UP", "DOWN"])
    if selected_status != "All":
        df = df[df["ping_status"] == selected_status]
    st.write(f"Showing {len(df)} records")

    st.dataframe(df, use_container_width=True)

    conn.close()
