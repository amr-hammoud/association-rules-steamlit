import streamlit as st
from utils import *

def render_rules_params(items):
  st.write("### Set Parameters for Association Rule Mining")
  col1, col2 = st.columns(2)
  with col1:
      st.number_input("Minimum Support", min_value=0.0, max_value=1.0, value=0.1, key="min_support", on_change=resetProceed)
  with col2:
      st.number_input("Minimum Confidence", min_value=0.0, max_value=1.0, value=0.1, key="min_confidence", on_change=resetProceed)