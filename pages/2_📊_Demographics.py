import streamlit as st
from modules.style_helpers import add_header, global_page_style, custom_page_style
from data.data import get_excel_data, aggregate_demo_table
from modules.control_helpers import sidebar_main

# Set page configuration
st.set_page_config(page_title="Demographics", layout="wide", page_icon="📊")

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


options = ["%", "Abs", "Deviation"]
selection = st.segmented_control(
    label="cell_items_filter",
    options=options,
    selection_mode="single",
    default="%",
    key="segmented_control",
    label_visibility="collapsed",
)

col_format = None
if selection in ["%", "Deviation"]:
    col_format = "%f %%"

if selection:
    agg_df = aggregate_demo_table(daily_df, targets_df, selection)
    st.dataframe(
        agg_df,
        hide_index=True,
        column_config={
            "Country_Label": st.column_config.TextColumn(label="Country", pinned=True),
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

if __name__ == "__main__":
    global_page_style()
    custom_page_style("2_demographics.css")
