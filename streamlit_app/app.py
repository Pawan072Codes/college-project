import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Page config — must be first Streamlit command
st.set_page_config(page_title="Business Analytics Dashboard", layout="wide", page_icon="📊")

# Connect to database
engine = create_engine("postgresql://postgres:Pawan%409873@localhost:5432/business_analytics")

@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM sales_cleaned", engine)
    return df

df = load_data()

st.title("📊  Business Analytics Dashboard")
st.markdown("Interactive sales insights — powered by PostgreSQL, Python & AI")
# Sidebar filters
st.sidebar.header("🔍 Filters")

countries = sorted(df["country"].unique())
selected_countries = st.sidebar.multiselect("Select Country", countries, default=[])

if selected_countries:
    df = df[df["country"].isin(selected_countries)]

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["invoice_date"].min().date(), df["invoice_date"].max().date())
)

if len(date_range) == 2:
    df = df[(df["invoice_date"].dt.date >= date_range[0]) & (df["invoice_date"].dt.date <= date_range[1])]

# KPI Metrics Row
total_revenue = df["total_sales"].sum()
total_orders = df["invoice_no"].nunique()
total_customers = df["customer_id"].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("👥 Total Customers", f"{total_customers:,}")
col4.metric("🎯 Avg Order Value", f"£{avg_order_value:,.2f}")


st.markdown("---")

# Monthly Sales Trend
monthly = df.groupby(["year", "month"])["total_sales"].sum().reset_index()
monthly["period"] = monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2)

fig1 = px.line(monthly, x="period", y="total_sales", markers=True,
               title="Monthly Sales Trend", labels={"total_sales": "Total Sales (£)", "period": "Month"})
st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_sales = df.groupby("weekday")["total_sales"].sum().reindex(weekday_order).reset_index()
    fig2 = px.bar(weekday_sales, x="weekday", y="total_sales", title="Sales by Weekday",
                  labels={"total_sales": "Total Sales (£)"})
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    top_countries = df.groupby("country")["total_sales"].sum().sort_values(ascending=False).head(10).reset_index()
    fig3 = px.bar(top_countries, x="total_sales", y="country", orientation="h", title="Top 10 Countries",
                  labels={"total_sales": "Total Sales (£)"})
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("📋 Raw Data Explorer")

with st.expander("View filtered data"):
    st.dataframe(df.head(1000), use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data as CSV", csv, "filtered_sales_data.csv", "text/csv")