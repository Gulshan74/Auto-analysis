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
import requests

# Initialize session state variables for authentication
if "users" not in st.session_state:
    st.session_state.users = {}  # A dictionary to store user credentials (username: password)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        # Check if the username exists and password matches
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.sidebar.success("Logged in!")
        else:
            st.sidebar.error("Invalid credentials!")

def signup():
    st.sidebar.title("Sign Up")
    new_username = st.sidebar.text_input("New Username", key="signup_username")
    new_password = st.sidebar.text_input("New Password", type="password", key="signup_password")
    if st.sidebar.button("Sign Up"):
        if new_username and new_password:
            if new_username in st.session_state.users:
                st.sidebar.error("User already exists!")
            else:
                st.session_state.users[new_username] = new_password
                st.sidebar.success("User created! Please switch to Login to access the dashboard.")
        else:
            st.sidebar.error("Please enter both username and password.")

# Let user choose to Login or Sign Up if not logged in
if not st.session_state.logged_in:
    auth_option = st.sidebar.selectbox("Select an option", ["Login", "Sign Up"], key="auth_option")
    if auth_option == "Login":
        login()
    else:
        signup()
    st.stop()

# --- Main Dashboard ---
st.title("📊 Business Analytics Dashboard")

# File uploader for dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Preview:")
        st.dataframe(df.head())
        st.session_state.df = df  # Store for further analysis
    except Exception as e:
        st.error(f"Error reading file: {e}")

# If no file is uploaded, fallback to backend data fetching
if "df" not in st.session_state:
    st.info("No file uploaded; fetching default data from backend...")
    BACKEND_URL = "https://auto-analysis-avbw.onrender.com"
    try:
        response = requests.get(f"{BACKEND_URL}/get-sales-csv")
        response.raise_for_status()
        data = response.json()
        if "data" in data and isinstance(data["data"], list):
            df = pd.DataFrame(data["data"], columns=["Date", "Product", "Revenue", "Cost", "Profit"])
            st.dataframe(df)
            st.session_state.df = df
        else:
            st.error("Unexpected API response format.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

# If data is available, show analysis options
if "df" in st.session_state:
    df = st.session_state.df

    st.sidebar.subheader("Choose Analysis")
    analysis_options = st.sidebar.multiselect(
        "Select chart types to display:",
        options=["Line Chart", "Bar Chart", "Scatter Plot", "Histogram"],
        default=["Line Chart"]
    )

    st.subheader("Analysis Results")
    st.write("### Summary Statistics")
    st.dataframe(df.describe())

    if "Line Chart" in analysis_options:
        st.write("#### Line Chart")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            x_axis = st.selectbox("Select X-axis", options=df.columns, key="line_x")
            y_axis = st.selectbox("Select Y-axis", options=numeric_cols, key="line_y")
            st.line_chart(df.set_index(x_axis)[y_axis])
        else:
            st.write("No numeric columns for line chart.")

    if "Bar Chart" in analysis_options:
        st.write("#### Bar Chart")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            x_axis = st.selectbox("Select X-axis for bar chart", options=df.columns, key="bar_x")
            y_axis = st.selectbox("Select Y-axis for bar chart", options=numeric_cols, key="bar_y")
            st.bar_chart(df.set_index(x_axis)[y_axis])
        else:
            st.write("No numeric columns for bar chart.")

    if "Scatter Plot" in analysis_options:
        st.write("#### Scatter Plot")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Select X-axis for scatter", options=numeric_cols, key="scatter_x")
            y_axis = st.selectbox("Select Y-axis for scatter", options=[col for col in numeric_cols if col != x_axis], key="scatter_y")
            import altair as alt
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=x_axis,
                y=y_axis,
                tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("Not enough numeric columns for scatter plot.")

    if "Histogram" in analysis_options:
        st.write("#### Histogram")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Select column for histogram", options=numeric_cols, key="hist_col")
            import altair as alt
            chart = alt.Chart(df).mark_bar().encode(
                alt.X(selected_col, bin=True),
                y='count()'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No numeric columns for histogram.")
