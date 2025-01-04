import streamlit as st

def resetTransactions():
    st.session_state["transactions"] = []
    if "frequent_itemsets_dict" in st.session_state:
        del st.session_state["frequent_itemsets_dict"]
    if "rules_dict" in st.session_state:
        del st.session_state["rules_dict"]
    if "support_cache" in st.session_state:
        del st.session_state["support_cache"]
    
def resetProceed():
    st.session_state["proceed_clicked"] = False

def calculate_or_get_support(itemset, transactions):
    itemset_frozen = frozenset(itemset)
    
    if "support_cache" not in st.session_state:
        st.session_state["support_cache"] = {}
        
    if itemset_frozen in st.session_state["support_cache"]:
        return st.session_state["support_cache"][itemset_frozen]
        
    count = sum(1 for transaction in transactions if itemset_frozen.issubset(transaction))
    support_value = count / len(transactions)
    
    st.session_state["support_cache"][itemset_frozen] = support_value

    return support_value

def generate_candidates(frequent_itemsets_keys, k):
    candidates = []
    length = len(frequent_itemsets_keys)

    for i in range(length):
        for j in range(i+1, length):
            # Convert each key to a sorted list for easy prefix comparison
            l1 = sorted(list(frequent_itemsets_keys[i]))
            l2 = sorted(list(frequent_itemsets_keys[j]))

            # If they share the same prefix up to k-2, merge them
            if l1[:k-2] == l2[:k-2]:
                candidate = frequent_itemsets_keys[i] | frequent_itemsets_keys[j]
                if len(candidate) == k:
                    candidates.append(candidate)
    return candidates


def get_frequent_itemsets(items, transactions):
    min_support = st.session_state["min_support"]
    progress_bar = st.progress(0)

    # clear the support_cache for each new run
    st.session_state["support_cache"] = {}

    itemsets_1 = [frozenset([item]) for item in items]
    freq_dict = {}

    # For each candidate of size 1, compute support
    for itemset in itemsets_1:
        support = calculate_or_get_support(itemset, transactions)
        if support >= min_support:
            freq_dict[itemset] = support

    k = 2
    current_freq_keys = list(freq_dict.keys())

    # Keep generating larger itemsets until no more can be found
    while True:
        progress_bar.progress(
            min(k / (len(items) if len(items) else 1), 1.0)
        )

        candidates = generate_candidates(current_freq_keys, k)

        if not candidates:
            break

        new_freq_dict = {}
        for candidate in candidates:
            support = calculate_or_get_support(candidate, transactions)
            if support >= min_support:
                new_freq_dict[frozenset(candidate)] = support

        if len(new_freq_dict) == 0:
            break

        # Merge new_freq_dict into freq_dict
        freq_dict.update(new_freq_dict)

        # Prepare for next iteration
        current_freq_keys = list(new_freq_dict.keys())
        k += 1

    progress_bar.empty()

    if len(freq_dict) == 0:
        st.warning("No frequent itemsets found with the given minimum support.")
        st.stop()

    st.session_state["frequent_itemsets_dict"] = freq_dict
    st.success(f"Found {len(freq_dict)} Frequent Itemsets")
    return freq_dict


def generate_rules(transactions):
    freq_dict = st.session_state["frequent_itemsets_dict"]
    min_confidence = st.session_state["min_confidence"]
    progress_bar = st.progress(0)

    rules_dict = {}

    for itemset_frozen in freq_dict:
        _ = calculate_or_get_support(itemset_frozen, transactions)

    itemsets_with_len_gt1 = [fs for fs in freq_dict.keys() if len(fs) > 1]
    total_itemsets = len(itemsets_with_len_gt1)
    processed_itemsets = 0
    rule_index = 1

    from itertools import combinations

    for itemset in itemsets_with_len_gt1:
        support_itemset = freq_dict[itemset]

        n = len(itemset)
        items_list = list(itemset)

        for r in range(1, n):  
            for subset in combinations(items_list, r):
                antecedent = frozenset(subset)
                consequent = itemset - antecedent

                support_antecedent = calculate_or_get_support(antecedent, transactions)
                confidence = support_itemset / support_antecedent if support_antecedent else 0

                if confidence >= min_confidence:
                    support_consequent = calculate_or_get_support(consequent, transactions)
                    lift = confidence / support_consequent if support_consequent else 0
                    conviction = None
                    if confidence < 1:
                        conviction = (1 - support_consequent) / (1 - confidence) if (1 - confidence) != 0 else None

                    rules_dict[rule_index] = {
                        "antecedent": antecedent,
                        "consequent": consequent,
                        "confidence": confidence,
                        "lift": lift,
                        "conviction": conviction,
                    }
                    rule_index += 1

        processed_itemsets += 1
        progress_bar.progress(processed_itemsets / total_itemsets)

    progress_bar.empty()
    st.session_state["rules_dict"] = rules_dict

    return rules_dict


def generate_pagination_options(num_rules):
    options = [5, 10, 20, 50, 100, num_rules]
    return [option for option in options if option < num_rules] + ["All"]
    
    