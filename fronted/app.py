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
import altair as alt

# --- Authentication Section (if needed) ---
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

auth_mode = st.sidebar.radio("Choose Option", ["Login", "Sign Up"], key="auth_mode")
if auth_mode == "Sign Up":
    st.sidebar.title("Sign Up")
    new_username = st.sidebar.text_input("New Username", key="signup_username")
    new_password = st.sidebar.text_input("New Password", type="password", key="signup_password")
    if st.sidebar.button("Sign Up"):
        if new_username and new_password:
            if new_username in st.session_state.users:
                st.sidebar.error("User already exists!")
            else:
                st.session_state.users[new_username] = new_password
                st.sidebar.success("User created! Switch to Login.")
        else:
            st.sidebar.error("Enter both username and password.")
elif auth_mode == "Login":
    st.sidebar.title("Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        if login_username in st.session_state.users and st.session_state.users[login_username] == login_password:
            st.session_state.logged_in = True
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Invalid credentials!")

if not st.session_state.logged_in:
    st.stop()

# --- Main Dashboard Section ---
st.title("📊 Business Analytics Dashboard")
st.write("Upload your dataset (CSV or Excel) for dynamic analysis:")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Data Preview:")
        st.dataframe(df.head())
        
        # Detect column types dynamically
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        st.sidebar.subheader("Data Columns")
        st.sidebar.write("Numeric Columns:", numeric_cols)
        st.sidebar.write("Categorical Columns:", categorical_cols)
        
        # Provide dynamic analysis options based on detected columns
        available_charts = []
        if numeric_cols:
            available_charts.extend(["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"])
        if categorical_cols:
            available_charts.append("Pie Chart")
        
        analysis_options = st.sidebar.multiselect(
            "Select chart types to display:",
            options=available_charts,
            default=available_charts[0] if available_charts else None
        )
        
        st.subheader("Analysis Results")
        st.write("### Summary Statistics")
        st.dataframe(df.describe(include='all'))
        
        # Render each selected chart dynamically
        if "Line Chart" in analysis_options and numeric_cols:
            st.write("#### Line Chart")
            x_axis = st.selectbox("Select X-axis", options=df.columns, key="line_x")
            y_axis = st.selectbox("Select Y-axis", options=numeric_cols, key="line_y")
            st.line_chart(df.set_index(x_axis)[y_axis])
            
        if "Bar Chart" in analysis_options and numeric_cols:
            st.write("#### Bar Chart")
            x_axis = st.selectbox("Select X-axis for bar chart", options=df.columns, key="bar_x")
            y_axis = st.selectbox("Select Y-axis for bar chart", options=numeric_cols, key="bar_y")
            st.bar_chart(df.set_index(x_axis)[y_axis])
            
        if "Scatter Plot" in analysis_options and len(numeric_cols) >= 2:
            st.write("#### Scatter Plot")
            x_axis = st.selectbox("Select X-axis for scatter", options=numeric_cols, key="scatter_x")
            y_axis = st.selectbox("Select Y-axis for scatter", options=[col for col in numeric_cols if col != x_axis], key="scatter_y")
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=x_axis,
                y=y_axis,
                tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
            
        if "Histogram" in analysis_options and numeric_cols:
            st.write("#### Histogram")
            selected_col = st.selectbox("Select column for histogram", options=numeric_cols, key="hist_col")
            chart = alt.Chart(df).mark_bar().encode(
                alt.X(selected_col, bin=True),
                y='count()'
            )
            st.altair_chart(chart, use_container_width=True)
            
        if "Pie Chart" in analysis_options and categorical_cols:
            st.write("#### Pie Chart")
            selected_col = st.selectbox("Select column for pie chart", options=categorical_cols, key="pie_col")
            pie_data = df[selected_col].value_counts().reset_index()
            pie_data.columns = [selected_col, "Count"]
            chart = alt.Chart(pie_data).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field=selected_col, type="nominal"),
                tooltip=[selected_col, "Count"]
            )
            st.altair_chart(chart, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a dataset to begin analysis.")
