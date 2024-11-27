import streamlit as st
from section_transactions_loader import *
from components_transactions_table import *
from components_rules_params import *
from components_rules_table import *

st.title("Association Rules")
render_tabs()

if len(st.session_state["transactions"]) > 0:
    transactions = st.session_state["transactions"]
    items = set().union(*transactions)

    render_transaction_table(transactions)
    
    st.divider()
    
    render_rules_params(items)
    
    if st.button("Proceed", key="proceed_button", use_container_width=True):
        st.session_state["proceed_clicked"] = True
        
        frequent_itemsets = get_frequent_itemsets(items, transactions)
        
        rules = generate_rules(frequent_itemsets, transactions)
        
    if st.session_state.get("proceed_clicked", False):  
        render_rules_table()
