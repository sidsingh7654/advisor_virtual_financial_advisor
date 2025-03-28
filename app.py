import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import joblib

# Load models
stage1_model = joblib.load('stage1_gbm.pkl')
stage2_model = joblib.load('stage2_gbm.pkl')

# App Title
st.title("AI-Powered Virtual Financial Advisor 💼📈")

# User Inputs
st.header("Enter Your Financial Profile")

income = st.number_input("Annual Income (in USD)", min_value=1000, max_value=1000000, value=50000, step=1000)
age = st.number_input("Age", min_value=18, max_value=100, value=30)
risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])

# Feature Processing Example
# Convert risk_tolerance to numeric
risk_map = {"Low": 0, "Medium": 1, "High": 2}
risk_tolerance_num = risk_map[risk_tolerance]

# Example Features Vector
features = np.array([[income, age, risk_tolerance_num]])

# Stage 1 Prediction - Asset Class Recommendation
asset_class = stage1_model.predict(features)[0]
st.subheader(f"Recommended Asset Class: {asset_class}")

# Stage 2 Prediction - Specific Product Recommendation
product = stage2_model.predict(features)[0]
st.subheader(f"Recommended Specific Product: {product}")

st.write("Note: This is a prototype recommendation. Please consult a certified financial advisor before making investment decisions.")
