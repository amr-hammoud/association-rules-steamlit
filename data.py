import random
import pandas as pd
import streamlit as st

def getData(items_csv, num_transactions, max_num_items):
    if not items_csv.strip():
        return []

    items = [item.strip() for item in items_csv.split(",") if item.strip()]
    transactions = []
    progress_bar = st.progress(0)
    for i in range(num_transactions):
        transaction = set(random.sample(items, random.randint(1, max_num_items)))
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

            for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
                for _, row in chunk.iterrows():
                    transaction = set(row.dropna().values[1:])
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
