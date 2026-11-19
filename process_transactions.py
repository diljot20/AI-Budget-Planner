# actually runs AI predictions on a list of transactions

from predict import categorize_transaction
from budget_engine import analyze_budget


def process_transactions(transactions):

    categorized = {}

    for key, value in transactions.items():
        cat = categorize_transaction(key)
        if cat in categorized.keys():
            categorized[cat] += value

        else:
            categorized[cat] = value

    return categorized

# analyze_budget: (int, dict ("category" : int), dict ("category" : int), int)

# Test

'''
sample_transactions = {"Petro Canada":100,
          "Food Basics": 50,
          "Netflix":10,
          "Auberge du Pomier":200,
          "Uniqlo":40,
          "Starbucks": 10,
          "Ali Express": 21,
          "McDonalds": 5,
          "OLG": 20}
a = process_transactions(sample_transactions)
print(analyze_budget(5000, a, a, 500))

'''