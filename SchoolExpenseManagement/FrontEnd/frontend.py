import streamlit as st
from ui_part import add_update_tab
from analytics import analytics_tab
from analytics_by_month import analytics_tab_month

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics By Category", "Analytics by Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()
    
with tab3:
    analytics_tab_month()

