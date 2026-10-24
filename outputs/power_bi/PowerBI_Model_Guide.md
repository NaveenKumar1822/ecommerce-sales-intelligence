# Power BI Data Model Guide
## E-commerce Sales Intelligence

---

## Step 1: Import the CSV Files

1. Open **Power BI Desktop** → **Home** → **Get Data** → **Text/CSV**
2. Import each file in this order:
   - `FactSales.csv`
   - `DimDate.csv`
   - `DimCustomer.csv`
   - `DimProduct.csv`
   - `CustomerRFM.csv`
   - `DataQualityReport.csv` (optional reference)
   - `BusinessInsights.csv` (optional reference)

---

## Step 2: Validate Data Types in Power Query

Open **Transform Data** and set these column types:

### FactSales
| Column | Type |
|---|---|
| OrderID | Whole Number |
| CustomerID | Whole Number |
| ProductID | Whole Number |
| OrderDate | Date (format: yyyy-mm-dd) |
| Status | Text |
| PaymentMethod | Text |
| HasDiscount | True/False |
| Quantity | Whole Number |
| UnitPrice | Decimal Number |
| DiscountAmount | Decimal Number |
| GrossRevenue | Decimal Number |
| NetRevenue | Decimal Number |
| TotalCost | Decimal Number |
| Profit | Decimal Number |
| ShippingFee | Decimal Number |
| IsCompleted | True/False |
| IsReturned | True/False |
| IsCanceled | True/False |
| OrderYear | Whole Number |
| OrderQuarter | Whole Number |
| OrderMonthNum | Whole Number |

### DimDate
| Column | Type |
|---|---|
| Date | Date |
| Year | Whole Number |
| Quarter | Whole Number |
| MonthNumber | Whole Number |
| YearMonthSort | Whole Number |
| WeekdayNumber | Whole Number |
| IsWeekend | True/False |

### DimCustomer
| Column | Type |
|---|---|
| CustomerID | Whole Number |
| SignupDate | Date |
| RecencyDays | Whole Number |
| Frequency | Whole Number |
| MonetaryValue | Decimal Number |

### DimProduct
| Column | Type |
|---|---|
| ProductID | Whole Number |
| ListPrice | Decimal Number |
| UnitCost | Decimal Number |
| GrossMarginPct | Decimal Number |

---

## Step 3: Create Relationships

In **Model view**, create these relationships (drag the key column to match):

| From Table.Column | To Table.Column | Cardinality | Direction | Active |
|---|---|---|---|---|
| FactSales.OrderDate | DimDate.Date | Many:1 | Single (→ Fact) | ✅ Yes |
| FactSales.CustomerID | DimCustomer.CustomerID | Many:1 | Single (→ Fact) | ✅ Yes |
| FactSales.ProductID | DimProduct.ProductID | Many:1 | Single (→ Fact) | ✅ Yes |
| CustomerRFM.CustomerID | DimCustomer.CustomerID | 1:1 | Single | ✅ Yes |

**Star Schema Diagram:**

```
           DimDate
              │
              │ 1:*
              │
DimCustomer ──┼── FactSales ──── DimProduct
              │
              │ 1:1
              │
         CustomerRFM
```

### Important Notes

- **Single filter direction only** for FactSales relationships — this prevents
  ambiguous filter paths and maintains correct aggregation behaviour.
- CustomerRFM is a 1:1 extension of DimCustomer. Only use it for RFM segment
  visuals; all revenue KPIs come from FactSales.
- No SalesTarget table is in this package (no target file was provided).
  If you receive targets later, add a `SalesTarget` table at Month × Category
  grain and relate it to DimDate[YearMonth] using an inactive relationship,
  then activate it with `USERELATIONSHIP` in target DAX measures.

---

## Step 4: Mark DimDate as the Date Table

1. Right-click `DimDate` in the Fields pane → **Mark as Date Table**
2. Select the `Date` column as the date key
3. Power BI will validate the date range and enable time-intelligence functions

---

## Step 5: Sort Columns Correctly

Set these "Sort by Column" assignments (Modeling → Sort by Column):

| Column | Sort By |
|---|---|
| DimDate.MonthName | DimDate.MonthNumber |
| DimDate.MonthNameShort | DimDate.MonthNumber |
| DimDate.WeekdayName | DimDate.WeekdayNumber |
| DimDate.YearMonth | DimDate.YearMonthSort |
| DimDate.QuarterLabel | DimDate.Quarter |

---

## Step 6: Create the Measures Table and Import DAX

1. **Modeling** → **New Table** → enter `_Measures = {0}` → Enter
2. Select `_Measures` in Fields pane
3. For each measure in `DAX_Measures.dax`, go to **New Measure** and paste

---

## Step 7: Format Measures

Apply these formats in the Properties pane after creating each measure:

| Measure | Format |
|---|---|
| Total Revenue, Total Profit, etc. | Currency ($), 0 decimals |
| Profit Margin %, MoM Growth %, YoY Growth % | Percentage, 1 decimal |
| Total Orders, Total Customers, Total Units | Whole Number |
| Average Order Value | Currency ($), 2 decimals |
| Discount Margin Gap | Percentage, 1 decimal |

---

## Step 8: Save the File

**File** → **Save As** → `Ecommerce_Sales_Intelligence.pbix`

---

## Relationship Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| YoY measures return blank | DimDate not marked as date table | Step 4 |
| Slicers don't filter charts | Wrong filter direction | Verify single-direction arrows |
| Revenue includes returns | IsCompleted not filtered | Use the provided DAX measures |
| Month axis not sorted | Sort by Column not set | Step 5 |

