import streamlit as st

from data.dummy_data import dummy_df, raw_dummy_data
import pandas as pd

raw_df = raw_dummy_data()

# Set page configuration
st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")

# Sidebar navigation
st.sidebar.title("Filters")



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

# Sidebar filters
country_options = list(raw_df["Country"].unique())
method_options = list(raw_df["Methodology"].unique())
group_options = list(raw_df["Group"].unique())

selected_countries = st.sidebar.multiselect(
    "Countries", country_options, placeholder="All countries"
)

selected_group = st.sidebar.multiselect(
    "Reporting group", group_options, max_selections=1, placeholder="All groups"
)

selected_methods = st.sidebar.multiselect(
    "Methodologies", method_options, placeholder="All methodologies"
)


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

    # LOGIC: 
    if selection in ["1d", "7d", "14d"]:
        back_days = int(selection[:-1])
        raw_df = raw_df[raw_df["Date"] >= raw_df["Date"].max() - pd.Timedelta(days=back_days)]
    

    # Apply filters
    if selected_group:
        raw_df = raw_df[raw_df["Group"].isin(selected_countries)]
    if selected_countries:
        raw_df = raw_df[raw_df["Country"].isin(selected_countries)]
    if selected_methods:
        raw_df = raw_df[raw_df["Methodology"].isin(selected_methods)]

    df = dummy_df(raw_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            valid_completes = raw_df["Valid Completes"].sum()
            st.metric("Valid Completes", valid_completes, "+275 (0.75%)", border=True)
    with col2:
        with st.container():
            st.metric(
                "Response Rate", f"{round(raw_df['Response Rate'].mean(),1)} %", "(0.75%)", delta_color="inverse", border=True
            )
    with col3:
        with st.container():
            st.metric(
                "Sample Exhaustion",
                f"{round(raw_df['Sample Exhaustion'].mean(),1)} %",
                "(10.75%)",
                delta_color="inverse",
                border=True
            )
    with col4:
        with st.container():
            st.metric(
                "Data Quality Issues",
                raw_df["Data Quality Issues"].sum(),
                "+5 (4.75%)",
                delta_color="inverse",
                border=True,
            )

# Display table with styled headerr
st.markdown("Country Level Breakdown")
edited_df = st.dataframe(
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
        "% Completion": st.column_config.ProgressColumn(
            min_value=0, max_value=100, format="%d%%"
        ),
        "Response Rate": st.column_config.NumberColumn(format="%d%%"),
        "Refusal Rate": st.column_config.NumberColumn(format="%d%%"),
        "Sample Exhaustion": st.column_config.NumberColumn(format="%d%%"),
        "Data Quality Issues": st.column_config.NumberColumn(format="plain"),
    },
    hide_index=True,
    # selection_mode="single-row",
    # key="data",
    # on_select="rerun",
)

