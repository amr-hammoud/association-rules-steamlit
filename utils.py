def calculate_support(itemset, transactions):
    itemset = set(itemset)
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

def generate_candidates(frequent_itemsets, k):
    candidates = []
    frequent_itemsets_list = list(frequent_itemsets)
    length = len(frequent_itemsets_list)
    for i in range(length):
        for j in range(i+1, length):
            l1 = list(frequent_itemsets_list[i])
            l2 = list(frequent_itemsets_list[j])
            l1.sort()
            l2.sort()
            if l1[:k-2] == l2[:k-2]:
                candidate = frequent_itemsets_list[i] | frequent_itemsets_list[j]
                if len(candidate) == k:
                    candidates.append(candidate)
    return candidates

from itertools import combinations

def generate_rules(frequent_itemsets, transactions, min_confidence, progress_bar=None):
    rules = []
    support_cache = {}

    for itemset in frequent_itemsets:
        support_cache[frozenset(itemset)] = calculate_support(itemset, transactions)

    single_items = set()
    for itemset in frequent_itemsets:
        if len(itemset) == 1:
            single_items.update(itemset)
    for item in single_items:
        support_cache[frozenset([item])] = calculate_support({item}, transactions)

    itemsets_with_len_gt1 = [itemset for itemset in frequent_itemsets if len(itemset) > 1]
    total_itemsets = len(itemsets_with_len_gt1)
    processed_itemsets = 0

    # Main loop to generate rules
    for itemset in itemsets_with_len_gt1:
        support_itemset = support_cache[frozenset(itemset)]
        for consequent in itemset:
            antecedent = itemset - {consequent}
            antecedent_frozen = frozenset(antecedent)

            if antecedent_frozen in support_cache:
                support_antecedent = support_cache[antecedent_frozen]
            else:
                support_antecedent = calculate_support(antecedent, transactions)
                support_cache[antecedent_frozen] = support_antecedent

            confidence = support_itemset / support_antecedent

            if confidence >= min_confidence:
                consequent_frozen = frozenset([consequent])
                support_consequent = support_cache[consequent_frozen]
                lift = confidence / support_consequent
                conviction = (1 - support_consequent) / (1 - confidence) if confidence < 1 else None
                rules.append((antecedent, consequent, confidence, lift, conviction))
        processed_itemsets += 1
        if progress_bar:
            progress_bar.progress(processed_itemsets / total_itemsets)
    return rules

