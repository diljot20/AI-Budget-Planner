import joblib

model = joblib.load("logistic_regression.joblib")

def categorize_transaction(description):
    return model.predict([description])[0]