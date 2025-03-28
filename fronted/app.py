import streamlit as st
import pandas as pd
import requests

st.title("📊 Business Analytics Dashboard")

# Set the FastAPI Backend URL (use your deployed URL)
BACKEND_URL = "https://auto-analysis-avbw.onrender.com"

try:
    # Fetch data from the CSV endpoint
    response = requests.get(f"{BACKEND_URL}/get-sales-csv")
    response.raise_for_status()
    data = response.json()
    
    if "data" in data and isinstance(data["data"], list):
        # Convert the JSON data to DataFrame.
        df = pd.DataFrame(data["data"], columns=["Date", "Product", "Revenue", "Cost", "Profit"])
        
        # Display the DataFrame
        st.dataframe(df)
        
        # Plot Revenue trend (ensure the Date column is parsed correctly if needed)
        st.subheader("📈 Revenue Trend")
        # Optionally convert "Date" to datetime if needed:
        # df["Date"] = pd.to_datetime(df["Date"])
        st.line_chart(df.set_index("Date")["Revenue"])
    else:
        st.error("⚠️ The API response does not contain the expected 'data' key.")
except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Error fetching data from API: {e}")
except Exception as e:
    st.error(f"⚠️ An unexpected error occurred: {e}")
