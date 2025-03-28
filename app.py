import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------------
# Load Models
# -------------------------
stage1_model = joblib.load("stage1_gbm.pkl")
stage2_model = joblib.load("stage2_gbm.pkl")

# -------------------------
# Encoding Dictionaries
# -------------------------
risk_tolerance_map = {'Low': 0, 'Moderate': 1, 'High': 2}
investment_experience_map = {'None': 0, 'Beginner': 1, 'Intermediate': 2, 'Expert': 3}
market_volatility_tolerance_map = {'Low': 0, 'Medium': 1, 'High': 2}
goal_based_investing_map = {'No': 0, 'Yes': 1}
preferred_investment_type_map = {'Equity': 0, 'Debt': 1, 'Mutual Fund': 2}
short_term_goal_map = {'Short-Term Savings': 0, 'Vacation': 1}
mid_term_goal_map = {'Car Purchase': 0, 'Education Fund': 1, 'Home Renovation': 2}
long_term_goal_map = {'Wealth Accumulation': 0, 'Long-Term Security': 1}
investment_horizon_map = {'Short': 0, 'Medium': 1, 'Long': 2}

# -------------------------
# Streamlit App
# -------------------------
st.title("AI-Powered Virtual Financial Advisor")

st.header("Enter your Financial Profile")

# Inputs
Mthly_HH_Income = st.number_input("Monthly Household Income", value=10000)
Mthly_HH_Expense = st.number_input("Monthly Household Expense", value=5000)
Emi_or_Rent_Amt = st.number_input("EMI or Rent Amount", value=2000)
No_of_Earning_Members = st.number_input("Number of Earning Members", value=2)
Savings_Amount = st.number_input("Savings Amount", value=1000)
Debt_to_Income_Ratio = st.number_input("Debt to Income Ratio", value=0.3)

Investment_Horizon = st.selectbox("Investment Horizon", list(investment_horizon_map.keys()))
Risk_Tolerance = st.selectbox("Risk Tolerance", list(risk_tolerance_map.keys()))
Preferred_Investment_Type = st.selectbox("Preferred Investment Type", list(preferred_investment_type_map.keys()))
Investment_Experience = st.selectbox("Investment Experience", list(investment_experience_map.keys()))
Market_Volatility_Tolerance = st.selectbox("Market Volatility Tolerance", list(market_volatility_tolerance_map.keys()))
Short_Term_Goal = st.selectbox("Short Term Goal", list(short_term_goal_map.keys()))
Mid_Term_Goal = st.selectbox("Mid Term Goal", list(mid_term_goal_map.keys()))
Long_Term_Goal = st.selectbox("Long Term Goal", list(long_term_goal_map.keys()))
Goal_Based_Investing = st.selectbox("Goal Based Investing", list(goal_based_investing_map.keys()))

Adjusted_DTI = Debt_to_Income_Ratio * 100
Savings_Rate = (Savings_Amount / Mthly_HH_Income) * 100 if Mthly_HH_Income != 0 else 0
Disposable_Income = Mthly_HH_Income - Mthly_HH_Expense - Emi_or_Rent_Amt

if st.button("Predict Investment Class"):

    # -------------------------
    # Encode Categorical Inputs
    # -------------------------
    Investment_Horizon = investment_horizon_map[Investment_Horizon]
    Risk_Tolerance = risk_tolerance_map[Risk_Tolerance]
    Preferred_Investment_Type = preferred_investment_type_map[Preferred_Investment_Type]
    Investment_Experience = investment_experience_map[Investment_Experience]
    Market_Volatility_Tolerance = market_volatility_tolerance_map[Market_Volatility_Tolerance]
    Short_Term_Goal = short_term_goal_map[Short_Term_Goal]
    Mid_Term_Goal = mid_term_goal_map[Mid_Term_Goal]
    Long_Term_Goal = long_term_goal_map[Long_Term_Goal]
    Goal_Based_Investing = goal_based_investing_map[Goal_Based_Investing]

    # -------------------------
    # Stage 1 Prediction
    # -------------------------
    X1 = np.array([[Mthly_HH_Income, Mthly_HH_Expense, Emi_or_Rent_Amt, No_of_Earning_Members,
                    Savings_Amount, Investment_Horizon, Risk_Tolerance, Investment_Experience,
                    Market_Volatility_Tolerance, Short_Term_Goal, Mid_Term_Goal, Long_Term_Goal,
                    Goal_Based_Investing, Preferred_Investment_Type, Adjusted_DTI, Savings_Rate,
                    Disposable_Income, Debt_to_Income_Ratio]])

    asset_class = stage1_model.predict(X1)[0]
    st.success(f"Recommended Investment Class: {asset_class}")


     # ------------------ Stage 2 ------------------
    X_stage2 = input_data.copy()
    X_stage2["Preferred_Investment_Type"] = asset_class
    recommended_product = stage2_model.predict(X_stage2)[0]
    st.success(f"Recommended Product: {recommended_product}")

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

    # Filter Recommended Products
    df_recommend = df_stage3[
        (df_stage3['Product_Type'] == asset_class) &
        (df_stage3['Risk_Level'] == risk_tolerance) &
        (df_stage3['Investment_Horizon (Years)'] <= (5 if inv_horizon == "Long" else (3 if inv_horizon == "Mid" else 1)))
    ].sort_values(by='Expected_Return (%)', ascending=False).head(5)

    st.subheader("Top Recommended Products 🔥")
    st.dataframe(df_recommend.reset_index(drop=True))
