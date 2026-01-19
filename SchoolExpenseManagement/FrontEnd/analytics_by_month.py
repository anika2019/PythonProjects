import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"

def analytics_tab_month():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1), key="month_start_date")

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5), key="month_end_date")

    if st.button("Get Monthly Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/monthly/", json=payload)
        response = response.json()

        data = {
            "Month": list(response.keys()),
            "Total": [response[month]["total"] for month in response]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Month", ascending=True)

        st.title("Total Amount Spent By Month")

        # Bar chart showing total amount spent by month
        st.bar_chart(data=df_sorted.set_index("Month")['Total'], use_container_width=True)

        # Table with Month and Total columns
        df_table = df_sorted.copy()
        df_table["Total"] = df_table["Total"].map("{:.2f}".format)

        st.subheader("Monthly Breakdown")
        st.table(df_table)