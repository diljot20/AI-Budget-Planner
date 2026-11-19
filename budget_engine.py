def calculate_budget(monthly_income, expenses):
    """Calculate total expenses and the moneyeft from the monthly income."""
#Assuming that monthly income and expenses are not negative we can raise an error if it's negative .
    if monthly_income < 0:
        raise ValueError("Income cannot be negative")

    if any(amount < 0 for amount in expenses.values()):
        raise ValueError("Expenses cannot be negative")
# adding all the monthly expenses first and then deduct it from income to get the reaining balance
    total_expenses = sum(expenses.values())
    remaining_balance = monthly_income - total_expenses

    return total_expenses, remaining_balance


def compare_category_budgets(expenses, planned_budgets):
    """Compare user's actual spending with their planned budget categories."""

    results = {}
# Checking to make sure that none of the actual expenses or planned budgets are negative.
    if any(amount < 0 for amount in expenses.values()):
            raise ValueError("Expenses cannot be negative.")
    
    if any(budget < 0 for budget in planned_budgets.values()):
            raise ValueError("Budget cannot be negative.")
    
    # checking each category against its planned budget.
    for category, budget in planned_budgets.items():
        # If no spending was recorded we can treat the amount as zero.
            
        spent = expenses.get(category, 0)

        if spent > budget:
            results[category] = {
                "spent": spent,
                "budget": budget,
                "status": "Over budget",
                "difference": spent - budget
            }
        else:
            results[category] = {
                "spent": spent,
                "budget": budget,
                "status": "Within budget",
                "difference": budget - spent
            }

    return results


def generate_recommendations(
    remaining_balance,
    category_results,
    savings_goal
):
    """Generate recommendations based on rule based decisions."""

    recommendations = []
    # since want to have saving goals let's make sure that savings goals are valid.
    if savings_goal < 0:
        raise ValueError("Savings goal cannot be negative.")

    # Rule 1-> Check user's overall spending
    if remaining_balance < 0:
        recommendations.append(
            "Your expenses exceed your income. "
            "Consider reducing your splurges."
        )
    elif remaining_balance == 0:
        recommendations.append(
            "Your entire income has been spent. "
            "Try to reduce expenses to build your savings."
        )
    else:
        recommendations.append(
            f"You have ${remaining_balance:.2f} remaining."
        )

    # Rule 2-> find out which categories the user is currently overspending
    for category, details in category_results.items():

        if details["status"] == "Over budget":
            recommendations.append(
                f"You are ${details['difference']:.2f} over "
                f"your {category} budget. Consider reducing your spending."
            )

    # Rule 3-> checking if user's savings goal can be achieved

    if remaining_balance >= savings_goal:
        recommendations.append(
            f"Your savings goal of ${savings_goal:.2f} can be achieved!"
        )
    # otherwise calculate how much more money is needed for the goal.
    else:
        short = savings_goal - max(remaining_balance, 0)

        recommendations.append(
            f"Your savings goal is not currently obtainable. "
            f"You need another ${short:.2f}."
        )

    return recommendations


def analyze_budget(income, expenses, planned_budgets, savings_goal):
     # to analyze the budget we need to calculate the total expenses and the remaining balance.

    total, remaining = calculate_budget(income, expenses)

    #compareing our user's actual spending with planned category budgets.

    category_results = compare_category_budgets(
        expenses, planned_budgets
    )
# now we can give recommendations based on our results.
    recommendations = generate_recommendations(
        remaining, category_results, savings_goal
    )
 # returning all results.
    return {
        "income": income,
        "total_expenses": total,
        "remaining_balance": remaining,
        "category_results": category_results,
        "recommendations": recommendations
    }


# below are some of our example tests to check how our budget engine works.
if __name__ == "__main__":

    monthly_income = 3000

    expenses = {
        "Groceries": 400,
        "Transport": 150,
        "Shopping": 350,
        "Entertainment": 150
    }

    planned_budgets = {
        "Groceries": 400,
        "Transport": 200,
        "Shopping": 150,
        "Entertainment": 100
    }

    savings_goal = 500

    result = analyze_budget(
        monthly_income,
        expenses,
        planned_budgets,
        savings_goal
    )

    print("\n AI BUDGET PLANNER")

    print("Monthly Income: $", result["income"])
    print("Total Expenses: $", result["total_expenses"])
    print("Remaining Balance: $", result["remaining_balance"])

    print("\n CATEGORY ANALYSIS ")

    for category, details in result["category_results"].items():
        print(
            category,
            "-",
            details["status"],
            "- Difference: $",
            details["difference"]
        )

    print("\n WHAT WE RECOMEND ")

    for recommendation in result["recommendations"]:
        print( recommendation)
