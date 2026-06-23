import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Page configuration
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

#custom theme (Modern UI)
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #111827, #1f2937);
    color: white;
}

h1, h2, h3 {
    color: #f8fafc;
}

.stMetric {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.08);
}

.css-1d391kg {
    background-color: #111827;
}

hr {
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

#Load data
df = pd.read_csv("cleaned_superstore.csv")

#Title
st.title("📊 Superstore Sales & Profit Analytics Dashboard")


st.markdown("---")



#Sidebar filters
st.sidebar.header("🎛 Filters Panel")

region = st.sidebar.selectbox(
    "🌍 Select Region",
    ["All"] + sorted(df["Region"].unique())
)

category = st.sidebar.selectbox(
    "📦 Select Category",
    ["All"] + sorted(df["Category"].unique())
)

segment = st.sidebar.selectbox(
    "👥 Select Segment",
    ["All"] + sorted(df["Segment"].unique())
)

ship_mode = st.sidebar.selectbox(
    "🚚 Select Ship Mode",
    ["All"] + sorted(df["Ship Mode"].unique())
)

#Apply Filters
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if segment != "All":
    filtered_df = filtered_df[
        filtered_df["Segment"] == segment
    ]

if ship_mode != "All":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == ship_mode
    ]

#KPI section
st.markdown("## 📌 Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]
avg_discount = filtered_df["Discount"].mean()

avg_sales = filtered_df["Sales"].mean()
highest_sale = filtered_df["Sales"].max()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"{total_sales:,.0f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"{total_profit:,.0f}"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="📊 Avg Discount",
        value=f"{avg_discount:.2%}"
    )
    

col5, col6 = st.columns(2)

with col5:
    st.metric(
        label="📈 Average Sales",
        value=f"{avg_sales:,.0f}"
    )

with col6:
    st.metric(
        label="🚀 Highest Sale",
        value=f"{highest_sale:,.0f}"
    )

st.markdown("---")

#Dataset preview
st.markdown("## 📂 Dataset Preview")
st.dataframe(filtered_df, width="stretch")

st.markdown("---")

#Visualization section
st.markdown("## 📊 Data Visualizations")


col1, col2 = st.columns(2)

with col1:
    st.subheader("🥧 Sales Distribution by Category")

    sales_cat = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(4.5, 4.5))

    ax.pie(
        sales_cat,
        labels=sales_cat.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
    )

    ax.set_title(
        "Sales Distribution by Category",
        fontsize=12,
        pad=15
    )

    ax.axis("equal")

    st.pyplot(fig)
   

with col2:
    st.subheader("🌍 Profit by Region")

    profit_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(5,3))

    sns.barplot(
        data=profit_region,
        x="Region",
        y="Profit",
        ax=ax
    )

    ax.set_title(
        "Profit by Region",
        fontsize=12,
        pad=12
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Total Profit")

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    plt.tight_layout()

    st.pyplot(fig)
    
col3, col4 = st.columns(2)


with col3:
    st.subheader("🚚 Sales by Ship Mode")

    ship_sales = (
        filtered_df.groupby("Ship Mode")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(5,3))

    sns.barplot(
        data=ship_sales,
        x="Ship Mode",
        y="Sales",
        ax=ax
    )

    ax.set_title(
        "Sales by Ship Mode",
        fontsize=12,
        pad=12
    )

    ax.set_xlabel("Ship Mode")
    ax.set_ylabel("Total Sales")

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)
    
with col4:
    st.subheader("📉 Discount vs Profit Analysis")

    discount_profit = (
        filtered_df.groupby("Category")[["Discount", "Profit"]]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(5,3))

    discount_profit.set_index("Category").plot(
        kind="bar",
        ax=ax,
        width=0.7
    )

    ax.set_title("Average Discount vs Average Profit", fontsize=12)
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=0)
    plt.legend(["Discount", "Profit"])
    plt.tight_layout()

    st.pyplot(fig)
 


st.markdown("---")

#Top analysis
st.markdown("## 🏆 Top Business Insights")

col1, col2 = st.columns(2)


#Top customers
with col1:
    st.subheader("🏆 Top 10 Customers")

    top_customers = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        data=top_customers,
        x="Sales",
        y="Customer Name",
        ax=ax
    )

    ax.set_title("Top 10 Customers by Sales", fontsize=12, pad=12)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Customer Name")

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    plt.tight_layout()
    st.pyplot(fig)


#Top Sub-Categories by Sales
with col2:
    st.subheader("📦 Top Sub-Categories (Sales)")

    top_products = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        data=top_products,
        x="Sales",
        y="Sub-Category",
        ax=ax
    )

    ax.set_title("Top 10 Sub-Categories by Sales", fontsize=12, pad=12)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Sub-Category")

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    plt.tight_layout()
    st.pyplot(fig)


# Top Sub-Categories by Profit Data
top_profit = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

#Top Sub-Categories by Profit Chart
col_center1, col_center2, col_center3 = st.columns([1, 2, 1])

with col_center2:
    st.subheader("💰 Top Sub-Categories (Profit)")

    fig, ax = plt.subplots(figsize=(5,3))

    sns.barplot(
        data=top_profit,
        x="Profit",
        y="Sub-Category",
        ax=ax
    )

    ax.set_title(
        "Top 10 Sub-Categories by Profit",
        fontsize=12,
        pad=12
    )

    ax.set_xlabel("Total Profit")
    ax.set_ylabel("Sub-Category")

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.4
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.0f",
            padding=3
        )

    plt.tight_layout()
    st.pyplot(fig)
    
st.markdown("---")

left_col, right_col = st.columns([1, 1])



with left_col:
    st.markdown("## 🌎 Regional Sales Contribution")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(3,3))

    ax.pie(
        region_sales,
        labels=region_sales.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 1
        }
    )

    ax.axis("equal")

    plt.tight_layout()

    st.pyplot(fig)


with right_col:
    st.markdown("## 🧠 Advanced Insights")

    loss_orders = filtered_df[filtered_df["Profit"] < 0].shape[0]
    st.warning(f"⚠ Total Loss Making Orders: {loss_orders}")

    best_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    st.success(f"🏆 Most Profitable Category: {best_category}")

    #Download section
    st.markdown("### ⬇ Export Data")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv,
        file_name="superstore_dashboard_data.csv",
        mime="text/csv"
    )
    