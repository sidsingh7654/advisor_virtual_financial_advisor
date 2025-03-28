import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import requests
import joblib

# Load the models
stage1_model = joblib.load("stage1_gbm.pkl")
stage2_model = joblib.load("stage2_gbm.pkl")

st.set_page_config(page_title="AI-Powered Virtual Financial Advisor", layout="centered")

st.title("💰 AI-Powered Virtual Financial Advisor")

st.header("📋 User Financial Profile")

# Input fields for all Stage 1 features
Mthly_HH_Income = st.number_input("Monthly Household Income", min_value=0)
Mthly_HH_Expense = st.number_input("Monthly Household Expense", min_value=0)
Emi_or_Rent_Amt = st.number_input("EMI or Rent Amount", min_value=0)
No_of_Earning_Members = st.number_input("Number of Earning Members", min_value=0, step=1)
Savings_Amount = st.number_input("Current Savings Amount", min_value=0)
Investment_Horizon = st.selectbox("Investment Horizon (years)", [1, 3, 5, 10, 15, 20])
Risk_Tolerance = st.slider("Risk Tolerance (1 = Low, 5 = High)", 1, 5)
Investment_Experience = st.selectbox("Investment Experience (1 = None, 5 = Expert)", [1, 2, 3, 4, 5])
Market_Volatility_Tolerance = st.slider("Market Volatility Tolerance (1 = Low, 5 = High)", 1, 5)
Short_Term_Goal = st.number_input("Short Term Goal Amount", min_value=0)
Mid_Term_Goal = st.number_input("Mid Term Goal Amount", min_value=0)
Long_Term_Goal = st.number_input("Long Term Goal Amount", min_value=0)
Goal_Based_Investing = st.selectbox("Interested in Goal Based Investing?", ["Yes", "No"])
Preferred_Investment_Type = st.selectbox("Preferred Investment Type", ["Equity", "Mutual Fund", "Debt", "Gold", "Real Estate"])
Adjusted_DTI = st.number_input("Adjusted Debt-to-Income Ratio (%)", min_value=0.0, format="%.2f")
Savings_Rate = st.number_input("Savings Rate (%)", min_value=0.0, format="%.2f")
Disposable_Income = st.number_input("Disposable Income", min_value=0)
Debt_to_Income_Ratio = st.number_input("Debt-to-Income Ratio (%)", min_value=0.0, format="%.2f")

# Preprocess inputs
goal_investing = 1 if Goal_Based_Investing == "Yes" else 0
investment_type_map = {"Equity": 0, "Mutual Fund": 1, "Debt": 2, "Gold": 3, "Real Estate": 4}
investment_type_encoded = investment_type_map.get(Preferred_Investment_Type, 0)

# Arrange features in model-expected order
features = np.array([[
    Mthly_HH_Income,
    Mthly_HH_Expense,
    Emi_or_Rent_Amt,
    No_of_Earning_Members,
    Savings_Amount,
    Investment_Horizon,
    Risk_Tolerance,
    Investment_Experience,
    Market_Volatility_Tolerance,
    Short_Term_Goal,
    Mid_Term_Goal,
    Long_Term_Goal,
    goal_investing,
    investment_type_encoded,
    Adjusted_DTI,
    Savings_Rate,
    Disposable_Income,
    Debt_to_Income_Ratio
]])

if st.button("Predict Recommended Asset Class"):
    try:
        asset_class = stage1_model.predict(features)[0]
        st.success(f"Recommended Investment Asset Class: **{asset_class}**")




        # Example Stage 2: predict stock or mutual fund (placeholder for now)
        st.info("Now recommending specific products (Stage 2)...")
        stage2_prediction = stage2_model.predict(features)[0]
        st.success(f"Recommended Product: **{stage2_prediction}**")

    except Exception as e:
        st.error(f"Prediction failed. Please check inputs. Error: {e}")



  # ------------------ Stage 3 ------------------
    st.subheader("Stage 3: Product Recommendation")

    # Equity Products
    stock_list = ["RELIANCE.NS", "INFY.NS", "TCS.NS", "HDFCBANK.NS", "BAJFINANCE.NS"]
    stock_data = []

    for ticker in stock_list:
        stock = yf.Ticker(ticker)
        info = stock.info
        stock_data.append({
            "Product_ID": ticker,
            "Product_Type": "Equity",
            "Product_Name": info.get('longName', ''),
            "Category": "Stock",
            "Risk_Level": "High" if info.get('beta', 1) > 1 else "Medium",
            "Expected_Return (%)": round(info.get('forwardPE', 10), 2),
            "Investment_Horizon (Years)": 5,
            "Volatility_Level": "High" if info.get('beta', 1) > 1 else "Medium"
        })

    df_stocks = pd.DataFrame(stock_data)

    # Mutual Fund Products
    response = requests.get("https://www.amfiindia.com/spages/NAVAll.txt")
    data = response.text

    mf_data = []
    for line in data.split("\n"):
        tokens = line.strip().split(";")
        if len(tokens) > 5 and tokens[0].isdigit():
            mf_data.append({
                "Product_ID": tokens[0],
                "Product_Type": "Mutual Fund",
                "Product_Name": tokens[3],
                "Category": "General Mutual Fund",
                "Risk_Level": "Medium",
                "Expected_Return (%)": 8,
                "Investment_Horizon (Years)": 3,
                "Volatility_Level": "Medium"
            })

    df_mf = pd.DataFrame(mf_data)

    # Combine Products
    df_stage3 = pd.concat([df_stocks, df_mf], ignore_index=True)

    # --- Stage 3 Filtering ---
    selected_risk = "High" if Risk_Tolerance >= 4 else "Medium"
    selected_horizon = Investment_Horizon

    df_recommend = df_stage3[
        (df_stage3['Product_Type'] == Preferred_Investment_Type) &
        (df_stage3['Risk_Level'] == selected_risk) &
        (df_stage3['Investment_Horizon (Years)'] <= selected_horizon)
    ].sort_values(by='Expected_Return (%)', ascending=False).head(5)

    # --- Display ---
    st.subheader("Top Recommended Products 🔥")

    if not df_recommend.empty:
    st.dataframe(df_recommend.reset_index(drop=True))
    else:
    st.warning("No matching products found based on your preferences. Try adjusting risk or horizon.")
