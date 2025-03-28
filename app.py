import streamlit as st
import pandas as pd
import numpy as np
import pickle
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# --------------------------- Load Models ---------------------------
stage1_model = pickle.load(open("stage1_gbm.pkl", "rb"))
stage2_model = pickle.load(open("stage2_gbm.pkl", "rb"))

# --------------------------- Stage 1 Features ---------------------------
stage1_features = ['Mthly_HH_Income',
 'Mthly_HH_Expense',
 'Emi_or_Rent_Amt',
 'No_of_Earning_Members',
 'Savings_Amount',
 'Investment_Horizon',
 'Risk_Tolerance',
 'Investment_Experience',
 'Market_Volatility_Tolerance',
 'Short_Term_Goal',
 'Mid_Term_Goal',
 'Long_Term_Goal',
 'Goal_Based_Investing',
 'Preferred_Investment_Type',
 'Adjusted_DTI',
 'Savings_Rate',
 'Disposable_Income',
 'Debt_to_Income_Ratio']

# --------------------------- UI ---------------------------
st.title("AI-Powered Virtual Financial Advisor")
st.header("Stage 1: Asset Class Recommendation")

user_inputs = {}
for feature in stage1_features:
    user_inputs[feature] = st.number_input(f"Enter {feature}", value=0.0)

X1 = pd.DataFrame([user_inputs])

if st.button("Predict Asset Class"):
    asset_class = stage1_model.predict(X1)[0]
    st.success(f"Recommended Investment Asset Class: {asset_class}")

    # --------------------------- Stage 2 ---------------------------
    st.header("Stage 2: Recommend Specific Products")

    # Dummy feature vector for Stage 2 (replace with real mapping)
    stage2_features = pd.DataFrame([user_inputs])

    product_recommendation = stage2_model.predict(stage2_features)

    st.success(f"Recommended Product: {product_recommendation}")

    # --------------------------- Stage 3 ---------------------------
    st.header("Stage 3: Recommended Stocks and Mutual Funds")

    # Get Equity Data
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
            "Expected_Return (%)": round(info.get('forwardPE', 10),2),
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

    df_stage3 = pd.concat([df_stocks, df_mf], ignore_index=True)

    st.subheader("Recommended Stocks (Equity):")
    st.dataframe(df_stocks.head(5))

    st.subheader("Recommended Mutual Funds:")
    st.dataframe(df_mf.head(5))