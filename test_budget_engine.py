
import unittest

# importing the functions that we want to test from our main.
from budget_engine import (
    calculate_budget,
    compare_category_budgets,
    analyze_budget
)


class TestBudgetEngine(unittest.TestCase):

    # Test 1_>checking our normal budget calculations.
    def test_normal_budget(self):
        expenses = {
            "Groceries": 400,
            "Transport": 150,
            "Shopping": 350,
            "Entertainment": 150
        }

        total, remaining = calculate_budget(3000, expenses)

        self.assertEqual(total, 1050)
        self.assertEqual(remaining, 1950)

    # Test 2-> checking what happens when expenses exceed income.
    def test_expenses_exceed_income(self):
        expenses = {"Rent": 700, "Food": 400}

        total, remaining = calculate_budget(1000, expenses)

        self.assertEqual(total, 1100)
        self.assertEqual(remaining, -100)

    # Test 3-> checking if overspending is captured.
    def test_overspending(self):
        result = compare_category_budgets(
            {"Shopping": 350},
            {"Shopping": 250}
        )
        self.assertEqual(
            result["Shopping"]["status"],
            "Over budget"
        )    

    # Test 4->  checking if spending within budget is identified.
    def test_within_budget(self):
        result = compare_category_budgets(
            {"Groceries": 400},
            {"Groceries": 400}
        )

        self.assertEqual(
            result["Groceries"]["status"],
            "Within budget"
        )

        
    # Test 5 -> check if there is a situation with zero income and zero expenses.
    def test_zero_income(self):
        total, remaining = calculate_budget(0, {})

        self.assertEqual(total, 0)
        self.assertEqual(remaining, 0)

    # Test 6 -> check if there is a negative income found and if yes give an error.
    def test_negative_income(self):
        with self.assertRaises(ValueError):
            calculate_budget(-100, {})

    # Test 7-> checking if an achievable savings goal is recognized.
    def test_achievable_savings(self):
        result = analyze_budget(
            2000,
            {"Food": 300},
            {"Food": 400},
            500
        )
            
        self.assertTrue(
            any(
                "can be achieved" in message.lower()
                for message in result["recommendations"]
            )
        )

    # Test 8-> checking if an unachievable savings goal is recognized.
    def test_unachievable_savings(self):
        result = analyze_budget(
            1000,
            {"Food": 700},
            {"Food": 800},
            500
        )

        self.assertTrue(
            any(
                "not currently obtainable" in message.lower()
                for message in result["recommendations"]
            )
        )

    # Test 9-> all negative expenses should produce an error.
    def test_negative_expenses(self):
        with self.assertRaises(ValueError):
            calculate_budget(2000, {"Food": -100})

    # Test 10-> if there is negative planned category budgets it should be rejected.
    def test_negative_planned_budget(self):
        with self.assertRaises(ValueError):
            compare_category_budgets(
                {"Food": 100},
                {"Food": -50}
            )

    # Test 11-> all negative savings goals should show an error.
    def test_negative_savings_goal(self):
        with self.assertRaises(ValueError):
            analyze_budget(
                2000,
                {"Food": 300},
                {"Food": 400},
                -100
            )

    # Test 12-> if we find a missing expense category we should consider it as zero.
    def test_missing_expense_category(self):
        result = compare_category_budgets(
            {},
            {"Food": 400}
        )

        self.assertEqual(result["Food"]["spent"], 0)
        self.assertEqual(
            result["Food"]["status"],
            "Within budget"
        )


# Run all tests when this file is executed directly.
if __name__ == "__main__":
    unittest.main()
