
# AI Budget Planner

An interactive budgeting application built with Python, Streamlit, and machine learning. The application helps users track expenses, categorize transactions, and analyze their monthly budget.

## Features

- Enter monthly income and savings goals
- Add transactions with descriptions
- Predict transaction categories using a trained machine learning model
- Manually enter and categorize expenses
- Analyze spending and identify budget overruns
- View budget information through an interactive Streamlit interface

## Technologies Used

- Python
- Streamlit
- Pandas
- Machine Learning (Logistic Regression)
- Joblib

## Project Structure

- `app.py` - Streamlit user interface
- `budget_engine.py` - Budget analysis logic
- `predict.py` - Transaction category prediction
- `process_transactions.py` - Transaction processing
- `logistic_regression.joblib` - Trained classification model
- `test_budget_engine.py` - Budget analysis tests
- `requirements.txt` - Python dependencies

## How to Run

1. Clone the repository.
2. Open the project folder in a terminal.
3. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   streamlit run app.py
   ```

## My Contribution

This was an academic group project. My primary responsibility was developing the Streamlit user interface and integrating the team's transaction classification and budget analysis modules.

I also performed manual testing to verify transaction entry, category prediction, and budget calculations.

## Project Purpose

The project demonstrates how machine learning can be integrated into a Python-based application to support personal financial planning.
