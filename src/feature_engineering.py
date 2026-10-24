"""
feature_engineering.py
Business metrics computed from the cleaned fact table.
"""
import pandas as pd
import numpy as np


def compute_rfm(completed: pd.DataFrame, snapshot_date=None) -> pd.DataFrame:
    """
    Compute RFM scores and segments from completed-order transactions.
    Returns one row per customer.
    """
    if snapshot_date is None:
        snapshot_date = completed["order_date"].max() + pd.Timedelta(days=1)

    cust = completed.groupby("customer_id").agg(
        total_revenue=("net_revenue", "sum"),
        order_count=("order_id", "nunique"),
        last_purchase=("order_date", "max"),
    ).reset_index()

    cust["recency_days"] = (snapshot_date - cust["last_purchase"]).dt.days

    def score_q(s, asc=True):
        labels = [1, 2, 3, 4, 5] if asc else [5, 4, 3, 2, 1]
        return pd.qcut(s.rank(method="first"), 5, labels=labels).astype(int)

    cust["r_score"] = score_q(cust["recency_days"], asc=False)
    cust["f_score"] = score_q(cust["order_count"],  asc=True)
    cust["m_score"] = score_q(cust["total_revenue"],asc=True)
    cust["rfm_score"] = cust["r_score"].astype(str) + cust["f_score"].astype(str) + cust["m_score"].astype(str)

    def segment(row):
        r, f, m = row.r_score, row.f_score, row.m_score
        if r >= 4 and f >= 4 and m >= 4: return "Champions"
        if r >= 3 and f >= 3:             return "Loyal Customers"
        if r >= 4 and f <= 2:             return "Recent Customers"
        if r >= 3 and m >= 3:             return "Potential Loyalists"
        if r <= 2 and f >= 3 and m >= 3: return "At Risk"
        if r <= 2 and f <= 2 and m <= 2: return "Lost"
        return "Needs Attention"

    cust["customer_segment"] = cust.apply(segment, axis=1)
    return cust


def monthly_kpis(completed: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        completed.groupby("order_year_month")
        .agg(revenue=("net_revenue","sum"), profit=("profit","sum"),
             orders=("order_id","nunique"), units=("quantity","sum"))
        .reset_index().sort_values("order_year_month")
    )
    monthly["margin_pct"] = monthly["profit"] / monthly["revenue"] * 100
    monthly["mom_chg_pct"] = monthly["revenue"].pct_change() * 100
    return monthly


def category_kpis(completed: pd.DataFrame) -> pd.DataFrame:
    cat = (
        completed.groupby("category")
        .agg(revenue=("net_revenue","sum"), profit=("profit","sum"),
             units=("quantity","sum"), orders=("order_id","nunique"))
        .reset_index().sort_values("revenue", ascending=False)
    )
    cat["margin_pct"] = cat["profit"] / cat["revenue"] * 100
    cat["rev_share_pct"] = cat["revenue"] / cat["revenue"].sum() * 100
    return cat
