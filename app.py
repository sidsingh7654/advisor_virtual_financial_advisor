import streamlit as st
import pandas as pd
import numpy as np
import joblib
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# -----------------------------
# Load Stage 1 and Stage 2 Models
# -----------------------------
stage1_model = joblib.load("stage1_gbm.pkl")
stage2_model = joblib.load("stage2_gbm.pkl")

# -----------------------------
# Load Stage 3 Data
# -----------------------------
df_stage3 = pd.read_csv("Stage3_Dynamic_Products.csv")

# -----------------------------
# Stage 3 Recommendation Function
# -----------------------------
def recommend_products(product_type, customer_info, top_n=3):
    df_filtered = df_stage3[
        (df_stage3['Product_Type'] == product_type) &
        (df_stage3['Risk_Level'] == customer_info['Risk_Tolerance']) &
        (df_stage3['Investment_Horizon (Years)'] <= customer_info['Investment_Horizon'])
    ]

    if df_filtered.empty:
        return f"❌ No {product_type} products available for this customer profile."

    df_recommend = df_filtered.sort_values(by='Expected_Return (%)', ascending=False).head(top_n)

    return df_recommend[['Product_Name', 'Expected_Return (%)', 'Risk_Level', 'Volatility_Level']]

# -----------------------------
# Streamlit App
# -----------------------------
st.title("💸 AI-Powered Virtual Financial Advisor")

st.header("Step 1: Client Financial Inputs")

Mthly_HH_Income = st.number_input("Monthly Household Income", min_value=1000)
Mthly_HH_Expense = st.number_input("Monthly Household Expense", min_value=500)
Emi_or_Rent_Amt = st.number_input("EMI or Rent Amount", min_value=0)
No_of_Earning_Members = st.slider("No of Earning Members", 1, 10, 1)
Savings_Amount = st.number_input("Current Savings Amount", min_value=0)
Investment_Horizon = st.slider("Investment Horizon (Years)", 1, 30, 5)
Risk_Tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
Investment_Experience = st.selectbox("Investment Experience", ["Beginner", "Intermediate", "Advanced"])
Market_Volatility_Tolerance = st.selectbox("Market Volatility Tolerance", ["Low", "Medium", "High"])
Short_Term_Goal = st.number_input("Short Term Goal Amount", min_value=0)
Mid_Term_Goal = st.number_input("Mid Term Goal Amount", min_value=0)
Long_Term_Goal = st.number_input("Long Term Goal Amount", min_value=0)
Goal_Based_Investing = st.selectbox("Goal Based Investing", ["Yes", "No"])
Preferred_Investment_Type = st.selectbox("Preferred Investment Type", ["Equity", "Mutual Fund", "Debt"])

# Derived Features
Adjusted_DTI = (Emi_or_Rent_Amt / Mthly_HH_Income) if Mthly_HH_Income > 0 else 0
Savings_Rate = (Savings_Amount / Mthly_HH_Income) if Mthly_HH_Income > 0 else 0
Disposable_Income = Mthly_HH_Income - Mthly_HH_Expense - Emi_or_Rent_Amt
Debt_to_Income_Ratio = Emi_or_Rent_Amt / Mthly_HH_Income if Mthly_HH_Income > 0 else 0

if st.button("💡 Get Investment Recommendation"):
    # Stage 1
    X1 = pd.DataFrame([[Mthly_HH_Income, Mthly_HH_Expense, Emi_or_Rent_Amt, No_of_Earning_Members,
                        Savings_Amount, Investment_Horizon, Risk_Tolerance, Investment_Experience,
                        Market_Volatility_Tolerance, Short_Term_Goal, Mid_Term_Goal, Long_Term_Goal,
                        Goal_Based_Investing, Preferred_Investment_Type, Adjusted_DTI, Savings_Rate,
                        Disposable_Income, Debt_to_Income_Ratio]],
                      columns=['Mthly_HH_Income','Mthly_HH_Expense','Emi_or_Rent_Amt','No_of_Earning_Members',
                               'Savings_Amount','Investment_Horizon','Risk_Tolerance','Investment_Experience',
                               'Market_Volatility_Tolerance','Short_Term_Goal','Mid_Term_Goal','Long_Term_Goal',
                               'Goal_Based_Investing','Preferred_Investment_Type','Adjusted_DTI','Savings_Rate',
                               'Disposable_Income','Debt_to_Income_Ratio'])

    asset_class = stage1_model.predict(X1)[0]
    st.success(f"✅ Recommended Investment Asset Class: {asset_class}")

    # Stage 2
    product_allocation = stage2_model.predict(X1)[0]
    st.info(f"Recommended Allocation (Stage 2 Prediction): {product_allocation}")

    # Stage 3
    customer_info = {
        'Risk_Tolerance': Risk_Tolerance,
        'Investment_Horizon': Investment_Horizon
    }

    st.subheader("Stage 3: Recommended Products")

    for product_type in ["Equity", "Mutual Fund", "Debt"]:
        st.write(f"### 🟣 {product_type} Recommendations:")
        result = recommend_products(product_type, customer_info)
        st.write(result)

st.caption("Built by Siddharth's AI Advisor 🚀")
