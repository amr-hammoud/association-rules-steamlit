import streamlit as st
import pandas as pd

def render_transaction_table(transactions):
  st.write("### Sample Transactions:")
  sample_transactions = transactions[:5]
  df_sample = pd.DataFrame({
      'id': [i+1 for i in range(len(sample_transactions))],
      'Items': [', '.join(sorted(list(trans))) for trans in sample_transactions]
  })
  st.table(df_sample) 