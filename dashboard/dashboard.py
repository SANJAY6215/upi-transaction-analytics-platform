import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="UPI Analytics Platform",
    page_icon="💳",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM UI STYLE
# ---------------------------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */

.main{
background: linear-gradient(135deg,#0f172a,#020617);
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#020617,#0f172a);
padding-top:20px;
border-right:1px solid rgba(255,255,255,0.05);
}

/* SIDEBAR TITLE */

.sidebar-title{
font-size:20px;
font-weight:600;
color:white;
margin-bottom:10px;
}

/* NAVIGATION BUTTON STYLE */

div[role="radiogroup"] > label{
padding:12px 16px;
border-radius:10px;
margin-bottom:8px;
transition: all 0.3s ease;
cursor:pointer;
background:rgba(255,255,255,0.02);
font-size:15px;
}

/* HOVER ANIMATION */

div[role="radiogroup"] > label:hover{
background:rgba(0,255,213,0.08);
transform:translateX(6px);
box-shadow:0 0 10px rgba(0,255,213,0.25);
}

/* ACTIVE PAGE */

div[role="radiogroup"] > label[data-selected="true"]{
background:linear-gradient(90deg,#00ffd5,#00c3ff);
color:black;
font-weight:600;
}

/* KPI CARDS */

[data-testid="stMetric"]{
background:rgba(255,255,255,0.05);
padding:18px;
border-radius:12px;
box-shadow:0 0 10px rgba(0,255,213,0.2);
}

/* BUTTON */

.stButton>button{
background:linear-gradient(45deg,#00ffd5,#00c3ff);
color:black;
border-radius:8px;
font-weight:bold;
}

/* LIVE INDICATOR */

.live-indicator{
color:#00ff9c;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.title("💳 UPI Transaction Analytics Platform")

# ---------------------------------------------------
# LIVE AUTO REFRESH
# ---------------------------------------------------

refresh_interval = st.sidebar.slider(
"⚡ Auto Refresh Interval (seconds)",
5,
60,
10
)

refresh_count = st_autorefresh(
interval=refresh_interval * 1000,
limit=None,
key="dashboard_refresh"
)

st.sidebar.success("🟢 Live Dashboard Enabled")

st.markdown(
f"<p class='live-indicator'>🟢 Live Dashboard Running | Refresh Count: {refresh_count}</p>",
unsafe_allow_html=True
)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

engine = create_engine(st.secrets["DATABASE_URL"])

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data(ttl=10)
def load_data():

    df = pd.read_sql("SELECT * FROM fact_transactions", engine)

    df["transaction_time"] = pd.to_datetime(df["transaction_time"])
    df["hour"] = df["transaction_time"].dt.hour
    df["date"] = df["transaction_time"].dt.date

    return df

transactions = load_data()

# ---------------------------------------------------
# FRAUD LOGIC
# ---------------------------------------------------

fraud = transactions[
    (transactions["amount"] > 1000) |
    (transactions["status"] == "FAILED")
]

# ---------------------------------------------------
# SIDEBAR NAVIGATION (MODERN UI)
# ---------------------------------------------------

st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

menu = {
" Overview":"Overview",
" Fraud Analytics":"Fraud Analytics",
" Merchant Analytics":"Merchant Analytics",
" User Analytics":"User Analytics",
" Payment Analytics":"Payment Analytics",
" Raw Data":"Raw Data"
}

selection = st.sidebar.radio("", list(menu.keys()))
page = menu[selection]

# ---------------------------------------------------
# OVERVIEW PAGE
# ---------------------------------------------------

if page == "Overview":

    total_transactions = len(transactions)
    revenue = transactions["amount"].sum()

    success_rate = (
        len(transactions[transactions["status"]=="SUCCESS"])
        / total_transactions
    ) * 100

    trend_data = transactions.groupby("date").size()

    growth = trend_data.pct_change().mean() * 100 if len(trend_data) > 1 else 0

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Revenue",f"₹{revenue:,.0f}")
    col2.metric("Total Transactions",total_transactions)
    col3.metric("Growth Rate",f"{growth:.2f}%")
    col4.metric("Success Rate",f"{success_rate:.2f}%")

    st.divider()

    trend = trend_data.reset_index(name="transactions")

    fig = px.line(
        trend,
        x="date",
        y="transactions",
        markers=True,
        template="plotly_dark",
        title="Daily Transaction Trend"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# FRAUD ANALYTICS
# ---------------------------------------------------

elif page == "Fraud Analytics":

    fraud_score = (len(fraud) / len(transactions)) * 100
    suspicious_users = fraud["user_id"].nunique()

    col1,col2 = st.columns(2)

    col1.metric("Fraud Score",f"{fraud_score:.2f}%")
    col2.metric("Suspicious Users",suspicious_users)

    st.divider()

    # FIXED HEATMAP
    failed = transactions[transactions["status"]=="FAILED"].copy()

    failed["date"] = pd.to_datetime(failed["transaction_time"]).dt.date
    failed["hour"] = pd.to_datetime(failed["transaction_time"]).dt.hour

    heatmap_data = (
        failed.groupby(["date","hour"])
        .size()
        .reset_index(name="failed_count")
    )

    fig = px.density_heatmap(
        heatmap_data,
        x="hour",
        y="date",
        z="failed_count",
        color_continuous_scale="Turbo",
        template="plotly_dark",
        title="Failed Transactions Heatmap"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Fraud Transactions")

    st.dataframe(fraud,use_container_width=True)

# ---------------------------------------------------
# MERCHANT ANALYTICS
# ---------------------------------------------------

elif page == "Merchant Analytics":

    merchant_txn = (
        transactions.groupby("merchant_id")
        .size()
        .reset_index(name="transactions")
    )

    merchant_revenue = (
        transactions.groupby("merchant_id")["amount"]
        .sum()
        .reset_index()
    )

    top_merchants = merchant_txn.sort_values(
        "transactions",
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_merchants,
        x="merchant_id",
        y="transactions",
        color="transactions",
        template="plotly_dark",
        title="Top Merchants"
    )

    st.plotly_chart(fig1,use_container_width=True)

    fig2 = px.bar(
        merchant_revenue,
        x="merchant_id",
        y="amount",
        template="plotly_dark",
        title="Merchant Revenue"
    )

    st.plotly_chart(fig2,use_container_width=True)

# ---------------------------------------------------
# USER ANALYTICS
# ---------------------------------------------------

elif page == "User Analytics":

    active_users = transactions["user_id"].nunique()

    txn_frequency = (
        transactions.groupby("user_id")
        .size()
        .reset_index(name="transactions")
    )

    repeat_customers = txn_frequency[txn_frequency["transactions"] > 5]

    col1,col2,col3 = st.columns(3)

    col1.metric("Active Users",active_users)
    col2.metric("Avg Transaction Frequency",round(txn_frequency["transactions"].mean(),2))
    col3.metric("Repeat Customers",len(repeat_customers))

    fig = px.histogram(
        txn_frequency,
        x="transactions",
        template="plotly_dark",
        title="Transaction Frequency Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# PAYMENT ANALYTICS
# ---------------------------------------------------

elif page == "Payment Analytics":

    payment_share = (
        transactions.groupby("payment_method")
        .size()
        .reset_index(name="transactions")
    )

    fig1 = px.pie(
        payment_share,
        names="payment_method",
        values="transactions",
        hole=0.4,
        template="plotly_dark",
        title="Payment Method Share"
    )

    st.plotly_chart(fig1,use_container_width=True)

    hourly = (
        transactions.groupby("hour")
        .size()
        .reset_index(name="transactions")
    )

    fig2 = px.bar(
        hourly,
        x="hour",
        y="transactions",
        template="plotly_dark",
        title="Hourly Payment Distribution"
    )

    st.plotly_chart(fig2,use_container_width=True)

    peak_hour = hourly.sort_values(
        "transactions",
        ascending=False
    ).iloc[0]["hour"]

    st.metric("Peak Transaction Hour",f"{int(peak_hour)}:00")

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

elif page == "Raw Data":

    st.subheader("Transactions Dataset")

    st.dataframe(transactions,use_container_width=True,height=600)