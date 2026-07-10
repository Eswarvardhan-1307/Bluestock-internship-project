-- ==========================================================
-- BlueStock Mutual Fund Project
-- Day 2 Analytical SQL Queries
-- ==========================================================

--------------------------------------------------------------
-- Query 1 : Top 5 Funds by AUM
--------------------------------------------------------------

SELECT
    scheme_name,
    fund_house,
    aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;

--------------------------------------------------------------
-- Query 2 : Average NAV per Month
--------------------------------------------------------------

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav),2) AS average_nav
FROM nav_history
GROUP BY month
ORDER BY month;

--------------------------------------------------------------
-- Query 3 : Monthly SIP Inflow Trend
--------------------------------------------------------------

SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;

--------------------------------------------------------------
-- Query 4 : Transactions by State
--------------------------------------------------------------

SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM investor_transactions
GROUP BY state
ORDER BY total_amount DESC;

--------------------------------------------------------------
-- Query 5 : Funds with Expense Ratio < 1%
--------------------------------------------------------------

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

--------------------------------------------------------------
-- Query 6 : Top Fund Houses by Total AUM
--------------------------------------------------------------

SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM scheme_performance
GROUP BY fund_house
ORDER BY total_aum DESC;

--------------------------------------------------------------
-- Query 7 : Average Returns by Category
--------------------------------------------------------------

SELECT
    category,
    ROUND(AVG(return_1yr_pct),2) AS avg_1yr_return,
    ROUND(AVG(return_3yr_pct),2) AS avg_3yr_return,
    ROUND(AVG(return_5yr_pct),2) AS avg_5yr_return
FROM scheme_performance
GROUP BY category
ORDER BY avg_5yr_return DESC;

--------------------------------------------------------------
-- Query 8 : Top 10 Funds by Sharpe Ratio
--------------------------------------------------------------

SELECT
    scheme_name,
    sharpe_ratio,
    risk_grade
FROM scheme_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;

--------------------------------------------------------------
-- Query 9 : Portfolio Sector Allocation
--------------------------------------------------------------

SELECT
    sector,
    ROUND(SUM(weight_pct),2) AS total_weight
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_weight DESC;

--------------------------------------------------------------
-- Query 10 : Monthly Net Inflows by Category
--------------------------------------------------------------

SELECT
    month,
    category,
    net_inflow_crore
FROM category_inflows
ORDER BY month, category; 

