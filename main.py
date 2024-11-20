import streamlit as st
import extra_streamlit_components as stx
import pandas as pd
from data import *
from utils import *

st.title("Association Rules")

if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

chosen_tab = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Upload Transactions", description=""),
    stx.TabBarItemData(id="tab2", title="Generate Transactions", description=""),
], default="tab1")

# Tab 1: Upload Transactions
if chosen_tab == "tab1":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Each row should represent a transaction")
    if st.button("Read File", key="read_file_button"):
        if uploaded_file:
            transactions = readFile(uploaded_file)
            if transactions and len(transactions) > 0:
                st.session_state["transactions"] = transactions
                st.success(f"Loaded {len(transactions)} transactions!")
            else:
                st.warning("No transactions found in the uploaded file.")
        else:
            st.warning("Please upload a valid CSV file.")

# Tab 2: Generate Transactions
elif chosen_tab == "tab2":
    products_list = st.text_area("Enter products here (comma separated)", height=40)
    num_transactions = st.number_input("Number of transactions", min_value=1, value=100)
    max_number_items = st.number_input("Maximum number of items per transaction", min_value=1, value=5)
    if st.button("Generate Transactions", key="generate_transactions_button"):
        transactions = getData(products_list, num_transactions, max_number_items)
        if transactions:
            st.session_state["transactions"] = transactions
            st.success(f"Generated {len(transactions)} transactions!")
        else:
            st.error("Failed to generate transactions.")

st.divider()

# Display loaded transactions if any
if len(st.session_state["transactions"]) > 0:
    transactions = st.session_state["transactions"]

    st.write("### Sample Transactions:")
    sample_transactions = transactions[:5]
    
    df_sample = pd.DataFrame({
        'id': [i+1 for i in range(len(sample_transactions))],
        'Items': [', '.join(sorted(list(trans))) for trans in sample_transactions]
    })

    st.table(df_sample) 
    
    st.write("### Set Parameters for Association Rule Mining")
    min_support = st.number_input("Minimum Support (as a percentage)", min_value=0.0, max_value=100.0, value=10.0)
    min_confidence = st.number_input("Minimum Confidence (as a percentage)", min_value=0.0, max_value=100.0, value=10.0)
    max_k = st.number_input("Maximum size of itemsets (k)", min_value=2, value=5)


    if st.button("Proceed", key="proceed_button"):
        progress_bar = st.progress(0)
        min_support /= 100
        min_confidence /= 100

        # Generate Frequent 1-itemsets
        items = set().union(*transactions)
        itemsets = [{item} for item in items]
        frequent_itemsets = []
        itemset_support = {}
        
        # Generate frequent itemsets of increasing size
        k = 1
        current_frequent_itemsets = itemsets
        while current_frequent_itemsets and k <= max_k:
            progress = k / max_k
            progress_bar.progress(progress)
            itemset_support.update({
                frozenset(itemset): calculate_support(itemset, transactions)
                for itemset in current_frequent_itemsets
            })
            current_frequent_itemsets = [
                itemset for itemset in current_frequent_itemsets
                if itemset_support[frozenset(itemset)] >= min_support
            ]
            frequent_itemsets.extend(current_frequent_itemsets)
            k += 1
            current_frequent_itemsets = generate_candidates(current_frequent_itemsets, k)
            
        progress_bar.empty()

        st.session_state["frequent_itemsets"] = frequent_itemsets
        st.write(f"### Found {len(frequent_itemsets)} Frequent Itemsets")
        
        st.write("### Generating Association Rules")
        rules = generate_rules(frequent_itemsets, transactions, min_confidence)
        st.session_state["rules"] = rules
        
        if rules:
            rules_df = pd.DataFrame([
                {
                    'Antecedent': ', '.join(sorted(list(rule[0]))),
                    'Consequent': str(rule[1]),
                    'Confidence': round(rule[2], 2),
                    'Lift': round(rule[3], 2),
                    'Conviction': round(rule[4], 2) if rule[4] is not None else 'Infinity'
                }
                for rule in rules
            ])

            rules_df.sort_values(by='Confidence', ascending=False, inplace=True)
            st.write(f"### Top 10 Rules sorted by confidence:")
            st.table(rules_df.head(10))
        else:
            st.warning("No rules generated with the given minimum confidence.")
