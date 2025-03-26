import streamlit as st
import pandas as pd


def sidebar_main(country: pd.Series, group: pd.Series, methodology: pd.Series) -> tuple:
    """Sidebar for the main page
    Returns:
        tuple: selected_countries, selected_group, selected_methods
    """
    with st.sidebar:
        st.sidebar.title("Filters")

        country_options = sorted(country.unique())
        method_options = sorted(methodology.unique())
        group_options = sorted(group.unique())

        selected_countries = st.sidebar.multiselect(
            "Countries", country_options, placeholder="All countries"
        )

        selected_group = st.sidebar.multiselect(
            "Reporting group", group_options, max_selections=1, placeholder="All groups"
        )

        selected_methods = st.sidebar.multiselect(
            "Methodologies", method_options, placeholder="All methodologies"
        )
    return selected_countries, selected_group, selected_methods


def display_demo_table(agg_func, daily_df, targets_df):
    
    def callback_func():
        # if there is no selection, select the previous option
        if not st.session_state[agg_func.__name__]:
            st.session_state[agg_func.__name__] = "%"

    options = ["%", "Abs", "Deviation"]
    selection = st.segmented_control(
        label=agg_func.__name__,
        options=options,
        selection_mode="single",
        default="%",
        key=agg_func.__name__,
        label_visibility="collapsed",
        on_change=callback_func,
    )

    col_format = None
    if selection in ["%", "Deviation"]:
        col_format = "%f %%"

    if selection:
        agg_df = agg_func(daily_df, targets_df, selection)
        st.dataframe(
            agg_df,
            hide_index=True,
            column_config={
                "Country_Label": st.column_config.TextColumn(
                    label="Country", pinned=True
                ),
                "Methodology": st.column_config.TextColumn(),
                "Completes": st.column_config.TextColumn(),
                "18-29": st.column_config.NumberColumn(format=col_format),
                "30-44": st.column_config.NumberColumn(format=col_format),
                "45-54": st.column_config.NumberColumn(format=col_format),
                "55+": st.column_config.NumberColumn(format=col_format),
                "Male": st.column_config.NumberColumn(format=col_format),
                "Female": st.column_config.NumberColumn(format=col_format),
                "Education I": st.column_config.NumberColumn(format=col_format),
                "Education II": st.column_config.NumberColumn(format=col_format),
                "Education III": st.column_config.NumberColumn(format=col_format),
            },
        )

def date_filter_change_callback():
    # if there is no selection, select the previous option
    if not st.session_state["date_filter"]:
        st.session_state["date_filter"] = "1d"
