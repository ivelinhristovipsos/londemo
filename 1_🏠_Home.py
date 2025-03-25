import pandas as pd
import streamlit as st

from data.data import get_excel_data, aggregate_daily_data
from modules.style_helpers import add_header, apply_style_to_agg_data, custom_page_style

st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")

data_dict = get_excel_data("data/dummy_data.xlsx")
daily_df = data_dict["daily_data"]
targets_df = data_dict["targets"]


add_header("<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png'/> <br/> Fieldwork Progress Dashboard ", 1)

st.logo('https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg', icon_image='https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg')

with st.sidebar:
    st.sidebar.title("Filters")

    country_options = sorted(daily_df["Country_Label"].unique())
    method_options = sorted(daily_df["Methodology"].unique())
    group_options = sorted(daily_df["Group"].unique())

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
        period_selection_mask = daily_df["Date"] >= daily_df["Date"].max() - pd.Timedelta(
            days=back_days
        )
        daily_df = daily_df[period_selection_mask]

    st.text(f'{daily_df["Date"].dt.date.min()} - {daily_df["Date"].dt.date.max()}')

    # Apply filters
    if selected_group:
        daily_df = daily_df[daily_df["Group"].isin(selected_group)]
    if selected_countries:
        daily_df = daily_df[daily_df["Country_Label"].isin(selected_countries)]
    if selected_methods:
        daily_df = daily_df[daily_df["Methodology"].isin(selected_methods)]

    # st.table(daily_agg_df)
    col1, col2, col3, col4 = st.columns(4)
    
    
    with col1:
        with st.container():
            total_valid_completes = data_dict["daily_data"]["Valid Completes"].sum()
            filtered_valid_completes = daily_df["Valid Completes"].sum()
            filtered_percent = round(filtered_valid_completes / total_valid_completes * 100, 1)
            delta_display = f"{filtered_valid_completes} ({filtered_percent}%)" if back_days else None
            st.metric("Valid Completes", total_valid_completes, delta_display, border=True)
    with col2:
        with st.container():
            total_rr = round(total_valid_completes / data_dict["daily_data"]["Sample_Closed"].sum() * 100, 1)
            filtered_rr = round(daily_df["Valid Completes"].sum() / daily_df["Sample_Closed"].sum() * 100, 1)
            delta_rr = round(filtered_rr - total_rr, 1)
            delta_display = f"{delta_rr} ({filtered_rr}%)"  if back_days else None
            st.metric("Response Rate", f"{total_rr} %", delta_display, border=True)
    with col3:
        with st.container():
            total_se = round(data_dict["daily_data"]["Sample_Closed"].sum() / targets_df["Sample_Available"].sum() * 100, 1)
            filtered_se = round(daily_df["Sample_Closed"].sum() / targets_df["Sample_Available"].sum() * 100, 1)
            delta_se = round(filtered_se - total_se, 1)
            delta_display = f"{delta_se} ({filtered_se}%)"  if back_days else None
            st.metric(
                "Sample Exhaustion",
                f"{total_se} %",
                delta_display,
                delta_color="inverse",
                border=True,
            )
    with col4:
        with st.container():
            total_invalid_completes = data_dict["daily_data"]["Invalid Completes"].sum()
            filtered_invalid_completes = daily_df["Invalid Completes"].sum()
            filtered_percent = round(filtered_invalid_completes / total_invalid_completes * 100, 1)
            delta_display = f"{filtered_invalid_completes} ({filtered_percent}%)"  if back_days else None
            st.metric(
                "Data Quality Issues",
                total_invalid_completes,
                delta_display,
                delta_color="inverse",
                border=True,
            )



daily_agg_df = aggregate_daily_data(data_dict["daily_data"], daily_df, targets_df)
    
if selected_countries:
    daily_agg_df = daily_agg_df[daily_agg_df["Country_Label"].isin(selected_countries)]


if not back_days:
    daily_agg_df.drop(columns=["𝛥 Completes", "𝛥 Response Rate", "𝛥 Refusal Rate", "𝛥 Sample Exhaustion", "𝛥 Data Quality Issues"], inplace=True)
else:
    daily_agg_df = apply_style_to_agg_data(daily_agg_df)
with st.container():
    add_header("Country Level Breakdown", 4)

    st.dataframe(
        daily_agg_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Country_Label": st.column_config.TextColumn(label="Country", pinned=True),
            "Methodology": st.column_config.TextColumn(),
            "Valid Completes": st.column_config.TextColumn(),
            "% Completion": st.column_config.ProgressColumn(
                min_value=0, max_value=100, format="%d %%", help="Percentage of target completes achieved"
            ),
            "Response Rate": st.column_config.NumberColumn(format="%f %%"),
            "Refusal Rate": st.column_config.NumberColumn(format="%f %%"),
            "Sample Exhaustion": st.column_config.NumberColumn(format="%f %%"),
            "Data Quality Issues": st.column_config.NumberColumn(format="plain"),
        },
        
    )

if __name__ == "__main__":
    custom_page_style("base.css")
    custom_page_style("1_home.css")
