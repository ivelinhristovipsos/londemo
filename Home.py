import streamlit as st

from data.dummy_data import dummy_df, generate_reporting_groups

df = dummy_df()

# Set page configuration
st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")

# Sidebar navigation
st.sidebar.title("Filters")

# Sidebar filters
country_options = list(df["Country"].unique())
method_options = list(df["Methodology"].unique())

selected_countries = st.sidebar.multiselect(
    "Countries", country_options, placeholder="All countries"
)

reporting_groups = generate_reporting_groups(df)
selected_group = st.sidebar.multiselect(
    "Reporting group", list(reporting_groups.keys()), max_selections=1, placeholder="All groups"
)

selected_methods = st.sidebar.multiselect(
    "Methodologies", method_options, placeholder="All methodologies"
)


# Apply CSS to change multiselect options colors to blue
st.markdown(
    """
    <style>
        div[data-baseweb="select"] span {
            background-color: #5f5ff5 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Apply filters
if selected_group:
    df = reporting_groups["".join(selected_group)]
if selected_countries:
    df = df[df["Country"].isin(selected_countries)]
if selected_methods:
    df = df[df["Methodology"].isin(selected_methods)]

# Top-level metrics container
with st.container(border=True) as cont:

    options = ["1d", "7d", "14d", "max"]
    selection = st.segmented_control(
        label="date_filter",
        options=options,
        selection_mode="single",
        default="1d",
        key="segmented_control",
        label_visibility="collapsed",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.metric("Valid Completes", "17350", "+275 (0.75%)", border=True)
    with col2:
        with st.container():
            st.metric(
                "Response Rate", "23.2%", "(0.75%)", delta_color="inverse", border=True
            )
    with col3:
        with st.container():
            st.metric(
                "Sample Exhaustion",
                "65.1%",
                "(10.75%)",
                delta_color="inverse",
                border=True,
            )
    with col4:
        with st.container():
            st.metric(
                "Data Quality Issues",
                "75",
                "+5 (4.75%)",
                delta_color="inverse",
                border=True,
            )

# Display table with styled header
with st.container(border=True):
    st.markdown("Country Level Breakdown")
    st.dataframe(
        df.style.set_table_styles(
            [
                {
                    "selector": "thead th",
                    "props": [("background-color", "##03002e"), ("color", "white")],
                }
            ]
        ),
        use_container_width=True,
        column_config={
            "Response Rate": st.column_config.NumberColumn(format="plain"),
            "% Completion": st.column_config.ProgressColumn(
                min_value=0, max_value=100, format="plain"
            ),
        },
        hide_index=True,
    )
