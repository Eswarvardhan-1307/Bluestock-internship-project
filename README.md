# 📊 Mutual Fund Performance Analytics & Risk Evaluation Platform

A complete data analytics pipeline for evaluating Indian mutual fund performance using risk-adjusted metrics, benchmark comparison, and investor behavior analysis.

## 🧭 Overview

Investors often rely only on historical returns while ignoring downside risk, volatility, benchmark performance, and portfolio concentration. This project builds an end-to-end analytics pipeline — from raw data to a composite fund scorecard — to evaluate mutual funds objectively across multiple dimensions.

## 🎯 Objectives

- Clean and validate raw financial datasets (NAV history, scheme master, SIP transactions, investor demographics)
- Build a structured SQLite data warehouse
- Compute performance & risk metrics (CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown)
- Analyze investor behavior (age, gender, geography, SIP continuity)
- Generate a composite fund scorecard and data-driven recommendations

## 🗂️ Datasets

| Dataset | Description |
|---|---|
| **Fund Master** | Scheme Name, Category, Expense Ratio, Risk Category, Fund Manager |
| **NAV History** | Daily NAV & AUM per scheme |
| **SIP Transactions** | Investor ID, Age Group, Gender, State, SIP Amount, Frequency, Folio Number |
| **Benchmark Indices** | NIFTY50 & NIFTY100 daily closing values |

## 🧹 Data Cleaning

- Duplicate removal (exact & near-duplicate NAV rows)
- Missing value handling (forward-fill within 3-day gaps)
- Date standardization to ISO 8601
- NAV sanity validation (±20% day-on-day threshold)
- Expense ratio range checks (0–2.5%)

## 🏗️ Database Design

Star-schema SQLite warehouse:

Dim_Fund ──┐
Dim_Date ──┼──> Fact_NAV
│
Dim_Investor ──> Fact_SIP <── Dim_Fund, Dim_Date 


## 📈 Metrics Computed

| Metric | Formula |
|---|---|
| Daily Return | `Rₜ = (NAVₜ − NAVₜ₋₁) / NAVₜ₋₁` |
| CAGR | `(NAV_end / NAV_start)^(1/n) − 1` |
| Sharpe Ratio | `(R_p − R_f) / σ_p` |
| Sortino Ratio | `(R_p − R_f) / σ_downside` |
| Alpha / Beta | `R_p − R_f = α + β(R_m − R_f) + ε` |
| Max Drawdown | `min[(NAVₜ − NAV_peak) / NAV_peak]` |
| Sector HHI | `Σ (wᵢ)²` |

## 🔑 Key Insights

- Funds with higher Sharpe ratios delivered better risk-adjusted returns
- Sortino ratios highlighted funds with lower downside risk
- Several small/midcap funds showed positive Alpha but higher drawdown
- Higher HHI values indicate more concentrated (riskier) portfolios
- Regular SIP investors show better continuity than irregular investors
- Folio/AUM grew from ₹13.26 Cr → ₹26.12 Cr over the study period
- Low inter-fund NAV correlation confirms genuine diversification benefit

## 🏆 Top Results

| Metric | Top Fund |
|---|---|
| Best Sharpe Ratio | Mirae Asset Large Cap Fund (~1.45) |
| Best Sortino Ratio | Mirae Asset Large Cap Fund (~2.39) |
| Best Alpha | SBI Small Cap Fund (~0.30) |
| Best Composite Score | ICICI Pru Midcap Fund (~79/100) |

## 🛠️ Tech Stack

- **Python** — Pandas, NumPy, SciPy, Matplotlib
- **SQLite** — data warehouse
- **Seaborn** — visualizations

## 🚀 Future Scope

- Real-time NAV updates via AMFI APIs
- ML models for return/volatility prediction
- Portfolio optimization techniques
- Interactive dashboards (Power BI / Tableau)
- Automated report generation

## 📚 References

- [AMFI India](https://www.amfiindia.com)
- [NSE India](https://www.nseindia.com)
- [RBI](https://www.rbi.org.in)
- Pandas, NumPy, SciPy, Matplotlib documentation
- [SQLite Docs](https://www.sqlite.org/docs.html)
