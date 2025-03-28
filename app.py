import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load models
stage1_model = joblib.load("stage1_gbm.pkl")
stage2_model = joblib.load("stage2_gbm.pkl")

st.title("AI-Powered Virtual Financial Advisor")

st.header("Enter Your Financial Profile")

# Input fields
Mthly_HH_Income = st.number_input("Monthly Household Income")
Mthly_HH_Expense = st.number_input("Monthly Household Expense")
Emi_or_Rent_Amt = st.number_input("EMI or Rent Amount")
No_of_Earning_Members = st.number_input("Number of Earning Members", step=1)
Savings_Amount = st.number_input("Savings Amount")
Investment_Horizon = st.selectbox("Investment Horizon (Years)", [1, 3, 5, 10, 15, 20])
Risk_Tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
Investment_Experience = st.selectbox("Investment Experience", ["None", "Beginner", "Intermediate", "Expert"])
Market_Volatility_Tolerance = st.selectbox("Market Volatility Tolerance", ["Low", "Medium", "High"])
Short_Term_Goal = st.number_input("Short Term Goal Amount")
Mid_Term_Goal = st.number_input("Mid Term Goal Amount")
Long_Term_Goal = st.number_input("Long Term Goal Amount")
Goal_Based_Investing = st.selectbox("Do you prefer Goal Based Investing?", ["Yes", "No"])
Preferred_Investment_Type = st.selectbox("Preferred Investment Type", ["Equity", "Debt", "Mutual Fund", "ETF", "Others"])
Adjusted_DTI = st.number_input("Adjusted DTI")
Savings_Rate = st.number_input("Savings Rate")
Disposable_Income = st.number_input("Disposable Income")
Debt_to_Income_Ratio = st.number_input("Debt to Income Ratio")

if st.button("Get Recommendation"):

    # Create dataframe
    X1 = pd.DataFrame({
        'Mthly_HH_Income': [Mthly_HH_Income],
        'Mthly_HH_Expense': [Mthly_HH_Expense],
        'Emi_or_Rent_Amt': [Emi_or_Rent_Amt],
        'No_of_Earning_Members': [No_of_Earning_Members],
        'Savings_Amount': [Savings_Amount],
        'Investment_Horizon': [Investment_Horizon],
        'Risk_Tolerance': [Risk_Tolerance],
        'Investment_Experience': [Investment_Experience],
        'Market_Volatility_Tolerance': [Market_Volatility_Tolerance],
        'Short_Term_Goal': [Short_Term_Goal],
        'Mid_Term_Goal': [Mid_Term_Goal],
        'Long_Term_Goal': [Long_Term_Goal],
        'Goal_Based_Investing': [Goal_Based_Investing],
        'Preferred_Investment_Type': [Preferred_Investment_Type],
        'Adjusted_DTI': [Adjusted_DTI],
        'Savings_Rate': [Savings_Rate],
        'Disposable_Income': [Disposable_Income],
        'Debt_to_Income_Ratio': [Debt_to_Income_Ratio]
    })

    # Encode categorical
    for col in ['Risk_Tolerance', 'Investment_Experience', 'Market_Volatility_Tolerance', 'Goal_Based_Investing', 'Preferred_Investment_Type']:
        X1[col] = X1[col].astype('category').cat.codes

    # Stage 1 Prediction
    asset_class = stage1_model.predict(X1)[0]

    st.subheader(f"Recommended Asset Class: {asset_class}")

    # Stage 2 Prediction (Stock / MF)
    X2 = X1.copy()
    X2["Predicted_Asset"] = asset_class
    recommendation = stage2_model.predict(X2)[0]
    st.info(f"Recommended Product: {recommendation}")

    # ------------------ Stage 3 (Dynamic Product List) ------------------

    # Get Stock Data
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

    # Get Mutual Fund Data
    response = requests.get("https://www.amfiindia.com/spages/NAVAll.txt")
    data = response.text

    mf_data = []
    for line in data.split("\n"):
        tokens = line.strip().split(";")
        if len(tokens) > 5:
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

    # Combine Stage 3 Dataset
    df_stage3 = pd.concat([df_stocks, df_mf], ignore_index=True)

    # Filter Recommendations
    df_recommend = df_stage3[
        (df_stage3['Product_Type'] == asset_class) &
        (df_stage3['Risk_Level'] == Risk_Tolerance) &
        (df_stage3['Investment_Horizon (Years)'] <= Investment_Horizon)
    ].sort_values(by='Expected_Return (%)', ascending=False).head(5)

    st.subheader("Top Recommended Products 🔥")
    st.dataframe(df_recommend.reset_index(drop=True))
