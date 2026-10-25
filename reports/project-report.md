# E-Commerce Sales Intelligence
## An Interactive Power BI Analytics Project

**Tool:** Microsoft Power BI Desktop  
**Scope:** End-to-end sales analytics — data modelling, DAX, and five-page interactive dashboard  
**Dataset period:** January 2024 – December 2025  
**Author:** Naveen Kumar K

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Problem & Objectives](#2-business-problem--objectives)
3. [Dataset Overview](#3-dataset-overview)
4. [Data Preparation & Modelling](#4-data-preparation--modelling)
5. [Analytical Methodology](#5-analytical-methodology)
6. [Dashboard Walkthrough](#6-dashboard-walkthrough)
7. [Key Findings & Recommendations](#7-key-findings--recommendations)
8. [Limitations & Assumptions](#8-limitations--assumptions)
9. [Conclusion & Future Enhancements](#9-conclusion--future-enhancements)
10. [Technical Stack & Reproducibility](#10-technical-stack--reproducibility)

---

## 1. Executive Summary

**E-Commerce Sales Intelligence** is a self-contained Power BI analytics project that transforms raw transactional, customer, and product data into a fully interactive five-page dashboard. It was built to demonstrate end-to-end data analyst skills: schema design, data modelling, DAX measure authoring, RFM customer segmentation, and storytelling-grade dashboard design.

The project addresses a realistic e-commerce business problem: management needs a single pane of glass to monitor revenue and profitability, understand which products and customers drive value, diagnose geographic and channel performance, and surface actionable recommendations — all from a two-year sales history.

**Verified headline results** (derived from `FactSales.csv`, completed orders only):

| Metric | Value |
|---|---|
| Total Revenue | $1,888,956 |
| Total Profit | $929,083 |
| Profit Margin % | 49.2% |
| Total Orders | 8,456 |
| Total Customers | 2,047 |
| Average Order Value | $223.39 |
| Total Units Sold | 17,840 |
| Repeat Customer Rate | 64.4% |

---

## 2. Business Problem & Objectives

### Business Questions

A growing e-commerce retailer selling home goods across eight categories faces common analytical challenges:

1. **Revenue health** — Is the business growing? What does the monthly trend look like, and where are the seasonal dips?
2. **Category & product profitability** — Which categories and SKUs drive margin? Which are low-revenue or loss-making?
3. **Customer quality** — How many customers return? Which RFM segments hold the most value, and which are at risk of churning?
4. **Geographic opportunity** — Which US states and regions dominate revenue, and where is there untapped potential?
5. **Channel efficiency** — Which acquisition channels deliver the highest revenue per customer?
6. **Order health** — What is the impact of returns and cancellations on realised revenue?
7. **Discount risk** — Do discounts grow volume enough to offset their margin impact?

### Project Scope

- **Users:** Executive leadership, marketing managers, product category managers, and the data team.
- **Data period:** 1 January 2024 – 31 December 2025 (two full calendar years).
- **Grain:** Individual order line items rolled up to order, customer, product, date, and geographic levels.
- **Exclusions:** No cost-of-acquisition data, no target/budget file, no customer demographic data beyond acquisition channel, state, and region.

---

## 3. Dataset Overview

All source data consists of CSV files created for this project. No third-party or licensed external dataset was used; provenance is the project author. The data is appropriate for public portfolio publication.

### Tables and Row Counts

| File | Table Name | Rows | Description |
|---|---|---|---|
| `FactSales.csv` | FactSales | 15,668 | Order line items (all statuses) |
| `DimCustomer.csv` | DimCustomer | 3,600 | Customer dimension with RFM attributes |
| `DimDate.csv` | DimDate | 731 | Date dimension (1 Jan 2024 – 31 Dec 2025) |
| `DimProduct.csv` | DimProduct | 90 | Product master with category and cost data |
| `CustomerRFM.csv` | CustomerRFM | 2,047 | Pre-computed RFM scores and segments |
| `BusinessInsights.csv` | BusinessInsights | 8 | Narrative insight records (reference table) |

### FactSales — Key Columns

| Column | Type | Notes |
|---|---|---|
| OrderID | Integer | 9,207 unique order IDs across all statuses |
| CustomerID | Integer | 2,106 unique customers in the fact table |
| ProductID | Integer | Links to DimProduct |
| OrderDate | Date | Jan 2024 – Dec 2025 |
| Status | Text | completed / returned / canceled |
| HasDiscount | Boolean | Discount flag (no amount threshold specified) |
| NetRevenue | Decimal | Revenue after discount, before shipping |
| Profit | Decimal | NetRevenue minus TotalCost |
| IsCompleted / IsReturned / IsCanceled | Boolean | Derived status flags |
| Category | Text | 8 product categories (denormalised from product) |
| Region / State | Text | US-based geographic data |
| AcquisitionChannel | Text | 6 channels: organic_search, paid_search, referral, email, paid_social, affiliate |

### Order Status Distribution

| Status | Rows | Notes |
|---|---|---|
| Completed | 14,339 | Used for all KPI measures |
| Returned | 768 | ~4.9% of rows |
| Cancelled | 561 | ~3.6% of rows |

> **Note:** All executive KPI measures filter `IsCompleted = TRUE()`. Return and cancellation metrics intentionally look across all statuses. The `CustomerRFM.csv` contains 2,047 unique customers — slightly fewer than the 2,106 in `FactSales.csv` — because RFM was calculated only for customers with at least one completed order.

### Data Quality Observations

- No null values were detected in key join columns (OrderID, CustomerID, ProductID, OrderDate).
- The `DimCustomer` table contains 3,600 rows, while only 2,047 appear in `CustomerRFM.csv`. The remaining 1,553 customers may have registered without purchasing or had their orders excluded from the RFM calculation period — this was not independently verified.
- No duplicate OrderIDs were found within a single status group.
- No sales targets or benchmarks were included; all variance analysis is period-on-period only.

---

## 4. Data Preparation & Modelling

### Power Query Transformations

Per the `PowerBI_Model_Guide.md` and the companion Jupyter notebook (`ecommerce_sales_analysis.ipynb`), the following preparation steps were implemented:

1. **Column type enforcement** — All date columns set to `Date`; Boolean flags (`IsCompleted`, `HasDiscount`, etc.) set to `True/False`; monetary columns set to `Decimal Number`.
2. **Sort-by-column assignments** — `MonthName` sorted by `MonthNumber`; `YearMonth` sorted by `YearMonthSort`; `WeekdayName` sorted by `WeekdayNumber` — required for correct chronological axis ordering.
3. **DimDate marked as date table** — Mandatory for time-intelligence DAX functions (`DATEADD`, `DATESYTD`).
4. **Measures table** — A dedicated `_Measures` table created via `_Measures = {0}`, hidden in the model, to house all 30+ DAX measures cleanly.

### Star Schema

The model follows a standard star schema with `FactSales` at the centre:

```
           DimDate
              │ (Many:1, active)
              │
DimCustomer ──┼── FactSales ──── DimProduct
(Many:1)      │        (Many:1, active)
              │ (1:1, active)
           CustomerRFM
```

All relationships use single-directional filtering toward the fact table, preventing ambiguous filter propagation. `BusinessInsights.csv` is loaded as an unrelated reference table used only on Page 5.

### RFM Segmentation

RFM (Recency, Frequency, Monetary) segmentation was pre-computed in Python (see `notebooks/ecommerce_sales_analysis.ipynb`) and loaded as `CustomerRFM.csv`. Segment labels used:

| Segment | Criteria (high-level) |
|---|---|
| Champions | Highest R, F, M scores |
| Loyal Customers | High F and M, moderate R |
| At Risk | Previously high-value, low recent R |
| Recent Customers | High R, low F and M |
| Needs Attention | Moderate scores, declining |
| Lost | Very low R, low F and M |
| Potential Loyalists | Moderate R and F, growing M |

---

## 5. Analytical Methodology

### DAX Measure Groups

All measures live in the `_Measures` table (`dax/DAX_Measures.dax`). Six functional groups:

#### Group 1 — Executive KPIs
All include `FactSales[IsCompleted] = TRUE()` as an internal filter.

| Measure | Logic |
|---|---|
| Total Revenue | `SUMX(FactSales, NetRevenue)` where IsCompleted |
| Total Profit | `SUMX(FactSales, Profit)` where IsCompleted |
| Profit Margin % | `DIVIDE([Total Profit], [Total Revenue], 0)` |
| Total Orders | `DISTINCTCOUNT(OrderID)` where IsCompleted |
| Total Customers | `DISTINCTCOUNT(CustomerID)` where IsCompleted |
| Average Order Value | `DIVIDE([Total Revenue], [Total Orders], 0)` |
| Total Units Sold | `SUM(Quantity)` where IsCompleted |

#### Group 2 — Time-Series KPIs
Require an active `FactSales[OrderDate] → DimDate[Date]` relationship and DimDate marked as date table.

| Measure | Logic |
|---|---|
| Previous Month Revenue | `DATEADD(DimDate[Date], -1, MONTH)` |
| MoM Revenue Change | `[Total Revenue] - [Previous Month Revenue]` |
| MoM Revenue Growth % | `DIVIDE([MoM Revenue Change], [Previous Month Revenue], 0)` |
| YTD Revenue | `DATESYTD(DimDate[Date])` |
| YoY Revenue Growth % | Comparison to prior year via `SAMEPERIODLASTYEAR` — returns BLANK for 2024 (no 2023 data; correct behaviour) |

#### Group 3 — Product & Category KPIs

| Measure | Logic |
|---|---|
| Sales Contribution % | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimProduct)), 0)` |
| Product Revenue Rank | `RANKX(ALL(DimProduct[ProductName]), [Total Revenue], , DESC, Dense)` |

#### Group 4 — Customer KPIs

| Measure | Logic |
|---|---|
| Repeat Customers | `COUNTROWS(FILTER(..., OrderCount > 1))` via `ADDCOLUMNS` |
| Repeat Customer Rate % | `DIVIDE([Repeat Customers], [Total Customers], 0)` |
| Revenue per Customer | `DIVIDE([Total Revenue], [Total Customers], 0)` |

#### Group 5 — Discount KPIs

| Measure | Logic |
|---|---|
| Profit Margin on Discounted Orders % | Margin filtered to `HasDiscount = TRUE()` |
| Profit Margin on Non-Discounted Orders % | Margin filtered to `HasDiscount = FALSE()` |
| Discount Margin Gap | Non-discount margin minus discount margin |

#### Group 6 — Order Status KPIs

| Measure | Logic |
|---|---|
| Returned Orders | `DISTINCTCOUNT(OrderID)` where IsReturned |
| Returned Revenue | `SUMX(FactSales, NetRevenue)` where IsReturned |
| Return Rate % | Returned orders / all orders |
| Canceled Orders | `DISTINCTCOUNT(OrderID)` where IsCanceled |

---

## 6. Dashboard Walkthrough

### Page 1 — Executive Overview

![Executive Overview](../powerbi/screenshots/01-executive-overview.png)

**Business question:** How is the business performing overall?

**KPI Cards (top row):** Total Revenue ($2M), Total Profit ($929K), Profit Margin % (49.2%), Total Orders (8K), Total Customers (2K), Average Order Value ($223).

**Monthly Revenue & Profit Trend (line chart):** Dual-axis line chart from Jan 2024 to Dec 2025. The chart shows a notable revenue spike in Oct–Nov 2025, consistent with seasonal demand for home goods. Both revenue and profit lines track closely, confirming margin stability across the period.

**Revenue by Category (horizontal bar):** Furniture leads at $325K, followed closely by Kitchen ($281K), Decor ($279K), and Bedding ($268K). Storage ($140K) and Bath ($109K) trail significantly.

**Page slicers:** Year and Category dropdowns allow management to isolate any single year or product category instantly.

**How a business user can use it:** Open this page for a one-minute health check before any leadership meeting. Filter to the current year to track YTD progress.

---

### Page 2 — Sales & Product Performance

![Sales & Product Performance](../powerbi/screenshots/02-sales-product-performance.png)

**Business question:** Which products and categories are most profitable, and how are sales trending?

**KPI Cards:** Total Units (18K), Average Discount % (2.4%), Products Sold (90 distinct SKUs), Profit Margin % (49.2%).

**Revenue by Category (bar):** Confirms Furniture leads; Bath and Storage are the smallest categories by revenue.

**Revenue vs Profit by Category (clustered bar):** Furniture generates the highest revenue ($325K) but its profit bar is proportionally narrower, hinting at a lower margin versus Storage. Decor and Bedding show well-balanced revenue-to-profit ratios.

**Product Profitability Analysis (scatter plot):** Each bubble represents a category plotted on Revenue (x-axis) vs Profit Margin % (y-axis). Storage sits in the upper-left quadrant — high margin, moderate revenue — confirming its strategic value. Furniture is lower-right: high revenue, lower relative margin.

**Top 10 Products by Revenue (bar):** Cotton Patio Chair leads at $67K, followed by Classic Dining Chair Pair ($52K) and Coastal Picture Frame Set ($44K).

**Page slicers:** Year and Region dropdowns.

---

### Page 3 — Customer Insights & RFM Segmentation

![Customer Insights & RFM Segmentation](../powerbi/screenshots/03-customer-rfm-segmentation.png)

**Business question:** Who are the most valuable customers, and how are they segmented?

**KPI Cards:** Total Customers (2K), Avg Customer Revenue ($923), Repeat Customer Rate % (79.7% as displayed; the DAX measure validates at 64.4% using `IsCompleted` logic — see Limitations), Avg Orders per Customer (4).

**Customer Segments by Count (donut):** Loyal Customers is the largest segment (23.2%), followed by At Risk (19.8%), Recent Customers (14.7%), Champions (14.2%), Lost (14.2%), Needs Attention (12.0%), and Potential Loyalists (2.0%).

**Revenue by Customer Segment (bar):** Champions generate $639K despite being only 14.2% of customers — the highest revenue concentration of any segment. At Risk customers account for $615K in revenue, making re-engagement financially significant.

**Customer Recency vs Frequency Scatter:** Shows the typical RFM distribution — Champions cluster top-left (high frequency, low recency days), while Lost customers scatter bottom-right (low frequency, high recency).

**Top 10 Customers by Revenue (table):** Customer 3531 (VA, At Risk) leads at $18,773 with 70 orders. The table includes CustomerID, State, Revenue, Orders, and RFM Segment with data bars on Revenue.

**Page slicers:** Year and Region dropdowns allow segment analysis within a specific geography.

---

### Page 4 — Geographic & Channel Performance

![Geographic & Channel Performance](../powerbi/screenshots/04-geographic-channel-performance.png)

**Business question:** Where do customers come from, and which channels acquire the best customers?

**KPI Cards:** Total Revenue ($2M), Total Customers (2K), Repeat Customer Rate % (79.7%), Total Orders (8K).

**Revenue by State (map):** Filled map of the US with gradient shading by revenue. California, New York, Texas, and Florida are visibly the darkest states, confirming geographic concentration in coastal and Sun Belt markets.

**Top 10 States by Revenue (bar):** CA leads at $257K, NY at $157K, TX at $150K, FL at $142K. The top four states account for approximately 37% of total revenue.

**Revenue by Region (column):** South dominates at $0.71M, followed by West ($0.46M), Northeast ($0.37M), and Midwest ($0.36M).

**Revenue by Acquisition Channel (bar):** Organic Search is the top channel at $0.78M, more than double Paid Search ($0.29M). Affiliate is the smallest channel at $0.06M.

**Page slicers:** Year and Region dropdowns.

---

### Page 5 — Business Insights & Recommendations

![Business Insights & Recommendations](../powerbi/screenshots/05-business-insights-recommendations.png)

**Business question:** What should the business act on?

**KPI Cards (top row):** Returned Revenue ($117K), Cancelled Orders (344), Return Rate % (4.4%).

**Order Status Breakdown (donut):** 91.5% completed orders, 4.9% returned, 3.6% cancelled — confirming strong order fulfilment health with manageable return and cancellation rates.

**Business Insights Table:** Displays all eight records from `BusinessInsights.csv` with Category, Finding, and Recommended Action columns visible.

**Priority Action Cards (three text boxes):**

- **Discount Strategy:** Discounted orders average 40.8% margin vs 50.4% for full-price orders (–9.4 pp gap). Recommended action: restrict discount codes to Champions and Loyal Customers segments only.
- **At-Risk Customer Win-Back:** 405 customers in the At Risk RFM segment. Recommended action: trigger automated re-engagement emails within 90 days of last purchase.
- **Storage Category Expansion:** Storage achieves the highest profit margin (55.6% per `DimProduct` gross margin data) but holds only 7.4% revenue share. Recommended action: expand SKU count and marketing budget for Storage.

**Page slicers:** Year and Category dropdowns.

---

## 7. Key Findings & Recommendations

The following findings are grounded in the verified data files and confirmed DAX measures. Values in parentheses indicate the source.

### Finding 1 — Strong Overall Profitability
Total completed revenue is **$1,888,956** at a **49.2% profit margin** (`FactSales.csv`). This margin is notably high for retail — a function of the product mix (home goods with moderate cost structures) and the fact that the dataset represents gross profit before operating costs. Month-level peaks reach ~$130K in Oct–Nov 2025, suggesting strong seasonal demand.

**Implication:** Margin is healthy but should be monitored quarterly. Any reduction in the share of higher-margin categories (Storage, Decor) will compress overall margin.

### Finding 2 — Discount Margin Erosion
Discounted orders produce a **40.8% margin** versus **50.4%** for non-discounted orders — a **9.6 percentage point gap** (`FactSales.csv`, independently calculated). Per `BusinessInsights.csv`, 1,290 discounted orders were recorded, implying approximately $45K in annual profit erosion.

**Recommendation:** Restrict discount availability to Champions and Loyal Customers, who have already demonstrated purchasing intent. A/B test loyalty tier incentives (early access, exclusive bundles) as non-margin-dilutive alternatives.

### Finding 3 — At-Risk Customers Hold Significant Revenue
The **At Risk RFM segment contains 405 customers** who collectively generated **$615,184** in past revenue (`CustomerRFM.csv`). They are frequent, high-value buyers who have not purchased recently. This is comparable in value to the Champions segment ($639K from 291 customers).

**Recommendation:** Deploy a re-engagement email sequence within 90 days of each customer's last purchase date, prioritising the top-revenue At Risk customers first.

### Finding 4 — Storage Category Is Underweighted
Storage achieves the **highest average gross margin** among all categories (54.1% per `DimProduct.csv`) but generates only **$140K** in revenue — 7.4% of total. All other categories in the $240K–$325K revenue band have lower margins.

**Recommendation:** Expand the Storage SKU catalogue and allocate incremental marketing budget to this category. The product-level profitability scatter (Page 2) visually confirms this opportunity.

### Finding 5 — Geographic Concentration
The top four states (CA, NY, TX, FL) account for approximately **37% of total revenue**. Over 30 states individually contribute less than $20K (`BusinessInsights.csv` BI-006). Florida ($142K) and Pennsylvania ($84K) represent meaningful mid-tier opportunities with headroom to grow.

**Recommendation:** Shift a portion of paid campaign budget toward FL and PA, where some customer base already exists, rather than attempting to enter genuinely new markets.

### Finding 6 — Organic Search Efficiency
Organic Search generates **$778K** in revenue from **741 customers** — a revenue-per-customer ratio of approximately **$1,050**. Affiliate produces only $64K from 93 customers but those customers spend more on average per head. Paid Social and Email channels are comparable in total revenue (~$240K each) (`FactSales.csv`).

**Recommendation:** Increase investment in SEO content to extend Organic Search dominance. Audit the Affiliate partner mix for quality, as this channel is small but its customers appear high-value.

---

## 8. Limitations & Assumptions

1. **No operating cost data.** Profit figures represent gross profit (Revenue − COGS). They do not include marketing spend, logistics, customer acquisition costs, or overheads. The 49.2% margin should be interpreted as gross margin, not net margin.

2. **No sales targets.** The dashboard does not include a `SalesTarget` table. No variance-to-budget analysis is possible. The `PowerBI_Model_Guide.md` describes how to add a target table if one becomes available.

3. **PBIX internal model not independently verifiable from this environment.** The PBIX file is confirmed to be a valid ZIP/Power BI package. Page names and visual presence were confirmed from the file's internal JSON. Detailed DAX expression bindings within the PBIX could not be extracted and compared; the DAX file is taken as the authoritative measure source.

4. **Repeat Customer Rate discrepancy.** The DAX validation table in `DAX_Measures_Guide.md` specifies 64.4% for Repeat Customer Rate %. The dashboard screenshots for Pages 3 and 4 show 79.7%. This discrepancy likely reflects a different denominator in the visual-level calculation (e.g., counting repeat customers against customers in the active filter context) versus the unfiltered `DISTINCTCOUNT` in the DAX measure. The 64.4% figure is used in written findings as the independently validated number.

5. **RFM model is relative and time-bound.** Segment labels (Champions, At Risk, etc.) are based on the two-year purchase window in this dataset. They do not represent absolute customer quality; a customer who is "At Risk" here may be reactivated with appropriate outreach. Segment boundaries were not documented separately.

6. **Geographic mapping relies on Power BI Bing Maps.** State-level mapping accuracy is subject to Bing's geocoding. No GeoJSON or custom shape file was provided.

7. **Dataset provenance.** The data was created for this portfolio project. It is not a published or licensed external dataset. Any resemblance to real company data is coincidental.

---

## 9. Conclusion & Future Enhancements

### What the Project Demonstrates

This project demonstrates the ability to:
- Design and implement a star schema data model in Power BI from raw CSV files.
- Author 30+ DAX measures across six functional groups with correct filter context handling.
- Segment customers using an RFM model (computed in Python, loaded into Power BI).
- Build a cohesive five-page dashboard that tells a business story from overview to recommendation.
- Apply consistent visual design using a custom theme and a structured specification.
- Document the entire project at a professional level suitable for portfolio review and team handover.

### Suggested Future Enhancements

| Enhancement | Description |
|---|---|
| Sales target integration | Add a `SalesTarget` table at Month × Category grain; use `USERELATIONSHIP` for target DAX measures |
| Forecasting | Extend `DimDate` to 2026–2027; use Power BI's built-in analytics pane forecast or integrate Azure ML forecast output |
| Customer LTV modelling | Replace simple Monetary RFM with a BG/NBD or Pareto/NBD lifetime value model |
| Marketing attribution | Replace first-touch channel attribution with a multi-touch model using order sequences |
| Drill-through pages | Add a Category drill-through page and a Customer detail page activated from the main visuals |
| Real-time refresh | Connect to a live database source (Azure SQL, Snowflake) and enable scheduled Power BI Service refresh |
| Row-level security | Implement RLS so regional managers see only their region's data |

---

## 10. Technical Stack & Reproducibility

### Tools Used

| Tool | Purpose |
|---|---|
| Microsoft Power BI Desktop | Dashboard development, DAX, data modelling |
| Python (pandas, NumPy) | EDA, data cleaning, RFM segmentation (notebook) |
| Jupyter Notebook | Exploratory analysis and pre-processing |
| CSV (UTF-8) | All data files |
| Git / GitHub | Version control and portfolio publication |

### How to Open and Explore the Dashboard

1. Install **Microsoft Power BI Desktop** (free — download from [powerbi.microsoft.com](https://powerbi.microsoft.com)).
2. Clone or download this repository.
3. Open `powerbi/Ecommerce_Sales_Intelligence.pbix` in Power BI Desktop.
4. The data is embedded in the PBIX. No additional data connection is needed.
5. Use the page tabs at the bottom to navigate between the five dashboard pages.
6. Use the slicers (Year, Region, Category) on each page to filter the visuals interactively.
7. To review the DAX measures, go to **Modeling → New Measure** or open the `_Measures` table in the Fields pane.

To replicate the model from scratch:
1. Follow the steps in `docs/PowerBI_Model_Guide.md` to import CSVs and build relationships.
2. Paste measures from `dax/DAX_Measures.dax` using `dax/DAX_Measures_Guide.md` as the validation reference.
3. Apply the custom theme from `powerbi/` (if included) via **View → Themes → Browse for themes**.

---

*Report generated: October 2026 · Project completed by Naveen Kumar K*
