"""
data_cleaning.py
Reproducible cleaning pipeline for the e-commerce dataset.
"""
import pandas as pd
import numpy as np


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """Normalize category names: strip whitespace and apply title-case."""
    df = products.copy()
    df["category"] = df["category"].str.strip().str.title()
    return df


def impute_unit_price(order_items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Fill null unit_price values from the product's list_price."""
    df = order_items.copy()
    null_mask = df["unit_price"].isnull()
    price_map = products.set_index("product_id")["list_price"]
    df.loc[null_mask, "unit_price"] = df.loc[null_mask, "product_id"].map(price_map)
    remaining = df["unit_price"].isnull().sum()
    if remaining > 0:
        print(f"WARNING: {remaining} unit_price rows still null after impute")
    return df


def compute_line_metrics(order_items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Add gross_revenue, net_revenue, unit_cost, total_cost, profit to each order line."""
    df = order_items.copy()
    df["gross_revenue"] = df["unit_price"] * df["quantity"]
    df["net_revenue"]   = df["gross_revenue"] - df["discount_amount"]
    cost_map = products.set_index("product_id")["unit_cost"]
    df["unit_cost"]   = df["product_id"].map(cost_map)
    df["total_cost"]  = df["unit_cost"] * df["quantity"]
    df["profit"]      = df["net_revenue"] - df["total_cost"]
    return df


def build_fact_table(order_items, orders, products, customers, region_map=None):
    """Join all four tables into a single analytical fact table."""
    if region_map is None:
        region_map = {
            "CA":"West","OR":"West","WA":"West","NV":"West","AZ":"West",
            "TX":"South","FL":"South","GA":"South","NC":"South","VA":"South",
            "NY":"Northeast","PA":"Northeast","NJ":"Northeast","MA":"Northeast",
            "IL":"Midwest","OH":"Midwest","MI":"Midwest","IN":"Midwest",
        }
    fact = (
        order_items
        .merge(orders[["order_id","customer_id","order_date","status",
                        "payment_method","discount_code","shipping_fee"]],
               on="order_id", how="left")
        .merge(products[["product_id","product_name","category"]],
               on="product_id", how="left")
        .merge(customers[["customer_id","signup_date","state","acquisition_channel"]],
               on="customer_id", how="left")
    )

    fact["is_completed"] = fact["status"] == "completed"
    fact["is_returned"]  = fact["status"] == "returned"
    fact["is_canceled"]  = fact["status"] == "canceled"

    fact["order_year"]       = fact["order_date"].dt.year
    fact["order_quarter"]    = fact["order_date"].dt.quarter
    fact["order_month_num"]  = fact["order_date"].dt.month
    fact["order_month_name"] = fact["order_date"].dt.strftime("%b")
    fact["order_year_month"] = fact["order_date"].dt.to_period("M").astype(str)
    fact["order_weekday"]    = fact["order_date"].dt.day_name()
    fact["has_discount"]     = (fact["discount_amount"] > 0) | (fact["discount_code"].notna())
    fact["region"]           = fact["state"].map(region_map).fillna("Other")

    return fact
