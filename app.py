import streamlit as st
import pandas as pd
import pickle
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# ----------------------- Load Stage 1 Model -------------------------
stage1_model = pickle.load(open("models/stage1_model.pkl", "rb"))

# ----------------------- Streamlit UI -------------------------------
st.title("AI-Powered Virtual Financial Advisor")
st.subheader("Personalized Investment Recommendation")

# ----------------------- Input Form -------------------------------
with st.form("customer_form"):
    st.write("### Enter your financial details")

    Mthly_HH_Income = st.number_input("Monthly Household Income", min_value=0)
    Mthly_HH_Expense = st.number_input("Monthly Household Expense", min_value=0)
    Emi_or_Rent_Amt = st.number_input("EMI or Rent Amount", min_value=0)
    No_of_Earning_Members = st.number_input("No. of Earning Members", min_value=0)
    Savings_Amount = st.number_input("Current Savings Amount", min_value=0)
    Investment_Horizon = st.slider("Investment Horizon (Years)", 1, 30, 5)

    Risk_Tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    Investment_Experience = st.selectbox("Investment Experience", ["Beginner", "Intermediate", "Expert"])
    Market_Volatility_Tolerance = st.selectbox("Market Volatility Tolerance", ["Low", "Medium", "High"])

    Short_Term_Goal = st.number_input("Short Term Goal Amount", min_value=0)
    Mid_Term_Goal = st.number_input("Mid Term Goal Amount", min_value=0)
    Long_Term_Goal = st.number_input("Long Term Goal Amount", min_value=0)

    Goal_Based_Investing = st.selectbox("Goal Based Investing", ["Yes", "No"])
    Preferred_Investment_Type = st.selectbox("Preferred Investment Type", ["Mutual Fund", "Equity", "Debt"])

    Adjusted_DTI = st.slider("Adjusted Debt-to-Income Ratio", 0.0, 1.0, 0.3)
    Savings_Rate = st.slider("Savings Rate", 0.0, 1.0, 0.2)
    Disposable_Income = st.number_input("Disposable Income", min_value=0)
    Debt_to_Income_Ratio = st.slider("Debt to Income Ratio", 0.0, 1.0, 0.4)

    submit = st.form_submit_button("Get Recommendation")

# ----------------------- Stage 1 Prediction -------------------------------
if submit:

    X_input = pd.DataFrame([{
        'Mthly_HH_Income': Mthly_HH_Income,
        'Mthly_HH_Expense': Mthly_HH_Expense,
        'Emi_or_Rent_Amt': Emi_or_Rent_Amt,
        'No_of_Earning_Members': No_of_Earning_Members,
        'Savings_Amount': Savings_Amount,
        'Investment_Horizon': Investment_Horizon,
        'Risk_Tolerance': Risk_Tolerance,
        'Investment_Experience': Investment_Experience,
        'Market_Volatility_Tolerance': Market_Volatility_Tolerance,
        'Short_Term_Goal': Short_Term_Goal,
        'Mid_Term_Goal': Mid_Term_Goal,
        'Long_Term_Goal': Long_Term_Goal,
        'Goal_Based_Investing': Goal_Based_Investing,
        'Preferred_Investment_Type': Preferred_Investment_Type,
        'Adjusted_DTI': Adjusted_DTI,
        'Savings_Rate': Savings_Rate,
        'Disposable_Income': Disposable_Income,
        'Debt_to_Income_Ratio': Debt_to_Income_Ratio
    }])

    asset_class = stage1_model.predict(X_input)[0]
    st.success(f"Recommended Asset Class: {asset_class}")

# ----------------------- Stage 3 Dynamic Recommendation -------------------------------

    # ---------------- STOCKS ----------------
    st.write("### Dynamic Recommendations")
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

    # ---------------- MUTUAL FUNDS ----------------
    url = "https://www.amfiindia.com/net-asset-value/nav-history"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get("https://www.amfiindia.com/spages/NAVAll.txt", headers=headers)
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

    # ---------------- COMBINE ----------------
    df_stage3 = pd.concat([df_stocks, df_mf], ignore_index=True)

    # ---------------- SHOW RECOMMENDATION ----------------
    if asset_class == "Equity":
        st.write(df_stocks[['Product_Name', 'Expected_Return (%)', 'Risk_Level', 'Volatility_Level']].head(5))
    elif asset_class == "Mutual Fund":
        st.write(df_mf[['Product_Name', 'Expected_Return (%)', 'Risk_Level', 'Volatility_Level']].head(5))
    else:
        st.warning("No specific recommendations found.")
