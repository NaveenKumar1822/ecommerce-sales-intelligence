# E-commerce Sales Intelligence: Performance, Profitability & Business Insights

> **Portfolio project** | Python · Pandas · Matplotlib · Seaborn · Power BI · DAX · Git

---

## Project Overview

A complete, reproducible end-to-end sales analytics solution for a US home-goods
e-commerce business, covering 24 months of transactions (January 2024 – December 2025).
The project delivers a Jupyter Notebook analytical workflow and a production-ready
Power BI dashboard package, demonstrating the full data analyst toolchain from raw CSV
to recruiter-ready interactive dashboard.

---

## Business Problem

E-commerce management needs to understand:
- Are sales growing and where are the peaks/troughs?
- Which products and categories drive revenue and profit?
- Are high-sales products necessarily the most profitable?
- Which customers are most valuable and which are at risk of churning?
- Where are the geographic opportunities?
- Are discounts helping or hurting profitability?

---

## Dataset

**Source:** User-provided e-commerce transaction data  
**Period:** 2024-01-01 to 2025-12-31  
**Tables:**

| File | Rows | Description |
|---|---|---|
| `orders.csv` | 9,245 | One row per order — date, status, payment method, shipping fee |
| `order_items.csv` | 15,608 | One row per product line — quantity, unit price, discount |
| `products.csv` | 90 | Product catalogue — name, category, list price, unit cost |
| `customers.csv` | 3,600 | Customer register — state, sign-up date, acquisition channel |

**No external or synthetic data used.**

---

## Analytical Objectives

1. Measure overall revenue and profitability
2. Identify monthly and seasonal sales patterns
3. Rank categories and products by revenue and profit
4. Segment customers using RFM methodology
5. Map geographic revenue concentration
6. Quantify the discount-margin trade-off
7. Identify at-risk customers and retention opportunities

---

## Technology Stack

| Layer | Tool |
|---|---|
| Data Processing | Python 3.12, Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Notebook | Jupyter Notebook |
| BI Dashboard | Power BI Desktop |
| DAX Modelling | DAX (Power BI) |
| Data Transforms | Power Query M |
| Version Control | Git, GitHub |

---

## Key Metrics & Definitions

| Metric | Definition |
|---|---|
| Net Revenue | `unit_price × quantity − discount_amount` (completed orders only) |
| Profit | `net_revenue − (unit_cost × quantity)` |
| Profit Margin % | `profit / net_revenue × 100` |
| Average Order Value | `total net revenue / distinct completed order IDs` |
| Return Rate % | `returned order IDs / all order IDs` |
| Repeat Customer Rate % | `customers with >1 completed order / total customers with ≥1 order` |
| RFM Scores | Quintile-based (1–5) on Recency, Frequency, Monetary independently |

---

## Business Findings

| # | Finding | Metric |
|---|---|---|
| 1 | Strong profitability across all categories | $1.89M revenue, 49.2% margin |
| 2 | Discounts cost 9.4 pp of margin | Non-disc: 50.4%; Disc: 40.8% |
| 3 | 64.4% repeat customer rate | 1,318 of 2,047 customers returned |
| 4 | Storage has the highest margin but least revenue | 55.6% margin, only 7.4% revenue share |
| 5 | CA, NY, TX drive 29.3% of revenue | Geographic concentration risk |
| 6 | Organic Search = most efficient channel | $777K revenue (41% of total) |
| 7 | 405 At Risk customers may churn | High historical value, low recency |
| 8 | Cotton Patio Chair is the #1 SKU | $67K revenue, 44.8% margin |

---

## Power BI Data Model

Star schema with FactSales at the centre:

```
           DimDate
              │ 1:*
              │
DimCustomer ──┼── FactSales ──── DimProduct
(1:*)         │
              │ 1:1
         CustomerRFM
```

**Relationships:** All single-direction (dimension → fact), preventing ambiguous filter paths.

---

## Dashboard Pages

| Page | Purpose |
|---|---|
| 1. Executive Overview | 6 KPI cards, monthly trend, category bars, region donut |
| 2. Sales Trends | MoM change, quarterly comparison, seasonality, weekday heatmap |
| 3. Product & Category | Revenue vs profit bars, margin chart, top/bottom products, discount table |
| 4. Customer & Geographic | Top customers, RFM donut, state map, channel bars, repeat vs one-time |
| 5. Business Insights | Return analysis, insights table, priority action cards |

---

## Important DAX Measures

```dax
Total Revenue =
    CALCULATE(SUMX(FactSales, FactSales[NetRevenue]), FactSales[IsCompleted] = TRUE())

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0)

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Previous Year Revenue], [Previous Year Revenue], BLANK())

Repeat Customer Rate % =
    DIVIDE([Repeat Customers], [Total Customers], 0)
```

See `outputs/power_bi/DAX_Measures.dax` for the full library of 30+ measures.

---

## Project Structure

```
ecommerce-sales-intelligence/
├── notebooks/
│   └── ecommerce_sales_analysis.ipynb   ← Main analytical notebook
├── data/
│   ├── raw/                             ← Original CSV files (unmodified)
│   └── processed/                       ← Cleaned data & charts
├── outputs/
│   └── power_bi/
│       ├── FactSales.csv                ← Main fact table (15,668 rows)
│       ├── DimDate.csv                  ← Date dimension (731 rows)
│       ├── DimCustomer.csv              ← Customer dimension (3,600 rows)
│       ├── DimProduct.csv               ← Product dimension (90 rows)
│       ├── CustomerRFM.csv              ← RFM segments (2,047 customers)
│       ├── DataQualityReport.csv        ← Cleaning audit trail
│       ├── BusinessInsights.csv         ← Evidence-based recommendations
│       ├── DAX_Measures.dax             ← 30+ production DAX measures
│       ├── DAX_Measures_Guide.md        ← How to create & validate measures
│       ├── PowerBI_Model_Guide.md       ← Step-by-step model setup
│       ├── PowerBI_Dashboard_Specification.md ← Visual-by-visual spec
│       └── theme.json                   ← Power BI theme file
├── src/
│   ├── data_cleaning.py                 ← Cleaning pipeline functions
│   ├── feature_engineering.py           ← Metric computation functions
│   └── validation.py                    ← Data quality assertions
├── tests/
│   └── test_sales_analysis.py           ← 16 unit tests (all passing)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Notebook Setup & Execution

```bash
# 1. Clone or download the repository
git clone https://github.com/YOUR_USERNAME/ecommerce-sales-intelligence.git
cd ecommerce-sales-intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place raw CSVs in data/raw/
#    (orders.csv, order_items.csv, products.csv, customers.csv)

# 4. Run the notebook
jupyter notebook notebooks/ecommerce_sales_analysis.ipynb
# or: jupyter nbconvert --to notebook --execute notebooks/ecommerce_sales_analysis.ipynb

# 5. Run tests
python -m pytest tests/ -v
```

---

## Power BI Import Instructions

**Detailed steps in:** `outputs/power_bi/PowerBI_Model_Guide.md`

Quick steps:
1. Open Power BI Desktop
2. **Home → Get Data → Text/CSV** → import all 5 CSV files from `outputs/power_bi/`
3. Set data types per the model guide
4. Create relationships (FactSales → DimDate, DimCustomer, DimProduct)
5. Mark DimDate as the date table
6. Create the `_Measures` table and import `DAX_Measures.dax`
7. Apply `theme.json` via **View → Themes → Browse for themes**
8. Build 5 pages per `PowerBI_Dashboard_Specification.md`
9. Save as `Ecommerce_Sales_Intelligence.pbix`

---

## Limitations & Future Improvements

- **No sales targets provided** — add a monthly target CSV for variance analysis
- **No ship dates** — shipping duration and on-time delivery analysis unavailable
- **Gross margin only** — operating expenses and marketing costs not included
- **US only** — no international market data
- **First-touch attribution** — acquisition channel reflects signup, not last-touch

**Suggested next steps:**
- Connect to live database for real-time refresh
- Add A/B test data for discount code experiments
- Build customer cohort retention curves
- Add Google Analytics data for full-funnel analysis

---

## License

This project uses a user-provided dataset. Do not publish the raw data files publicly.
