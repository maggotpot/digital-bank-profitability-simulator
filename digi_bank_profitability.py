import pandas as pd

def digital_bank_profitability(
        # Parameters
        customers = 1000000,
        avg_deposit = 2000,
        loan_to_deposit_ratio = 0.7,
        loan_interest_rate = 0.06,
        deposit_interest_rate = 0.02,
        default_rate = 0.03,
        recovery_rate = 0.4,
        operating_cost_per_customer = 120,
        interchange_per_customer = 40,
        subscription_per_customer = 60
):
    # Calculate total deposits & total loans
    total_deposits = customers * avg_deposit
    total_loans = total_deposits * loan_to_deposit_ratio

    # Calculate interest income & interest expense
    interest_income = total_loans * loan_interest_rate
    interest_expense = total_deposits * deposit_interest_rate

    # Calculate expected loss from defaults
    expected_loss = total_loans * default_rate * (1 - recovery_rate)

    # Calculate other revenues
    interchange_revenue = customers * interchange_per_customer
    subscription_revenue = customers * subscription_per_customer

    # Calculate operating costs
    operating_cost = customers * operating_cost_per_customer

    # Calculate net profit
    net_profit = (
        interest_income
        - interest_expense
        - expected_loss
        - operating_cost
        + interchange_revenue
        + subscription_revenue
    )

    return {
        "Total Deposits": total_deposits,
        "Total Loans": total_loans,
        "Interest Income": interest_income,
        "Interest Expense": interest_expense,
        "Expected Credit Loss": expected_loss,
        "Interchange Revenue": interchange_revenue,
        "Subscription Revenue": subscription_revenue,
        "Operating Costs": operating_cost,
        "Net Profit": net_profit
    }

results = digital_bank_profitability()
print(pd.Series(results))


# What happens if defaults increase?

import numpy as np

default_scenarios = np.linspace(0.01, 0.08, 10)

profits = []

for scenario in default_scenarios:
    results = digital_bank_profitability(default_rate=scenario)
    profits.append(results["Net Profit"])

scenario_df = pd.DataFrame({
    "Default Rate": default_scenarios,
    "Net Profit": profits
})

print(scenario_df)


# Adjusted for Customer Growth, Marketing and CAC

def simulate_growth(
        months = 24,
        initial_customers = 1000000,
        monthly_growth_rate = 0.02,
        marketing_spend = 500000,
        CAC = 200
):
    customer_counts = initial_customers
    final_outcomes = []

    for month in range(1, months + 1):
        organic_new_customers = customer_counts * monthly_growth_rate
        paid_new_customers = marketing_spend / CAC

        customer_counts += organic_new_customers + paid_new_customers

        profit_data = digital_bank_profitability(customers=int(customer_counts))

        final_outcomes.append({
            "Month": month,
            "Customers": int(customer_counts),
            "Net Profit": profit_data["Net Profit"]
        })
    
    return pd.DataFrame(final_outcomes)

growth_df = simulate_growth()
print(growth_df)

# Plot growth

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(growth_df["Month"], growth_df["Net Profit"])
plt.xlabel("Month")
plt.ylabel("Net Profit")
plt.title("Net Profit Growth Over Time")
plt.show()