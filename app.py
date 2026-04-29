import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Page Config
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    text-align: center;
    color: #2e7d32;
}
div[data-testid="metric-container"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>💰 Smart Expense Tracker Dashboard</h1>", unsafe_allow_html=True)

# Load Data
def load_data():
    try:
        df = pd.read_csv("data.csv")
    except:
        df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("➕ Add Transaction")

date_input = st.sidebar.date_input("Date", date.today())
type_input = st.sidebar.selectbox("Type", ["Income", "Expense"])
category_input = st.sidebar.selectbox(
    "Category",
    ["Salary", "Food", "Travel", "Shopping", "Bills", "Other"]
)
amount_input = st.sidebar.number_input("Amount", min_value=0)

if st.sidebar.button("Add Transaction"):
    new_data = pd.DataFrame({
        "Date": [date_input],
        "Type": [type_input],
        "Category": [category_input],
        "Amount": [amount_input]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("data.csv", index=False)
    st.success("✅ Transaction Added!")

# Summary
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("💵 Income", f"₹{income}")
col2.metric("💸 Expense", f"₹{expense}")
col3.metric("💰 Balance", f"₹{balance}")

# Table
st.subheader("📋 Transaction History")
st.dataframe(df, use_container_width=True)

# Delete Row
st.subheader("🗑 Delete Transaction")

if not df.empty:
    row_delete = st.number_input("Enter Row Number", min_value=0, max_value=len(df)-1, step=1)
    
    if st.button("Delete"):
        df = df.drop(row_delete).reset_index(drop=True)
        df.to_csv("data.csv", index=False)
        st.success("Deleted Successfully!")

# Charts Section
col4, col5 = st.columns(2)

# Bar Chart
with col4:
    st.subheader("📊 Expense by Category")
    expense_df = df[df["Type"] == "Expense"]

    if not expense_df.empty:
        category_sum = expense_df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        category_sum.plot(kind="bar", ax=ax)
        st.pyplot(fig)

# Pie Chart
with col5:
    st.subheader("🥧 Expense Share")

    if not expense_df.empty:
        fig2, ax2 = plt.subplots()
        category_sum.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        st.pyplot(fig2)

# Monthly Dashboard
st.subheader("📅 Monthly Expense Dashboard")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    monthly = df[df["Type"] == "Expense"].groupby("Month")["Amount"].sum()

    if not monthly.empty:
        fig3, ax3 = plt.subplots()
        monthly.plot(kind="line", marker="o", ax=ax3)
        st.pyplot(fig3)