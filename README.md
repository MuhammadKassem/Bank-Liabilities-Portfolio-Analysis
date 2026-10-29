# Bank Liabilities Portfolio Analysis

A Data Analytics & Business Intelligence Case Study

## Overview
This independent case study analyzes a synthetic deposit portfolio across 24 monthly snapshots from January 2024 through December 2025. It uses Python and SQL/SQLite for data preparation and analysis, and Power BI for management reporting.

> **Data notice:** The dataset is synthetic and does not represent actual customer, account, or financial data from Bank Misr or any other bank. This project is not affiliated with or endorsed by a specific financial institution.

## Dataset at a glance
- Customers: 50,000
- Accounts: 90,228
- Products: 6
- Monthly balance records: 2,165,472
- Snapshot period: January 2024–December 2025

## Headline results
- December 2024 portfolio balance: EGP 3.935bn
- December 2025 portfolio balance: EGP 5.662bn
- Year-on-year growth: 43.89%
- Top 10 customer concentration at December 2025: approximately 0.27%
- Product balance growth, December 2024 to December 2025:
  - Interest Current Account: +74.20%
  - Basic Current Account: +71.79%
  - 24-Month Fixed Deposit: +23.14%
  - 12-Month Fixed Deposit: +21.94%
  - Flexi Savings: +4.35%

These figures are taken from the project's current analysis and should be revalidated if the source data or measure definitions change.

## Business questions addressed
1. Is the deposit portfolio growing or declining, and at what rate?
2. Which products hold the largest share of the portfolio?
3. Do deposits cover withdrawals?
4. Which products contribute most to recorded interest expense?
5. Is growth associated with customer growth or higher balances?
6. Is the portfolio concentrated among a small number of customers?
7. Which account and product types contribute most?
8. Which products combine stronger balance growth with relatively lower interest cost?
9. How stable is the portfolio and how does the product mix change over time?
10. What actions could management consider based on the evidence?

## Tools
- Python (data preparation and exploratory analysis)
- SQL / SQLite (structured storage and querying)
- Power BI (data model, measures, and dashboard)
- Excel/CSV as supporting data formats where applicable

## Suggested review before sharing
- Confirm all DAX measures and filter interactions.
- Confirm that growth comparisons use like-for-like month-end dates.
- Confirm the interest-cost definition, time period, and denominator.
- Check labels, units, number formats, and dashboard readability.
- Include the synthetic-data notice in the dashboard or accompanying report.
- Do not present the results as actual performance of any bank.

## Suggested project structure
```text
Bank_Liabilities_Portfolio_Analysis/
├── data/
│   └── liability_analysis.db
├── scripts/
│   └── analysis.py
├── powerbi/
│   └── Bank_Liabilities_Portfolio_Analysis.pbix
├── reports/
│   └── Executive_Summary_and_Recommendations.docx
└── README.md
```
The structure above is a suggested organization. File names and locations should be adjusted to match the actual files in your working directory.
