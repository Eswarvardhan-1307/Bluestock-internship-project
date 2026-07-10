import pandas as pd

# Load processed scheme performance data
performance = pd.read_csv(
    r"C:\Users\eswar\OneDrive\Desktop\Project Folder\data\processed\07_scheme_performance.csv"
)

print("=" * 50)
print(" Mutual Fund Recommendation System")
print("=" * 50)

risk = input("\nEnter Risk Appetite (Low / Moderate / High): ").strip().title()

# Filter by risk grade
filtered = performance[
    performance["risk_grade"].str.title() == risk
]

# Check if any funds match
if filtered.empty:
    print("\nNo funds found for the selected risk level.")

else:
    recommendations = (
        filtered
        .sort_values(
            by="sharpe_ratio",
            ascending=False
        )
        .head(3)
    )

    print("\nTop 3 Recommended Funds\n")

    print(
        recommendations[
            [
                "scheme_name",
                "fund_house",
                "risk_grade",
                "sharpe_ratio",
                "return_3yr_pct",
                "expense_ratio_pct"
            ]
        ]
    )
