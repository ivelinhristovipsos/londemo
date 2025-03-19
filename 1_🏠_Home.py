import pandas as pd
import streamlit as st

from data.dummy_data import dummy_df, raw_dummy_data
from modules.style_helpers import add_header, global_page_style

st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")

raw_df = raw_dummy_data()

add_header("Demo Dashboard", 2)

with st.sidebar:
    st.sidebar.title("Filters")

    country_options = sorted(raw_df["Country"].unique())
    method_options = sorted(raw_df["Methodology"].unique())
    group_options = sorted(raw_df["Group"].unique())

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
    back_days = None
    if selection in ["1d", "7d", "14d"]:
        back_days = int(selection[:-1])
        period_selection_mask = raw_df["Date"] >= raw_df["Date"].max() - pd.Timedelta(
            days=back_days
        )

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
            # calculate delta vs period bsed on selection:
            st.metric("Valid Completes", valid_completes, "+275 (mocked)", border=True)
    with col2:
        with st.container():
            rr_mean = round(raw_df["Response Rate"].mean(), 1)
            st.metric("Response Rate", f"{rr_mean} %", "-24%", border=True)
    with col3:
        with st.container():
            se_mean = raw_df["Sample Exhaustion"].mean()
            st.metric(
                "Sample Exhaustion",
                f"{round(se_mean, 1)} %",
                "(10.75%)",
                delta_color="inverse",
                border=True,
            )
    with col4:
        with st.container():
            dq_issues_mean = raw_df["Data Quality Issues"].sum()
            st.metric(
                "Data Quality Issues",
                dq_issues_mean,
                "+5 (4.75%)",
                delta_color="inverse",
                border=True,
            )

with st.container():
    add_header("Country Level Breakdown", 4)
    edited_df = st.dataframe(
        df,
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

if __name__ == "__main__":
    global_page_style()
