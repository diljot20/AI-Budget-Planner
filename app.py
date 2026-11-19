import streamlit as st
import pandas as pd
from budget_engine import analyze_budget
from predict import categorize_transaction

st.set_page_config(
    page_title="AI Budget Planner",
    layout="wide"
)

st.title("AI Budget Planner")
st.write("Manage your monthly expenses and savings goals.")

st.header("Financial Information")

income = st.number_input(
    "Monthly Income ($)",
    min_value=0.0,
    value=3000.0
)

savings_goal = st.number_input(
    "Monthly Savings Goal ($)",
    min_value=0.0,
    value=500.0
)


st.header("AI Transaction Classification")

transaction_description = st.text_input(
    "Transaction Description",
    placeholder="e.g., Walmart, Netflix, Starbucks"
)

if st.button("Predict Category"):
    if transaction_description.strip():
        predicted_category = categorize_transaction(
            transaction_description
        )

        st.success(
            f"Predicted Category: {predicted_category}"
        )
    else:
        st.warning("Please enter a transaction description.")


st.header("Add Transactions")

st.write("Enter transaction descriptions and amounts.")

if "transactions" not in st.session_state:
    st.session_state.transactions = []

description = st.text_input(
    "Description",
    key="new_description"
)

amount = st.number_input(
    "Amount ($)",
    min_value=0.01,
    value=10.0,
    key="new_amount"
)

if st.button("Add Transaction"):

    if description.strip():
        category = categorize_transaction(description)

        st.session_state.transactions.append({
            "Description": description,
            "Amount": amount,
            "Category": category
        })

        st.success("Transaction added successfully.")
    else:
        st.warning("Please enter a description.")

if st.session_state.transactions:
    st.subheader("Transaction History")

    transaction_df = pd.DataFrame(
        st.session_state.transactions
    )

    st.dataframe(transaction_df, hide_index=True)

st.header("Monthly Expenses")


categories = [
    "Education",
    "Entertainment",
    "Fees",
    "Groceries",
    "Healthcare",
    "Income",
    "Insurance",
    "Mortgage",
    "Personal Care",
    "Rent",
    "Restaurants",
    "Shopping",
    "Subscription",
    "Transfer",
    "Transportation",
    "Travel",
    "Utilities"
]


expenses = {}
planned_budgets = {}

for category in categories:
    with st.expander(category):

     col1, col2 = st.columns(2)

     with col1:
        expenses[category] = st.number_input(
            "Actual Spending ($)",
            min_value=0.0,
            value=0.0,
            key=f"expense_{category}"
        )

     with col2:
        planned_budgets[category] = st.number_input(
            "Planned Budget ($)",
            min_value=0.0,
            value=0.0,
            key=f"budget_{category}"
        )


st.header("Budget Analysis Options")

analysis_method = st.radio(
    "Choose how to calculate your expenses:",
    [
        "AI Classified Transactions",
        "Manual Expenses"
    ]
)


if st.button("Analyze Budget"):

    if st.session_state.transactions:

        transaction_totals = {}

        for transaction in st.session_state.transactions:
            category = transaction["Category"]
            amount = transaction["Amount"]

            transaction_totals[category] = (
                transaction_totals.get(category, 0) + amount
            )

        expenses = transaction_totals

    
    active_budgets = {
        category: amount
        for category, amount in planned_budgets.items()
        if amount > 0
    }

    result = analyze_budget(
        income,
        expenses,
        active_budgets,
        savings_goal
    )



    st.header("Budget Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Income",
            f"${result['income']:,.2f}"
        )

    with col2:
        st.metric(
            "Total Expenses",
            f"${result['total_expenses']:,.2f}"
        )

    with col3:
        st.metric(
            "Remaining Balance",
            f"${result['remaining_balance']:,.2f}"
        )

    st.header("Category Budget Comparison")

    for category, details in result["category_results"].items():

        if details["status"] == "Over budget":
            st.warning(
                f"{category}: ${details['difference']:.2f} over budget"
            )
        else:
            st.success(
                f"{category}: Within budget"
            )

    
    
    st.header("Spending by Category")

    chart_data = {
        category: amount
        for category, amount in expenses.items()
        if amount > 0
    }

    if chart_data:
        st.bar_chart(chart_data)
    else:
        st.info("No expenses entered.")

    st.header("Planned vs Actual Spending")

    all_categories = sorted(
        set(expenses) | set(planned_budgets)
    )

    comparison_data = pd.DataFrame({
        "Category": all_categories,
        "Actual Spending": [
            expenses.get(category, 0)
            for category in all_categories
        ],
        "Planned Budget": [
            planned_budgets.get(category, 0)
            for category in all_categories
        ]
    })

    comparison_data = comparison_data.set_index("Category")

    st.bar_chart(comparison_data, stack=False)



    st.header("Budget Recommendations")

    for recommendation in result["recommendations"]:
        st.write(recommendation)