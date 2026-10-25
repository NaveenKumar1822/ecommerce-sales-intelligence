# Power BI Data Model Guide
## E-Commerce Sales Intelligence

This guide covers every step needed to rebuild the data model from the raw CSV files
in `data/`. Follow the steps in order. If you are opening the pre-built file, start
at [Verifying the Model](#verifying-the-model) to confirm it matches these specifications.

---

## Step 1: Import the CSV Files

1. Open **Power BI Desktop** → **Home** → **Get Data** → **Text/CSV**
2. Import these files from the `data/` folder in this order:

| File | Table name in Power BI |
|---|---|
| `FactSales.csv` | FactSales |
| `DimDate.csv` | DimDate |
| `DimCustomer.csv` | DimCustomer |
| `DimProduct.csv` | DimProduct |
| `CustomerRFM.csv` | CustomerRFM |
| `BusinessInsights.csv` | BusinessInsights |

> **Note:** `BusinessInsights` is a reference-only table. Do **not** create a
> relationship between it and any other table — it is displayed on Page 5 as
> a standalone visual and must remain unrelated to the model.

---

## Step 2: Validate Data Types in Power Query

Open **Transform Data** and set these column types exactly. Mismatched types
will cause blank visuals and broken DAX measures.

### FactSales — 29 columns

| Column | Type | Notes |
|---|---|---|
| OrderID | Whole Number | |
| CustomerID | Whole Number | Join key → DimCustomer |
| ProductID | Whole Number | Join key → DimProduct |
| OrderDate | Date | Format: yyyy-mm-dd — join key → DimDate |
| Status | Text | Values: `completed`, `returned`, `canceled` |
| PaymentMethod | Text | |
| DiscountCode | Text | Null when no discount applied |
| HasDiscount | True/False | |
| Quantity | Whole Number | |
| UnitPrice | Decimal Number | |
| DiscountAmount | Decimal Number | |
| GrossRevenue | Decimal Number | UnitPrice × Quantity |
| NetRevenue | Decimal Number | GrossRevenue − DiscountAmount |
| TotalCost | Decimal Number | COGS for the line |
| Profit | Decimal Number | NetRevenue − TotalCost |
| ShippingFee | Decimal Number | |
| Category | Text | Denormalised from DimProduct |
| ProductName | Text | Denormalised from DimProduct |
| State | Text | US state abbreviation |
| Region | Text | South / West / Northeast / Midwest |
| AcquisitionChannel | Text | organic_search, paid_search, referral, email, paid_social, affiliate |
| OrderYear | Whole Number | Derived from OrderDate |
| OrderQuarter | Whole Number | 1–4 |
| OrderMonthNum | Whole Number | 1–12 |
| OrderMonthName | Text | January–December |
| OrderYearMonth | Text | e.g. `2024-01` |
| IsCompleted | True/False | TRUE when Status = completed |
| IsReturned | True/False | TRUE when Status = returned |
| IsCanceled | True/False | TRUE when Status = canceled |

### DimDate — 13 columns

| Column | Type | Notes |
|---|---|---|
| Date | Date | Primary key — join target for FactSales[OrderDate] |
| Year | Whole Number | 2024 or 2025 |
| Quarter | Whole Number | 1–4 |
| QuarterLabel | Text | e.g. `Q1 2024` |
| MonthNumber | Whole Number | 1–12 |
| MonthName | Text | Full name — sort by MonthNumber |
| MonthNameShort | Text | Three-letter abbreviation — sort by MonthNumber |
| YearMonth | Text | e.g. `Jan 2024` — sort by YearMonthSort |
| YearMonthSort | Whole Number | Numeric sort key, e.g. `202401` |
| WeekdayName | Text | Monday–Sunday — sort by WeekdayNumber |
| WeekdayNumber | Whole Number | 1 = Monday, 7 = Sunday |
| IsWeekend | True/False | |
| YearQuarter | Text | e.g. `2024-Q1` |

### DimCustomer — 9 columns

| Column | Type | Notes |
|---|---|---|
| CustomerID | Whole Number | Primary key |
| SignupDate | Date | |
| State | Text | US state abbreviation |
| AcquisitionChannel | Text | |
| Region | Text | |
| RFMSegment | Text | Populated via the CustomerRFM join |
| RecencyDays | Whole Number | |
| Frequency | Whole Number | |
| MonetaryValue | Decimal Number | |

### DimProduct — 6 columns

| Column | Type | Notes |
|---|---|---|
| ProductID | Whole Number | Primary key |
| ProductName | Text | |
| Category | Text | 8 categories |
| ListPrice | Decimal Number | |
| UnitCost | Decimal Number | |
| GrossMarginPct | Decimal Number | (ListPrice − UnitCost) / ListPrice |

### CustomerRFM — 12 columns

| Column | Type | Notes |
|---|---|---|
| CustomerID | Whole Number | Join key → DimCustomer (1:1) |
| TotalRevenue | Decimal Number | |
| OrderCount | Whole Number | |
| LastPurchaseDate | Date | |
| RecencyDays | Whole Number | |
| Frequency | Whole Number | |
| MonetaryValue | Decimal Number | |
| RecencyScore | Whole Number | 1–5 |
| FrequencyScore | Whole Number | 1–5 |
| MonetaryScore | Whole Number | 1–5 |
| RFMScore | Whole Number | Sum of R + F + M scores |
| CustomerSegment | Text | Champions, Loyal Customers, At Risk, etc. |

### BusinessInsights — 9 columns (reference table, no relationships)

| Column | Type |
|---|---|
| InsightID | Text |
| Category | Text |
| Finding | Text |
| SupportingMetric | Text |
| BusinessImplication | Text |
| RecommendedAction | Text |
| KPIToMonitor | Text |
| MeasurementPeriod | Text |
| Caveats | Text |

---

## Step 3: Create Relationships

Open **Model view**. Create the four relationships below by dragging the key column
from one table to the matching column in the other.

| From | To | Cardinality | Filter direction | Active |
|---|---|---|---|---|
| FactSales[OrderDate] | DimDate[Date] | Many:1 | Single → DimDate | ✅ Yes |
| FactSales[CustomerID] | DimCustomer[CustomerID] | Many:1 | Single → DimCustomer | ✅ Yes |
| FactSales[ProductID] | DimProduct[ProductID] | Many:1 | Single → DimProduct | ✅ Yes |
| CustomerRFM[CustomerID] | DimCustomer[CustomerID] | 1:1 | Single | ✅ Yes |

**Do not create a relationship for BusinessInsights.** It is a standalone reference table
used only in a table visual on Page 5 of the dashboard.

### Schema diagram

```
                DimDate
                   │
                   │ Many:1 (active)
                   │
DimCustomer ───────┼─────── FactSales ─────── DimProduct
    │          Many:1                  Many:1
    │          (active)                (active)
    │
    │ 1:1 (active)
    │
CustomerRFM


BusinessInsights   [unrelated — no join]
```

### Single filter direction — why it matters

All four relationships use **single-directional filtering** (the filter flows from the
dimension table toward FactSales, never the reverse). This prevents:

- Ambiguous filter paths when two dimension tables share a column (e.g. `State`
  appears in both `DimCustomer` and `FactSales`).
- Unintended cross-filtering between dimensions that would cause incorrect totals
  in aggregated visuals.

If Power BI prompts you to choose a direction, always select the arrow pointing
**away from FactSales** (i.e. the dimension filters the fact, not the other way around).

---

## Step 4: Mark DimDate as the Date Table

Time-intelligence measures (`DATEADD`, `DATESYTD`, `SAMEPERIODLASTYEAR`) only work
correctly when Power BI knows which table is the authoritative date table.

1. In the **Fields** pane, right-click `DimDate`
2. Select **Mark as Date Table**
3. In the dialog, select `Date` as the date column
4. Click **OK** — Power BI validates the column covers a contiguous date range with no gaps

> If you skip this step, `Monthly Revenue`, `YTD Revenue`, and `YoY Revenue Growth %`
> will all return the same value for every row, because the time-intelligence functions
> cannot resolve the date context.

---

## Step 5: Set Sort-by-Column Assignments

Without these assignments, month names sort alphabetically (April before January)
and weekday names sort alphabetically (Friday before Monday).

For each column below: select the column in the **Fields** pane →
**Column tools** tab → **Sort by Column** → choose the sort column.

| Column to sort | Sort by |
|---|---|
| DimDate[MonthName] | DimDate[MonthNumber] |
| DimDate[MonthNameShort] | DimDate[MonthNumber] |
| DimDate[YearMonth] | DimDate[YearMonthSort] |
| DimDate[WeekdayName] | DimDate[WeekdayNumber] |
| DimDate[QuarterLabel] | DimDate[Quarter] |

---

## Step 6: Create the Measures Table

1. **Modeling** tab → **New Table**
2. Enter exactly: `_Measures = {0}` → press **Enter**
3. In the **Fields** pane, right-click `_Measures` → **Hide in report view**
4. Select `_Measures` in the Fields pane before creating each new measure,
   so all measures land in this table rather than in FactSales

All measures are defined in [`dax/DAX_Measures.dax`](../dax/DAX_Measures.dax).
See [`dax/DAX_Measures_Guide.md`](../dax/DAX_Measures_Guide.md) for expected
output values to use when validating each measure.

### Measure groups in DAX_Measures.dax

| Group | Measures |
|---|---|
| 1 — Executive KPIs | Total Revenue, Total Orders, Total Units Sold, Total Profit, Profit Margin %, Total Customers, Average Order Value, Total Shipping Revenue, Total Discount Amount, Return Rate % |
| 2 — Time-Series KPIs | Monthly Revenue, Previous Month Revenue, MoM Revenue Change, MoM Revenue Growth %, YTD Revenue, Previous Year Revenue, YoY Revenue Growth %, Cumulative Revenue, Monthly Profit, Previous Month Profit |
| 3 — Product & Category KPIs | Sales Contribution %, Profit Contribution %, Product Revenue Rank, Category Revenue Rank, Top 5 Products Revenue, Bottom 5 Products Revenue |
| 4 — Customer KPIs | Revenue per Customer, Repeat Customers, One-Time Customers, Repeat Customer Rate % |
| 5 — Discount KPIs | Discounted Orders, Discount Rate %, Profit Margin on Discounted Orders %, Profit Margin on Non-Discounted Orders %, Discount Margin Gap |
| 6 — Order Status KPIs | Returned Orders, Canceled Orders, Returned Revenue |

> **Important:** Group 1 measures all include `FactSales[IsCompleted] = TRUE()` as
> an internal filter. Revenue KPIs exclude returned and cancelled orders automatically —
> you do not need to add a slicer or filter to get correct totals.
>
> Group 6 measures (`Returned Revenue`, `Return Rate %`) intentionally look across
> **all** order statuses. They are designed for Page 5 order-health visuals and should
> not be placed on the same card visual as Group 1 KPIs without a clear label.

---

## Step 7: Format the Measures

After creating each measure, apply the format below in **Column tools → Format**.

| Measure | Format string | Example output |
|---|---|---|
| Total Revenue | `$#,##0` | $1,888,956 |
| Total Profit | `$#,##0` | $929,083 |
| Total Shipping Revenue | `$#,##0` | |
| Total Discount Amount | `$#,##0` | |
| Returned Revenue | `$#,##0` | |
| Average Order Value | `$#,##0.00` | $223.39 |
| Revenue per Customer | `$#,##0.00` | |
| Profit Margin % | `#0.0%` | 49.2% |
| MoM Revenue Growth % | `#0.0%` | |
| YoY Revenue Growth % | `#0.0%` | |
| Return Rate % | `#0.0%` | |
| Repeat Customer Rate % | `#0.0%` | |
| Discount Rate % | `#0.0%` | |
| Discount Margin Gap | `#0.0%` | |
| Profit Margin on Discounted Orders % | `#0.0%` | |
| Profit Margin on Non-Discounted Orders % | `#0.0%` | |
| Total Orders | Whole number | 8,456 |
| Total Customers | Whole number | 2,047 |
| Total Units Sold | Whole number | 17,840 |
| Repeat Customers | Whole number | |
| One-Time Customers | Whole number | |
| Returned Orders | Whole number | |
| Canceled Orders | Whole number | |
| Discounted Orders | Whole number | |
| MoM Revenue Change | `$#,##0;-$#,##0` | Use signed format so negative values show red |

---

## Step 8: Save the File

**File** → **Save As** → save as `Ecommerce_Sales_Intelligence.pbix` in the `powerbi/` folder.

---

## Verifying the Model

After completing all steps, place each measure on a **Card visual with no slicers active**
and confirm it matches the expected value. Full validation table is in
[`dax/DAX_Measures_Guide.md`](../dax/DAX_Measures_Guide.md).

| Measure | Expected value |
|---|---|
| Total Revenue | $1,888,955.83 |
| Total Profit | $929,083.36 |
| Profit Margin % | 49.2% |
| Total Orders | 8,456 |
| Total Customers | 2,047 |
| Total Units Sold | 17,840 |
| Average Order Value | $223.39 |
| Repeat Customer Rate % | 64.4% |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Total Revenue returns BLANK | FactSales → DimDate relationship inactive | Check Model view; confirm the relationship arrow exists and is active |
| YoY Growth % is BLANK for all of 2024 | No 2023 data in DimDate | Expected behaviour — the dataset starts Jan 2024 |
| Monthly Revenue returns the same value for every month | DimDate not marked as date table | Step 4 |
| Month axis sorts alphabetically | Sort-by-column not set | Step 5 |
| Slicers on DimCustomer[State] do not filter charts | Filter direction is bidirectional or wrong | Set to single direction → DimCustomer |
| Revenue includes returned/cancelled orders | Using a raw SUM instead of the provided measures | Replace with the Group 1 measures from DAX_Measures.dax, which include IsCompleted = TRUE() internally |
| BusinessInsights table is not in any visual | Correct — it is reference-only | Add it to a Table visual on Page 5 only; do not join it to the model |
