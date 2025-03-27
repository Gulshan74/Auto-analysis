import streamlit as st
import pandas as pd
import requests

st.title("📊 Business Analytics Dashboard")

# Fetch Data from API
response = requests.get("https://auto-analysis-avbw.onrender.com")
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data["data"], columns=[ "Date", "Product", "Revenue", "Cost", "Profit"])

# Display Data
st.dataframe(df)
st.line_chart(df["Revenue"])
