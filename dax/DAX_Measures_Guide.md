# DAX Measures Guide
## E-commerce Sales Intelligence Dashboard

---

### Setup: Create a Measures Table

1. In Power BI Desktop → **Modeling** tab → **New Table**
2. Enter: `_Measures = {0}` and press Enter
3. Right-click the table in the Fields pane → **Hide**
4. Create all measures inside `_Measures` to keep the model organised

---

### How to Create a Measure

1. Click the `_Measures` table in the Fields pane
2. Go to **Modeling** → **New Measure**
3. Paste the DAX expression from `DAX_Measures.dax`
4. Press Enter → validate the result in a Card visual

---

### Validation Checklist

| Measure | Expected Value | Validation Visual |
|---|---|---|
| Total Revenue | $1,888,955.83 | Card (no filters) |
| Total Orders | 8,456 | Card (no filters) |
| Total Profit | $929,083.36 | Card (no filters) |
| Profit Margin % | 49.2% | Card (no filters) |
| Total Customers | 2,047 | Card (no filters) |
| Total Units Sold | 17,840 | Card (no filters) |
| Average Order Value | $223.39 | Card (no filters) |
| Repeat Customer Rate % | 64.4% | Card (no filters) |

---

### Measure Groups Explained

#### Group 1: Executive KPIs
All measures in this group filter to `IsCompleted = TRUE()` only, matching the
business rule that returns and cancellations do not count as realised revenue.

#### Group 2: Time-Series KPIs
These use `DATEADD` and `DATESYTD` and **require** a relationship from
`FactSales[OrderDate]` → `DimDate[Date]` to be active. Mark `DimDate` as
the date table first (right-click → Mark as Date Table → Date column).

**Important:** `YoY Revenue Growth %` returns BLANK for Jan–Dec 2024 because
there is no prior-year data. This is correct behaviour.

#### Group 3: Product & Category KPIs
`Sales Contribution %` uses `ALL(DimProduct)` to ignore product filters and
compute the share of total. When placed in a table or bar chart with
`DimProduct[ProductName]` on the axis, each row shows that product's share
of total revenue.

`Product Revenue Rank` returns 1 for the top-revenue product in the current
filter context. Use it as a visual-level filter (Rank ≤ 10) to build Top-10
product tables.

#### Group 4: Customer KPIs
`Repeat Customers` iterates over CustomerIDs in context and checks each one's
completed order count. Place it on a Card with no filters to get the total;
it will also respond to Region and Date slicers.

#### Group 5: Discount KPIs
`Discount Margin Gap` gives the percentage-point difference between
non-discounted and discounted order margins. A value of ~9.4 pp means
discounted orders are ~9.4 points less profitable.

---

### Common Errors

| Error | Cause | Fix |
|---|---|---|
| `[Total Revenue]` returns blank | Date relationship inactive | Activate the FactSales→DimDate relationship |
| `YoY Growth %` shows blank for 2024 | No 2023 data exists | Expected — add a tooltip explaining this |
| `Monthly Revenue` returns same value everywhere | DimDate not set as date table | Right-click DimDate → Mark as Date Table |
| `Repeat Customers` very slow | ADDCOLUMNS iterating large table | Add an index column to FactSales in Power Query |

---

### Filter Context Notes

- All executive KPI measures include `FactSales[IsCompleted] = TRUE()` internally,
  so they are safe to use with any slicer without accidental inclusion of returns.
- The `Return Rate %` and `Returned Revenue` measures intentionally look at
  *all* order statuses and ignore the IsCompleted filter.
- Slicers on `DimDate`, `DimProduct[Category]`, `DimCustomer[State]`, and
  `FactSales[PaymentMethod]` all work with every measure via cross-filtering.

