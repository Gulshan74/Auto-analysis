# import streamlit as st
# import pandas as pd
# import requests

# st.title("📊 Business Analytics Dashboard")

# # Set the FastAPI Backend URL (use your deployed URL)
# BACKEND_URL = "https://auto-analysis-avbw.onrender.com"

# try:
#     # Fetch data from the CSV endpoint
#     response = requests.get(f"{BACKEND_URL}/get-sales-csv")
#     response.raise_for_status()
#     data = response.json()
    
#     if "data" in data and isinstance(data["data"], list):
#         # Convert the JSON data to DataFrame.
#         df = pd.DataFrame(data["data"], columns=["Date", "Product", "Revenue", "Cost", "Profit"])
        
#         # Display the DataFrame
#         st.dataframe(df)
        
#         # Plot Revenue trend (ensure the Date column is parsed correctly if needed)
#         st.subheader("📈 Revenue Trend")
#         # Optionally convert "Date" to datetime if needed:
#         # df["Date"] = pd.to_datetime(df["Date"])
#         st.line_chart(df.set_index("Date")["Revenue"])
#     else:
#         st.error("⚠️ The API response does not contain the expected 'data' key.")
# except requests.exceptions.RequestException as e:
#     st.error(f"⚠️ Error fetching data from API: {e}")
# except Exception as e:
#     st.error(f"⚠️ An unexpected error occurred: {e}")













import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Update this URL to your deployed backend URL
BACKEND_URL = "https://auto-analysis-avbw.onrender.com"

# --- Authentication UI ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login_ui():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        response = requests.post(f"{BACKEND_URL}/login/", params={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Invalid credentials")

def signup_ui():
    st.sidebar.title("Sign Up")
    username = st.sidebar.text_input("New Username", key="signup_username")
    password = st.sidebar.text_input("New Password", type="password", key="signup_password")
    if st.sidebar.button("Sign Up"):
        response = requests.post(f"{BACKEND_URL}/signup/", params={"username": username, "password": password})
        if response.status_code == 200:
            st.sidebar.success("Account created! Please log in.")
        else:
            st.sidebar.error(response.json().get("detail", "Error during sign up"))

if not st.session_state["authenticated"]:
    auth_choice = st.sidebar.radio("Choose", ["Login", "Sign Up"], key="auth_choice")
    if auth_choice == "Login":
        login_ui()
    else:
        signup_ui()
    st.stop()

st.sidebar.write(f"Logged in as: {st.session_state.get('username')}")

# --- Main Dashboard ---
st.title("📊 Business Analytics Dashboard")
st.write("Upload your dataset (CSV or Excel) for dynamic analysis:")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state["df"] = df
        st.success("File uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

if "df" in st.session_state:
    df = st.session_state["df"]
    st.dataframe(df.head())

    # Dynamic column detection
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    st.sidebar.subheader("Data Columns")
    st.sidebar.write("Numeric:", numeric_cols)
    st.sidebar.write("Categorical:", categorical_cols)

    # Suggest available charts based on data types
    available_charts = []
    if numeric_cols:
        available_charts.extend(["Line Chart", "Bar Chart", "Histogram"])
    if numeric_cols and len(numeric_cols) >= 2:
        available_charts.append("Scatter Plot")
    if categorical_cols:
        available_charts.append("Pie Chart")

    analysis_options = st.sidebar.multiselect("Select chart types", available_charts, default=available_charts[0] if available_charts else None)

    st.subheader("Analysis Results")
    st.write("### Summary Statistics")
    st.dataframe(df.describe(include="all"))

    if "Line Chart" in analysis_options and numeric_cols:
        st.write("#### Line Chart")
        x_axis = st.selectbox("Select X-axis", options=df.columns, key="line_x")
        y_axis = st.selectbox("Select Y-axis", options=numeric_cols, key="line_y")
        fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        st.plotly_chart(fig, use_container_width=True)

    if "Bar Chart" in analysis_options and numeric_cols:
        st.write("#### Bar Chart")
        x_axis = st.selectbox("Select X-axis for bar chart", options=df.columns, key="bar_x")
        y_axis = st.selectbox("Select Y-axis for bar chart", options=numeric_cols, key="bar_y")
        fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
        st.plotly_chart(fig, use_container_width=True)

    if "Scatter Plot" in analysis_options and len(numeric_cols) >= 2:
        st.write("#### Scatter Plot")
        x_axis = st.selectbox("Select X-axis for scatter", options=numeric_cols, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis for scatter", options=[col for col in numeric_cols if col != x_axis], key="scatter_y")
        fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot", hover_data=df.columns)
        st.plotly_chart(fig, use_container_width=True)

    if "Histogram" in analysis_options and numeric_cols:
        st.write("#### Histogram")
        selected_col = st.selectbox("Select column for histogram", options=numeric_cols, key="hist_col")
        fig = px.histogram(df, x=selected_col, title="Histogram")
        st.plotly_chart(fig, use_container_width=True)

    if "Pie Chart" in analysis_options and categorical_cols:
        st.write("#### Pie Chart")
        selected_col = st.selectbox("Select column for pie chart", options=categorical_cols, key="pie_col")
        fig = px.pie(df, names=selected_col, title="Pie Chart")
        st.plotly_chart(fig, use_container_width=True)

# Advanced: Predictive Analytics
if st.button("Show Revenue Prediction"):
    response = requests.get(f"{BACKEND_URL}/predict/")
    if response.status_code == 200:
        pred = response.json().get("predicted_revenue")
        st.success(f"Predicted Revenue for tomorrow: {pred:.2f}")
    else:
        st.error("Prediction error")

