# Week 9 – Dashboard with Database Query (Streamlit + SQLite)

## Objective

This week, you’ll connect your dashboard directly to the database created in Week 8 (`log.db`)  
and display the stored log data using **Streamlit**.

---

## Tasks

1. Connect Streamlit to the `log.db` database.
2. Load data from the `system_log` table into a DataFrame.
3. Display:
   - The latest 5 entries in a table.
   - Line charts for CPU, Memory, and Disk.
4. Add a filter to show only records with specific Ping_Status (e.g., “UP” or “DOWN”).
5. Close the database connection properly.

---

## Example Output

- Table of latest 5 log entries  
- Line chart for system usage  
- Dropdown filter for Ping Status  

---

## Run the Dashboard

```bash
streamlit run app.py
```
---

Make sure log.db is in the same folder as your Streamlit app.

## Submission Checklist

 []app.py connects to database and displays data

 []Charts render correctly

 []Screenshot of your dashboard

 []Files pushed to GitHub
