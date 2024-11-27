import streamlit as st
import extra_streamlit_components as stx
from components_tab1 import *
from components_tab2 import *

def render_tabs():
  if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

  chosen_tab = stx.tab_bar(data=[
      stx.TabBarItemData(id="tab1", title="Upload Transactions", description=""),
      stx.TabBarItemData(id="tab2", title="Generate Transactions", description=""),
  ], default="tab1")


  if "chosen_tab" not in st.session_state or chosen_tab != st.session_state["chosen_tab"]:
      resetTransactions()
      
  st.session_state["chosen_tab"] = chosen_tab

  if chosen_tab == "tab1":
      render_tab_1()

  elif chosen_tab == "tab2":
      render_tab_2()