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
