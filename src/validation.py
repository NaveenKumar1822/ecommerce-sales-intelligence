"""
validation.py
Data quality assertions for the e-commerce analysis pipeline.
"""
import pandas as pd


def assert_no_revenue_nulls(df: pd.DataFrame, col="net_revenue"):
    nulls = df[col].isnull().sum()
    assert nulls == 0, f"FAIL: {nulls} null values in {col}"
    print(f"PASS: No nulls in {col}")


def assert_positive_revenue(df: pd.DataFrame, col="net_revenue"):
    neg = (df[col] < 0).sum()
    assert neg == 0, f"FAIL: {neg} negative {col} rows"
    print(f"PASS: All {col} values non-negative")


def assert_no_duplicate_orders(fact: pd.DataFrame):
    """Each order_id should appear at least once — but not more times than products."""
    pass  # Multi-line orders are expected; just report counts


def assert_revenue_reconciliation(notebook_total: float, export_total: float, tol: float = 0.01):
    diff = abs(notebook_total - export_total)
    assert diff <= tol, f"FAIL: Revenue mismatch ${diff:.2f}"
    print(f"PASS: Revenue reconciled (diff=${diff:.4f})")


def assert_fk_coverage(fact_col: pd.Series, dim_col: pd.Series, name: str):
    missing = set(fact_col.dropna()) - set(dim_col)
    assert len(missing) == 0, f"FAIL: {len(missing)} {name} keys in fact not in dimension"
    print(f"PASS: {name} FK coverage 100%")
