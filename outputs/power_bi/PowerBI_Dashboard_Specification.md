# Power BI Dashboard Specification
## E-commerce Sales Intelligence

Report canvas: 1280 × 720 px (16:9). Use the theme file `theme.json`.

---

## PAGE 1 — Executive Overview

**Purpose:** Give management a one-page health-check of the business.

### Layout (top to bottom)

#### Row 1 — KPI Cards (6 cards, equal width)
| # | Visual | Measure | Format | Notes |
|---|---|---|---|---|
| 1 | Card | Total Revenue | $1.89M | Bold, large font |
| 2 | Card | Total Profit | $929K | |
| 3 | Card | Profit Margin % | 49.2% | Conditional colour: ≥45% green |
| 4 | Card | Total Orders | 8,456 | |
| 5 | Card | Total Customers | 2,047 | |
| 6 | Card | Average Order Value | $223 | |

#### Row 2 — Trend + Category side by side

**Left — Monthly Revenue & Profit Trend (Line Chart)**
- X-axis: `DimDate[YearMonth]` sorted by `YearMonthSort`
- Y-axis: `[Total Revenue]` (line 1), `[Total Profit]` (line 2)
- Markers: On
- Title: "Monthly Revenue vs Profit (Completed Orders)"
- Legend: Bottom

**Right — Revenue by Category (Horizontal Bar Chart)**
- Y-axis: `FactSales[Category]` sorted by `[Total Revenue]` DESC
- X-axis: `[Total Revenue]`
- Data labels: On ($ value)
- Title: "Revenue by Category"

#### Row 3 — Region + Business Summary side by side

**Left — Revenue by Region (Donut Chart)**
- Legend: `DimCustomer[Region]`
- Values: `[Total Revenue]`
- Title: "Revenue by Region"

**Right — Business Summary (Text Box)**
```
Revenue: $1.89M | Profit: $929K | Margin: 49.2%
Date Range: Jan 2024 – Dec 2025
Top Category: Furniture ($325K)
Top State: California ($257K)
Repeat Customer Rate: 64.4%
Data excludes 407 returns ($117K) & 344 cancellations ($76K)
```

#### Page-level Slicers (top bar)
- Year slicer: `DimDate[Year]` — Dropdown
- Category slicer: `FactSales[Category]` — Dropdown

---

## PAGE 2 — Sales Trends

**Purpose:** Explain how sales move over time and identify seasonality.

#### Row 1 — Monthly Sales & MoM Growth

**Full-width Line Chart — Monthly Revenue Trend**
- X-axis: `DimDate[YearMonth]` sorted by `YearMonthSort`
- Y-axis: `[Total Revenue]`
- Reference line at mean revenue
- Title: "Monthly Revenue Trend (2024–2025)"

#### Row 2 — Two charts side by side

**Left — MoM Revenue Change (Column Chart)**
- X-axis: `DimDate[YearMonth]`
- Y-axis: `[MoM Revenue Change]`
- Conditional formatting: positive = green, negative = red
- Title: "Month-over-Month Revenue Change ($)"

**Right — Revenue by Quarter (Clustered Column)**
- X-axis: `DimDate[QuarterLabel]`
- Legend: `DimDate[Year]`
- Y-axis: `[Total Revenue]`
- Title: "Quarterly Revenue by Year"

#### Row 3 — Weekday + Category Trend

**Left — Revenue by Weekday (Column Chart)**
- X-axis: `DimDate[WeekdayName]` sorted by `WeekdayNumber`
- Y-axis: `[Total Revenue]`
- Title: "Revenue by Day of Week"

**Right — Category Revenue Trend (Line Chart)**
- X-axis: `DimDate[YearMonth]`
- Legend: `FactSales[Category]`
- Y-axis: `[Total Revenue]`
- Title: "Category Revenue Over Time"
- Note: Show top 4 categories to avoid clutter

#### Page-level Slicers
- Date range slicer: `DimDate[Date]` — Between
- Category slicer: `FactSales[Category]` — Multi-select checklist

---

## PAGE 3 — Product & Category Performance

**Purpose:** Understand which products and categories drive revenue and profit.

#### Row 1 — Category deep-dive (three charts)

**Left — Category Revenue vs Profit (Clustered Bar)**
- Y-axis: `FactSales[Category]`
- Values: `[Total Revenue]` (bar 1), `[Total Profit]` (bar 2)
- Sort by Revenue DESC
- Title: "Revenue & Profit by Category"

**Centre — Profit Margin by Category (Column Chart)**
- X-axis: `FactSales[Category]`
- Y-axis: `[Profit Margin %]`
- Reference line at 49.2% (overall average)
- Conditional colour: above average = teal, below = amber
- Title: "Profit Margin % by Category"

**Right — Sales Contribution % (Donut)**
- Legend: `FactSales[Category]`
- Values: `[Sales Contribution %]`
- Title: "Revenue Share by Category"

#### Row 2 — Top / Bottom Products

**Left — Top 10 Products by Revenue (Bar Chart)**
- Filter: `[Product Revenue Rank]` ≤ 10
- Y-axis: `DimProduct[ProductName]`
- X-axis: `[Total Revenue]`
- Title: "Top 10 Products by Revenue"

**Right — Bottom 10 Products by Profit (Bar Chart)**
- Filter: sort ASC by `[Total Profit]`, take 10
- Y-axis: `DimProduct[ProductName]`
- X-axis: `[Total Profit]`
- Conditional colour: negative profit = red
- Title: "Lowest-Profit Products"

#### Row 3 — Discount Impact Table

**Full-width Table**
| Column | Source |
|---|---|
| Category | FactSales[Category] |
| Total Revenue | [Total Revenue] |
| Discounted Revenue | CALCULATE([Total Revenue], HasDiscount=TRUE) |
| Discount Margin % | [Profit Margin on Discounted Orders %] |
| Non-Discount Margin % | [Profit Margin on Non-Discounted Orders %] |
| Margin Gap | [Discount Margin Gap] |

#### Page-level Slicers
- Category slicer: `FactSales[Category]`
- Discount toggle: `FactSales[HasDiscount]` — Dropdown

---

## PAGE 4 — Customer & Geographic Insights

**Purpose:** Understand who buys, from where, and how to retain them.

#### Row 1 — Top Customers + RFM (side by side)

**Left — Top 20 Customers by Revenue (Table)**
| Column | Source |
|---|---|
| CustomerID | FactSales[CustomerID] |
| State | DimCustomer[State] |
| Revenue | [Total Revenue] |
| Orders | [Total Orders] |
| RFM Segment | DimCustomer[RFMSegment] |

Sort by Revenue DESC. Add data bars on Revenue column.

**Right — RFM Segment Distribution (Donut Chart)**
- Legend: `DimCustomer[RFMSegment]`
- Values: `[Total Customers]`
- Title: "Customers by RFM Segment"

#### Row 2 — Geographic Analysis

**Left — Revenue by State (Map or Filled Map)**
- Location: `DimCustomer[State]`
- Values: `[Total Revenue]`
- Title: "Revenue by US State"
- Use filled map with gradient shading

**Centre — Top 10 States (Bar Chart)**
- Y-axis: `DimCustomer[State]`
- X-axis: `[Total Revenue]`
- Filter: top 10 by revenue
- Title: "Top 10 States by Revenue"

**Right — Region Breakdown (Clustered Column)**
- X-axis: `DimCustomer[Region]`
- Y-axis: `[Total Revenue]` and `[Total Customers]`
- Title: "Revenue & Customers by Region"

#### Row 3 — Channel & Repeat Analysis

**Left — Revenue by Acquisition Channel (Bar)**
- Y-axis: `DimCustomer[AcquisitionChannel]`
- X-axis: `[Total Revenue]`
- Sort DESC
- Title: "Revenue by Acquisition Channel"

**Right — Repeat vs One-Time Customers (KPI Cards + Mini Chart)**
- Card 1: `[Repeat Customer Rate %]` — 64.4%
- Card 2: `[Repeat Customers]` — 1,318
- Card 3: `[One-Time Customers]` — 729
- Bar chart: Repeat vs One-Time by region

#### Page-level Slicers
- Region: `DimCustomer[Region]`
- RFM Segment: `DimCustomer[RFMSegment]`
- State: `DimCustomer[State]` — Search slicer

---

## PAGE 5 — Business Insights & Recommendations

**Purpose:** Translate findings into management actions.
(No targets provided; this page serves as the recommendation board.)

#### Row 1 — Return & Cancellation Impact

**Left — Order Status Breakdown (Donut)**
- Values: completed, returned, canceled order counts
- Title: "Order Status Distribution"

**Right — Revenue at Risk (KPI Cards)**
- Card 1: `[Returned Orders]` with `[Returned Revenue]`
- Card 2: `[Canceled Orders]`
- Card 3: `[Return Rate %]`

#### Row 2 — Business Insights Table (Power BI Table Visual)

Import `BusinessInsights.csv` as a reference table (don't relate it).
Display columns: InsightID, Category, Finding, RecommendedAction, KPIToMonitor

Add conditional formatting on Category column.

#### Row 3 — Priority Action Cards (Text Boxes)

**Priority 1 — Discount Reduction**
> Discounted orders average 40.8% margin vs 50.4% for full-price orders (–9.4 pp).
> Action: Restrict discount codes to Champions and Loyal Customers segments only.

**Priority 2 — At-Risk Customer Win-Back**
> 405 customers in the "At Risk" RFM segment. These were frequent, high-value buyers
> who have not purchased recently. Action: Trigger automated re-engagement email within
> 90 days of last purchase date.

**Priority 3 — Storage Category Expansion**
> Storage achieves the highest profit margin (55.6%) but only 7.4% revenue share.
> Action: Expand SKU count and allocate higher marketing budget to Storage category.

---

## Dashboard Interactivity — Global Settings

| Setting | Specification |
|---|---|
| Cross-filtering | All visuals cross-filter unless specified |
| Drill-through | Enable on Product pages (Category → SubCategory → Product) |
| Tooltips | Show Revenue, Profit, Margin %, Order Count on hover |
| Number format | Revenue/Profit: $#,##0 or $#,##0.0K depending on card size |
| Percentage format | #0.0% with 1 decimal |
| Date display | Short month name + year (Jan 2024) |
| Blank handling | Show "—" or 0 with a note; never show blank KPI cards |

---

## Report Theme

Use `theme.json` for consistent colours. Primary palette:
- Dark slate: #1E2D40 (background cards)
- Teal accent: #2A9D8F (positive, completed, on-target)
- Amber: #E9C46A (warning, at risk)
- Coral: #E76F51 (negative, returned, below target)
- Light grey background: #F5F5F5

