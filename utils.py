
def generate_candidates(frequent_itemsets, k):
    """
    Generate candidates for the next level of itemsets
    """
    return [set(x).union(set(y)) for x in frequent_itemsets for y in frequent_itemsets if len(set(x).union(set(y))) == k]


def calculate_support(itemset, transactions):
    """
    Calculate support for an itemset by counting the transactions in which the itemset is present
    """
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)