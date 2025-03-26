import streamlit as st
from modules.style_helpers import add_header, global_page_style, custom_page_style
from data.data_helpers import (
    get_excel_data,
    aggregate_demo_age_table,
    aggregate_demo_gen_table,
    aggregate_demo_edu_table,
)
from modules.control_helpers import sidebar_main, display_demo_table

st.set_page_config(page_title="Demographics", layout="wide", page_icon="📊")



with st.spinner("Loading..."):
    add_header(
        "<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/> Fieldwork Progress Dashboard - Demographics",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
    )

    data_dict = get_excel_data("data/dummy_data.xlsx")
    daily_df = data_dict["daily_data"]
    targets_df = data_dict["targets"]

    selected_countries, selected_group, selected_methods = sidebar_main(
        daily_df["Country_Label"], daily_df["Group"], daily_df["Methodology"]
    )
    if selected_group:
        daily_df = daily_df[daily_df["Group"].isin(selected_group)]
    if selected_countries:
        daily_df = daily_df[daily_df["Country_Label"].isin(selected_countries)]
    if selected_methods:
        daily_df = daily_df[daily_df["Methodology"].isin(selected_methods)]
    
    st.divider()
    add_header("Age", 4)
    display_demo_table(aggregate_demo_age_table, daily_df, targets_df)
    st.divider()
    add_header("Gender", 4)
    display_demo_table(aggregate_demo_gen_table, daily_df, targets_df)
    st.divider()
    add_header("Education", 4)
    display_demo_table(aggregate_demo_edu_table, daily_df, targets_df)

if __name__ == "__main__":
    global_page_style()
    custom_page_style("2_demographics.css")
