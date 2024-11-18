import streamlit as st
import extra_streamlit_components as stx
from data import *

st.title("Association Rules")

chosen_tab = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Upload Transactions", description=""),
    stx.TabBarItemData(id="tab2", title="Generate Transactions", description="")], default="tab1")

placeholder = st.container()
  
if chosen_tab == "tab1":
  uploaded_file = placeholder.file_uploader("Upload a CSV file", type=["csv"],help="Each row should represent a transaction")

if chosen_tab == "tab2":
    products_list = placeholder.text_area("Enter products here (comma separated)", height=40)
    num_transactions = placeholder.number_input("Number of transactions", min_value=1, value=100000)
    max_number_items = placeholder.number_input("Maximum number of items per transaction", min_value=1, value=5)

st.divider()

clicked = st.button("Proceed")

transactions = []

if clicked:
  if chosen_tab == "tab1":
    transactions = readFile(uploaded_file)
  
  elif chosen_tab == "tab2":
    transactions = getData(products_list, num_transactions, max_number_items)

