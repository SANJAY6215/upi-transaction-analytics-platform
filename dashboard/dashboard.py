import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="UPI Transaction Analytics",
    page_icon="💳",
    layout="wide"
)

# -------------------------------
# Custom Styling
# -------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #00ffd5;
}

[data-testid="stMetricLabel"] {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

st.title("💳 UPI Transaction Analytics Dashboard")

# -------------------------------
# Database Connection
# -------------------------------

engine = create_engine(
    "postgresql://upi_user:upi_password@localhost:5432/upi_analytics"
)

transactions = pd.read_sql("SELECT * FROM fact_transactions", engine)

# -------------------------------
# Fraud Detection Logic
# -------------------------------

fraud = transactions[
    (transactions["amount"] > 1000) |
    (transactions["status"] == "FAILED")
]

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("Filters")

status_filter = st.sidebar.selectbox(
    "Transaction Status",
    ["All"] + list(transactions["status"].unique())
)

if status_filter != "All":
    transactions = transactions[transactions["status"] == status_filter]

# -------------------------------
# KPI Metrics
# -------------------------------

total_transactions = len(transactions)
total_amount = transactions["amount"].sum()
fraud_count = len(fraud)
unique_users = transactions["user_id"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", total_transactions)
col2.metric("Total Amount", f"₹{total_amount:,.2f}")
col3.metric("Fraud Transactions", fraud_count)
col4.metric("Unique Users", unique_users)

st.markdown("---")

# -------------------------------
# Charts Row 1
# -------------------------------

col1, col2 = st.columns(2)

# Payment Method Chart
payment_chart = transactions.groupby("payment_method").size().reset_index(name="count")

fig_payment = px.bar(
    payment_chart,
    x="payment_method",
    y="count",
    title="Payment Method Distribution",
    color="count"
)

fig_payment.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117"
)

col1.plotly_chart(fig_payment, use_container_width=True, key="payment_chart")


# Transaction Status Pie Chart
status_chart = transactions.groupby("status").size().reset_index(name="count")

fig_status = px.pie(
    status_chart,
    names="status",
    values="count",
    title="Transaction Status Distribution"
)

col2.plotly_chart(fig_status, use_container_width=True, key="status_chart")

st.markdown("---")

# -------------------------------
# Top Merchants Chart
# -------------------------------

merchant_chart = (
    transactions.groupby("merchant_id")
    .size()
    .reset_index(name="transactions")
    .sort_values("transactions", ascending=False)
    .head(10)
)

fig_merchants = px.bar(
    merchant_chart,
    x="merchant_id",
    y="transactions",
    title="Top 10 Merchants by Transactions",
    color="transactions"
)

fig_merchants.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117"
)

st.plotly_chart(fig_merchants, use_container_width=True, key="merchant_chart")

st.markdown("---")

# -------------------------------
# Transaction Trend
# -------------------------------

st.subheader("📈 Transaction Trend")

transactions["transaction_time"] = pd.to_datetime(
    transactions["transaction_time"]
)

trend = transactions.groupby(
    transactions["transaction_time"].dt.date
).size().reset_index(name="transactions")

fig_trend = px.line(
    trend,
    x="transaction_time",
    y="transactions",
    title="Daily Transactions Trend"
)

st.plotly_chart(fig_trend, use_container_width=True, key="trend_chart")

st.markdown("---")

# -------------------------------
# Fraud Transactions Table
# -------------------------------

st.subheader("🚨 Fraud Transactions")

if fraud.empty:
    st.success("No fraud transactions detected")
else:
    st.dataframe(fraud, use_container_width=True, height=400)