import random
import pandas as pd
import streamlit as st

def csvToArray(csv):
    return [item.strip() for item in csv.split(",") if item.strip()]

def getData(items_csv, num_transactions, min_number_items, max_num_items):
    if not items_csv.strip():
        return []

    items = csvToArray(items_csv)
    transactions = []
    progress_bar = st.progress(0)
    for i in range(num_transactions):
        random_num_items = random.randint(min_number_items, max_num_items)
        transaction = set(random.sample(items, random_num_items))
        transactions.append(transaction)
        progress = (i + 1) / num_transactions
        progress_bar.progress(progress)
    progress_bar.empty()
    return transactions


def readFile(uploaded_file):
    if uploaded_file is not None:
        try:
            total_size = uploaded_file.size
            chunk_size = 100
            transactions = []
            progress_bar = st.progress(0)
            bytes_read = 0

            # Read the CSV without headers
            for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size, header="infer"):
                for _, row in chunk.iterrows():
                    if len(row) < 2:
                        continue  
                    products_string = row.iloc[1]
                    if pd.isnull(products_string):
                        continue
                    products = csvToArray(products_string)
                    transaction = set(products)
                    transactions.append(transaction)
                bytes_read += chunk.memory_usage(deep=True).sum()
                progress = min(bytes_read / total_size, 1.0)
                progress_bar.progress(progress)

            progress_bar.empty()
            return transactions
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return []
    return []
