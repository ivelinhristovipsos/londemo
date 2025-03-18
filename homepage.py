import streamlit as st
import pandas as pd
import random
import plotly.express as px

# Set page configuration
st.set_page_config(page_title='Survey Dashboard', layout='wide')

# Sidebar navigation
st.sidebar.title("Filters")

data = {
    "Country": ["🇫🇷", "🇩🇪", "🇮🇹", "🇪🇸", "🇵🇱", "🇭🇺", "🇬🇷", "🇫🇮", "🇧🇬"],
    "Methodology": ["🌐Web", "🌐Web", "🧑‍🤝‍🧑F2F", "📞CATI", "🧑‍🤝‍🧑F2F", "🧑‍🤝‍🧑F2F", "📞CATI", "📞CATI", "📞CATI"],
    "Valid Completes": [753, 642, 580, 490, 520, 610, 450, 470, 430],
    "% Completion": [75, 68, 60, 55, 58, 62, 50, 52, 48],
    "Response Rate": [35.2, 32.5, 30.1, 28.7, 29.5, 31.0, 27.8, 28.2, 26.9],
    "Refusal Rate": ["-NA-", "12.3%", "10.5%", "9.8%", "11.0%", "10.2%", "9.5%", "10.0%", "8.7%"],
    "Sample Exhaustion": [98, 95, 92, 90, 91, 93, 89, 88, 87],
    "Data Quality Issues": [98, 85, 80, 75, 78, 82, 70, 72, 68]
}

df = pd.DataFrame(data)

# Reporting groups - random combinations of countries and methodologies
reporting_groups = {"All Groups": df}
for i in range(1, 4):  # Create 3 random groups
    random_countries = random.sample(list(df["Country"].unique()), random.randint(2, len(df["Country"].unique())))
    random_methods = random.sample(list(df["Methodology"].unique()), random.randint(1, len(df["Methodology"].unique())))
    group_name = f"Group {i}"
    reporting_groups[group_name] = df[(df["Country"].isin(random_countries)) & (df["Methodology"].isin(random_methods))]

# Filters with 'All' options
country_options = ["All Countries"] + list(df["Country"].unique())
method_options = ["All Methodologies"] + list(df["Methodology"].unique())
groups_options = list(reporting_groups.keys())

selected_countries = st.sidebar.multiselect("Select Countries", country_options, default="All Countries")
selected_methods = st.sidebar.multiselect("Select Methodologies", method_options, default="All Methodologies")
selected_group = st.sidebar.selectbox("Select Reporting Group", groups_options)

# Apply CSS to change multiselect options colors to blue
st.markdown(
    """
    <style>
        div[data-baseweb="select"] > div {
            background-color: #e0f7ff !important;
        }
        div[data-baseweb="select"] span {
            background-color: #007bff !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Apply filters
if selected_group != "All Groups":
    df = reporting_groups[selected_group]
if "All Countries" not in selected_countries:
    df = df[df["Country"].isin(selected_countries)]
if "All Methodologies" not in selected_methods:
    df = df[df["Methodology"].isin(selected_methods)]


# Top-level metrics container
with st.container() as cont:

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.metric("Valid Completes", "17350", "+275 (0.75%)", border=True)
    with col2:
        with st.container():
            st.metric("Response Rate", "23.2%", "(0.75%)", delta_color="inverse", border=True)
    with col3:
        with st.container():
            st.metric("Sample Exhaustion", "65.1%", "(10.75%)", delta_color="inverse", border=True)
    with col4:
        with st.container():
            st.metric("Data Quality Issues", "75", "+5 (4.75%)", delta_color="inverse", border=True)

# Display table with styled header

st.markdown("### Country Level Breakdown")
st.dataframe(df.style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '##03002e'), ('color', 'white')]}
]), use_container_width=True, column_config={
    "Response Rate": st.column_config.NumberColumn(format="plain"),
    "% Completion": st.column_config.ProgressColumn(
        min_value=0, max_value=100, format="plain"
    ),
})
