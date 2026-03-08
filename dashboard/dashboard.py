import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    "postgresql://upi_user:upi_password@127.0.0.1:5432/upi_analytics"
)
st.title("UPI Transaction Analytics Dashboard")

# Load data
transactions = pd.read_sql("SELECT * FROM fact_transactions", engine)
users = pd.read_sql("SELECT * FROM dim_user", engine)
merchants = pd.read_sql("SELECT * FROM dim_merchant", engine)

# -----------------------------
# KPI Metrics
# -----------------------------

total_transactions = len(transactions)
total_amount = transactions["amount"].sum()
fraud_transactions = transactions["fraud_flag"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Amount", f"₹{total_amount:,.2f}")
col3.metric("Fraud Transactions", fraud_transactions)

# -----------------------------
# Transactions by Status
# -----------------------------

st.subheader("Transactions by Status")

status_counts = transactions["status"].value_counts()
st.bar_chart(status_counts)

# -----------------------------
# Top Merchants
# -----------------------------

st.subheader("Top Merchants by Transactions")

top_merchants = transactions["merchant_id"].value_counts().head(10)
st.bar_chart(top_merchants)

# -----------------------------
# Fraud Transactions
# -----------------------------

st.subheader("Fraud Transactions")

fraud_data = transactions[transactions["fraud_flag"] == True]

st.dataframe(fraud_data.head(20))