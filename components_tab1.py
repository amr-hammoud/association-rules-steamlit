import streamlit as st
from data import *

def render_tab_1():
  uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Column 1 should contain the transaction id and column 2 should contain the products comma-separated")
  if st.button("Load Transactions", key="read_file_button", use_container_width=True):
      if uploaded_file:
          transactions = readFile(uploaded_file)
          if transactions and len(transactions) > 0:
              st.session_state["transactions"] = transactions
              st.success(f"Loaded {len(transactions)} transactions!")
          else:
              st.warning("No transactions found in the uploaded file.")
      else:
          st.warning("Please upload a valid CSV file.")