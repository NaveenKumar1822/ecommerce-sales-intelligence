# E-Commerce Sales Intelligence

> An end-to-end Power BI analytics project — star schema data model, 30+ DAX measures, RFM customer segmentation, and a five-page interactive dashboard built on two years of e-commerce sales data.

![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=flat&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-Measures-0078D4?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Table of Contents

- [Dashboard Preview](#dashboard-preview)
- [Business Problem](#business-problem)
- [Dataset Overview](#dataset-overview)
- [Tools & Technologies](#tools--technologies)
- [Data Model](#data-model)
- [Dashboard Pages](#dashboard-pages)
- [Key Findings](#key-findings)
- [DAX Measures](#dax-measures)
- [How to Open the Dashboard](#how-to-open-the-dashboard)
- [Repository Structure](#repository-structure)
- [Data & Licensing](#data--licensing)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)

---

## Dashboard Preview

| Page | Screenshot |
|------|-----------|
| Executive Overview | ![Executive Overview](powerbi/screenshots/01-executive-overview.png) |
| Sales & Product Performance | ![Sales & Product Performance](powerbi/screenshots/02-sales-product-performance.png) |
| Customer Insights & RFM | ![Customer Insights](powerbi/screenshots/03-customer-rfm-segmentation.png) |
| Geographic & Channel Performance | ![Geographic & Channel](powerbi/screenshots/04-geographic-channel-performance.png) |
| Business Insights & Recommendations | ![Business Insights](powerbi/screenshots/05-business-insights-recommendations.png) |

---

## Business Problem

A home-goods e-commerce retailer operating across eight product categories and all US regions needed a single analytics platform to answer:

- **Revenue health** — Is the business growing month-over-month and year-over-year?
- **Product profitability** — Which categories and SKUs maximise margin?
- **Customer quality** — Which RFM segments hold the most lifetime value?
- **Geographic opportunity** — Which states and regions should receive more investment?
- **Channel efficiency** — Which acquisition channels deliver the best revenue-per-customer?
- **Discount risk** — Are discounts expanding volume enough to offset margin compression?
- **Order health** — What revenue is lost to returns and cancellations?

---

## Dataset Overview

All data was created for this project. The dataset covers **January 2024 – December 2025**.

| Table | File | Rows | Description |
|-------|------|------|-------------|
| FactSales | `data/FactSales.csv` | 15,668 | Order line items (all statuses) |
| DimCustomer | `data/DimCustomer.csv` | 3,600 | Customer dimension with RFM attributes |
| DimDate | `data/DimDate.csv` | 731 | Full date dimension |
| DimProduct | `data/DimProduct.csv` | 90 | Product master with cost and margin |
| CustomerRFM | `data/CustomerRFM.csv` | 2,047 | Pre-computed RFM scores and segments |
| BusinessInsights | `data/BusinessInsights.csv` | 8 | Narrative insight reference table |

See [`data/README.md`](data/README.md) for column-level documentation and data licensing.

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Microsoft Power BI Desktop** | Dashboard, DAX measures, data model |
| **Python** (pandas, NumPy) | EDA, data cleaning, RFM segmentation |
| **Jupyter Notebook** | Exploratory analysis (`notebooks/`) |
| **DAX** | 30+ calculated measures across 6 functional groups |
| **Git / GitHub** | Version control and portfolio publication |

---

## Data Model

Star schema with `FactSales` at the centre:

```
           DimDate
              │ (Many:1 · active)
              │
DimCustomer ──┼── FactSales ──── DimProduct
 (Many:1)     │                   (Many:1 · active)
              │ (1:1 · active)
           CustomerRFM
```

- All relationships use single-directional filtering toward the fact table.
- `BusinessInsights` is an unrelated reference table (Page 5 only).
- `DimDate` is marked as the date table; time-intelligence measures require this.

Full setup instructions: [`docs/PowerBI_Model_Guide.md`](docs/PowerBI_Model_Guide.md)

---

## Dashboard Pages

### Page 1 — Executive Overview
One-page health check: 6 KPI cards (Revenue, Profit, Margin %, Orders, Customers, AOV), monthly revenue & profit trend line chart, revenue by category bar, and revenue by region donut. Slicers: Year, Category.

### Page 2 — Sales & Product Performance
Category-level revenue vs profit comparison, product profitability scatter plot (Revenue × Margin %), Top 10 products by revenue, and a discount impact table. Slicers: Year, Region.

### Page 3 — Customer Insights & RFM Segmentation
RFM segment distribution, revenue by segment, customer recency-vs-frequency scatter, and a Top 10 customers table with RFM labels. Slicers: Year, Region.

### Page 4 — Geographic & Channel Performance
Filled map of the US by state revenue, Top 10 states bar chart, regional column chart, and acquisition channel revenue bar. Slicers: Year, Region.

### Page 5 — Business Insights & Recommendations
Order status donut, returned revenue and return rate KPIs, a full Business Insights table, and three priority action cards (Discount Strategy, At-Risk Win-Back, Storage Expansion). Slicers: Year, Category.

---

## Key Findings

All figures verified against `data/FactSales.csv` (completed orders only) and `data/CustomerRFM.csv`.

| # | Finding | Metric |
|---|---------|--------|
| 1 | Healthy top-line revenue over 2 years | $1,888,956 total revenue |
| 2 | Strong gross profit margin | 49.2% overall |
| 3 | Discounts erode margin significantly | 40.8% vs 50.4% — 9.6 pp gap |
| 4 | 405 At-Risk customers hold material past value | $615K combined historical revenue |
| 5 | Storage is the highest-margin category but undersized | 54% gross margin; only 7.4% revenue share |
| 6 | Top 4 states = ~37% of revenue | CA $257K, NY $157K, TX $150K, FL $142K |
| 7 | Organic Search is the most efficient channel | $778K revenue from 741 customers |
| 8 | Return rate is manageable | 4.4% return rate; $117K returned revenue |

---

## DAX Measures

30+ measures across six groups — all in [`dax/DAX_Measures.dax`](dax/DAX_Measures.dax):

| Group | Measures (examples) |
|-------|---------------------|
| Executive KPIs | Total Revenue, Total Profit, Profit Margin %, Total Orders, AOV |
| Time-Series | MoM Revenue Change, MoM Growth %, YTD Revenue, YoY Growth % |
| Product & Category | Sales Contribution %, Product Revenue Rank |
| Customer | Repeat Customers, One-Time Customers, Repeat Customer Rate % |
| Discount | Profit Margin on Discounted/Non-Discounted Orders, Discount Margin Gap |
| Order Status | Returned Orders, Returned Revenue, Return Rate %, Canceled Orders |

Validation targets and implementation guide: [`dax/DAX_Measures_Guide.md`](dax/DAX_Measures_Guide.md)

---

## How to Open the Dashboard

1. **Install Power BI Desktop** (free) from [powerbi.microsoft.com](https://powerbi.microsoft.com/en-us/desktop/).
2. **Clone or download** this repository.
3. **Open** `powerbi/Ecommerce_Sales_Intelligence.pbix` in Power BI Desktop.
4. The data is embedded — no additional connection or file path change is needed.
5. Navigate the five dashboard pages using the tabs at the bottom of the screen.
6. Use the **Year**, **Region**, and **Category** slicers to explore interactively.

To rebuild the model from the raw CSVs:
- Follow [`docs/PowerBI_Model_Guide.md`](docs/PowerBI_Model_Guide.md) step by step.
- Paste measures from [`dax/DAX_Measures.dax`](dax/DAX_Measures.dax) and validate against the targets in [`dax/DAX_Measures_Guide.md`](dax/DAX_Measures_Guide.md).

---

## Repository Structure

```
ecommerce-sales-intelligence/
├── README.md
├── .gitignore
├── LICENSE
│
├── report/
│   ├── project-report.md          ← Full project report (Markdown)
│   └── project-report.pdf         ← Rendered PDF (generate from Markdown)
│
├── powerbi/
│   ├── Ecommerce_Sales_Intelligence.pbix
│   └── screenshots/
│       ├── 01-executive-overview.png
│       ├── 02-sales-product-performance.png
│       ├── 03-customer-rfm-segmentation.png
│       ├── 04-geographic-channel-performance.png
│       └── 05-business-insights-recommendations.png
│
├── data/
│   ├── README.md                  ← Data dictionary and licensing
│   ├── FactSales.csv
│   ├── DimCustomer.csv
│   ├── DimDate.csv
│   ├── DimProduct.csv
│   ├── CustomerRFM.csv
│   └── BusinessInsights.csv
│
├── dax/
│   ├── DAX_Measures.dax           ← All 30+ DAX measure definitions
│   └── DAX_Measures_Guide.md      ← Validation targets and implementation guide
│
├── docs/
│   ├── PowerBI_Model_Guide.md     ← Step-by-step model setup
│   └── PowerBI_Dashboard_Specification.md  ← Visual-level build spec
│
└── notebooks/
    └── ecommerce_sales_analysis.ipynb  ← Python EDA and RFM computation
```

---

## Data & Licensing

The data files in `data/` were created by the project author for this portfolio project. They are not sourced from a third-party database and contain no real personal or commercial data.

**You may** use the data files for learning, practice, and portfolio projects.  
**Please credit** this repository if you publish derived work.

The Power BI file (`Ecommerce_Sales_Intelligence.pbix`) is the author's original work. See [`LICENSE`](LICENSE) for the full terms.

---

## Limitations

- **Gross margin only.** Profit figures exclude operating costs, marketing spend, and logistics. The 49.2% margin is gross, not net.
- **No sales targets.** No variance-to-budget analysis is possible. Trend-only comparisons are used throughout.
- **Repeat Customer Rate figure.** The DAX-validated rate is 64.4%. The dashboard shows 79.7% on Pages 3 and 4, likely due to a different denominator in the visual filter context. The 64.4% figure is used in the written report.
- **RFM is relative.** Segment labels are based on the two-year window in this dataset. They should not be interpreted as absolute customer quality ratings.
- **No 2023 data.** YoY measures return BLANK for all of 2024 because no prior-year data exists.

---

## Future Enhancements

- **Sales target integration** — Add a `SalesTarget` table at Month × Category grain
- **Forecasting** — Extend the date table and apply Power BI's built-in forecast or an Azure ML model
- **Customer LTV** — Implement a BG/NBD probabilistic lifetime value model
- **Row-level security** — Restrict regional managers to their own data
- **Live data refresh** — Connect to Azure SQL or Snowflake with scheduled Power BI Service refresh
- **Drill-through pages** — Category detail and individual customer profile pages

---

*Built by Naveen Kumar K · October 2026*  
*Tools: Power BI Desktop · Python · DAX · Git*
