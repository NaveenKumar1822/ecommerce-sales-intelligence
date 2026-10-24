"""
test_sales_analysis.py
Unit tests for the e-commerce sales analysis pipeline.
Run with: python -m pytest tests/ -v
"""
import sys
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_cleaning import clean_products, impute_unit_price, compute_line_metrics
from feature_engineering import compute_rfm, monthly_kpis, category_kpis
from validation import (assert_no_revenue_nulls, assert_positive_revenue,
                         assert_revenue_reconciliation, assert_fk_coverage)

# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_products():
    return pd.DataFrame({
        "product_id":   [1, 2, 3],
        "product_name": ["A", "B", "C"],
        "category":     [" Kitchen", "BEDDING ", "furniture"],
        "list_price":   [50.0, 100.0, 75.0],
        "unit_cost":    [20.0, 40.0, 30.0],
    })

@pytest.fixture
def sample_order_items():
    return pd.DataFrame({
        "order_id":       [1, 1, 2],
        "product_id":     [1, 2, 3],
        "quantity":       [1, 2, 1],
        "unit_price":     [50.0, None, 75.0],
        "discount_amount":[0.0, 5.0, 0.0],
    })

@pytest.fixture
def sample_fact():
    dates = pd.to_datetime(["2024-01-10","2024-02-15","2024-02-20",
                             "2024-03-05","2024-01-25"])
    return pd.DataFrame({
        "order_id":       [1,2,3,4,5],
        "customer_id":    [10,20,10,30,20],
        "order_date":     dates,
        "net_revenue":    [100.0, 200.0, 150.0, 80.0, 120.0],
        "profit":         [40.0, 80.0, 60.0, 30.0, 50.0],
        "quantity":       [1,2,1,1,2],
        "category":       ["Kitchen","Bedding","Kitchen","Decor","Bedding"],
        "order_year_month":["2024-01","2024-02","2024-02","2024-03","2024-01"],
    })


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestCleanProducts:
    def test_category_normalized(self, sample_products):
        result = clean_products(sample_products)
        assert result["category"].tolist() == ["Kitchen", "Bedding", "Furniture"]

    def test_original_not_mutated(self, sample_products):
        original_vals = sample_products["category"].tolist()
        _ = clean_products(sample_products)
        assert sample_products["category"].tolist() == original_vals


class TestImputeUnitPrice:
    def test_null_filled(self, sample_order_items, sample_products):
        cleaned_prods = clean_products(sample_products)
        result = impute_unit_price(sample_order_items, cleaned_prods)
        assert result["unit_price"].isnull().sum() == 0

    def test_imputed_value_matches_list_price(self, sample_order_items, sample_products):
        cleaned_prods = clean_products(sample_products)
        result = impute_unit_price(sample_order_items, cleaned_prods)
        imputed_row = result.loc[result["product_id"] == 2, "unit_price"].values[0]
        assert imputed_row == 100.0


class TestComputeLineMetrics:
    def test_gross_revenue_correct(self, sample_order_items, sample_products):
        cleaned_prods = clean_products(sample_products)
        oi = impute_unit_price(sample_order_items, cleaned_prods)
        result = compute_line_metrics(oi, cleaned_prods)
        # product_id=2: qty=2, unit_price=100, gross=200
        row2 = result.loc[result["product_id"] == 2].iloc[0]
        assert row2["gross_revenue"] == pytest.approx(200.0)

    def test_net_revenue_subtracts_discount(self, sample_order_items, sample_products):
        cleaned_prods = clean_products(sample_products)
        oi = impute_unit_price(sample_order_items, cleaned_prods)
        result = compute_line_metrics(oi, cleaned_prods)
        row2 = result.loc[result["product_id"] == 2].iloc[0]
        assert row2["net_revenue"] == pytest.approx(195.0)  # 200 - 5 discount

    def test_profit_positive_for_valid_products(self, sample_order_items, sample_products):
        cleaned_prods = clean_products(sample_products)
        oi = impute_unit_price(sample_order_items, cleaned_prods)
        result = compute_line_metrics(oi, cleaned_prods)
        assert (result["profit"] >= 0).all()


class TestComputeRFM:
    def test_segments_assigned(self, sample_fact):
        rfm = compute_rfm(sample_fact, snapshot_date=pd.Timestamp("2024-04-01"))
        assert "customer_segment" in rfm.columns
        assert rfm["customer_segment"].notna().all()

    def test_recency_days_positive(self, sample_fact):
        rfm = compute_rfm(sample_fact, snapshot_date=pd.Timestamp("2024-04-01"))
        assert (rfm["recency_days"] >= 0).all()

    def test_one_row_per_customer(self, sample_fact):
        rfm = compute_rfm(sample_fact, snapshot_date=pd.Timestamp("2024-04-01"))
        assert rfm["customer_id"].nunique() == rfm.shape[0]


class TestMonthlyKPIs:
    def test_margins_calculated(self, sample_fact):
        result = monthly_kpis(sample_fact)
        assert "margin_pct" in result.columns
        assert (result["margin_pct"] > 0).all()

    def test_sorted_by_year_month(self, sample_fact):
        result = monthly_kpis(sample_fact)
        assert result["order_year_month"].tolist() == sorted(result["order_year_month"].tolist())


class TestValidation:
    def test_revenue_reconciliation_pass(self):
        assert_revenue_reconciliation(1000.00, 1000.00)

    def test_revenue_reconciliation_fail(self):
        with pytest.raises(AssertionError):
            assert_revenue_reconciliation(1000.00, 999.00, tol=0.01)

    def test_fk_coverage_pass(self):
        fact_col = pd.Series([1, 2, 3])
        dim_col  = pd.Series([1, 2, 3, 4])
        assert_fk_coverage(fact_col, dim_col, "ProductID")

    def test_fk_coverage_fail(self):
        fact_col = pd.Series([1, 2, 99])
        dim_col  = pd.Series([1, 2, 3])
        with pytest.raises(AssertionError):
            assert_fk_coverage(fact_col, dim_col, "ProductID")
