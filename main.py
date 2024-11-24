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
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Column 1 should contain the transaction id and column 2 should contain the products comma-separated")
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
    products_list = st.text_area("Enter products here (comma separated)", value="A, B, C, D, E", height=70)
    items = csvToArray(products_list)
    num_items = len(items)
    
    if num_items == 0:
        st.error("Please enter at least one product.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            num_transactions = st.number_input("Number of transactions", min_value=1, value=100)
        with col2:
            value = min(1, num_items)
            min_number_items = st.number_input(
                "Min items per transaction",
                min_value=1,
                max_value=num_items,
                value=value
            )
        with col3:
            value = min(5, num_items)
            max_number_items = st.number_input(
                "Max items per transaction",
                min_value=1,
                max_value=num_items,
                value=value
            )
        if st.button("Generate Transactions", key="generate_transactions_button", use_container_width=True):
            transactions = getData(products_list, num_transactions, min_number_items, max_number_items)
            if transactions:
                st.session_state["transactions"] = transactions
                st.success(f"Generated {len(transactions)} transactions!")
                st.divider()
            else:
                st.error("Failed to generate transactions.")


# Display loaded transactions if any
if len(st.session_state["transactions"]) > 0:
    transactions = st.session_state["transactions"]
    items = set().union(*transactions)
    

    st.write("### Sample Transactions:")
    sample_transactions = transactions[:5]
    
    df_sample = pd.DataFrame({
        'id': [i+1 for i in range(len(sample_transactions))],
        'Items': [', '.join(sorted(list(trans))) for trans in sample_transactions]
    })

    st.table(df_sample) 
    
    st.write("### Set Parameters for Association Rule Mining")
    col1, col2 = st.columns(2)
    with col1:
        min_support = st.number_input("Minimum Support", min_value=0.0, max_value=1.0, value=0.1, key="min_support")
    with col2:
        min_confidence = st.number_input("Minimum Confidence", min_value=0.0, max_value=1.0, value=0.1, key="min_confidence")
        
    max_possible_k = len(items)
    value = min(5, max_possible_k)
    max_k = st.number_input("Maximum size of itemsets (k)", min_value=2, max_value= max_possible_k,value=value, key="max_k")


    if st.button("Proceed", key="proceed_button", use_container_width=True):
        st.divider()
        st.session_state["proceed_clicked"] = True
        
        frequent_itemsets = get_frequent_itemsets(items, transactions, min_support, max_k)

        if len(frequent_itemsets) == 0:
            st.warning("No frequent itemsets found with the given minimum support.")
            st.stop()
        
        st.session_state["frequent_itemsets"] = frequent_itemsets
        st.success(f"Found {len(frequent_itemsets)} Frequent Itemsets")
        
        st.info("Generating Association Rules...")
        rules = generate_rules(frequent_itemsets, transactions, min_confidence)
        st.session_state["rules"] = rules
        
    if st.session_state.get("proceed_clicked", False):  
            rules = st.session_state.get("rules", [])
            if rules:
                num_rules = len(rules)
                st.success(f"Generated {num_rules} Association Rules")
                options = generate_pagination_options(num_rules)
                num_to_show = st.selectbox("Select number of rules to show per page", options, key="num_to_show")
                
                # num_to_show = st.number_input("Number of rules to show", min_value=1, max_value= num_rules, value=value, key="num_to_show")
                
                if num_to_show:
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
                    data_to_show = rules_df if num_to_show == "All" else rules_df.head(num_to_show)
                    data_to_show.reset_index(drop=True, inplace=True)
                    data_to_show.index += 1
                    st.write(f"### Top {num_to_show} Rules sorted by confidence:")
                    st.table(data_to_show)
                else:
                    st.warning("No rules to show.")
            else:
                st.warning("No rules generated with the given minimum confidence.")
