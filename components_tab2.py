from data import *
from utils import *
import streamlit as st

def render_tab_2():
    products_list = st.text_area("Enter products here (comma separated)", value="A, B, C, D, E", height=70)
    items = csvToArray(products_list)
    num_items = len(items)
    
    if num_items == 0:
        st.error("Please enter at least one product.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            num_transactions = st.number_input("Number of transactions", min_value=1, value=100, on_change=resetTransactions)
        with col2:
            value = min(1, num_items)
            min_number_items = st.number_input(
                "Min items per transaction",
                min_value=1,
                max_value=num_items,
                value=value,
                on_change=resetTransactions
            )
        with col3:
            value = min(5, num_items)
            max_number_items = st.number_input(
                "Max items per transaction",
                min_value=1,
                max_value=num_items,
                value=value,
                on_change=resetTransactions
            )
        if st.button("Generate Transactions", key="generate_transactions_button", use_container_width=True):
            resetTransactions()
            transactions = getData(products_list, num_transactions, min_number_items, max_number_items)
            if transactions:
                st.session_state["transactions"] = transactions
                st.success(f"Generated {len(transactions)} random transactions!")
            else:
                st.error("Failed to generate transactions.")