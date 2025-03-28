from threading import RLock

import numpy as np
import pandas as pd
import streamlit as st
import streamlit_analytics2 as streamlit_analytics

from modules.control_helpers import (
    date_filter_change_callback,
    draw_completes_barchart,
    sidebar_main,
)
from modules.data_helpers import aggregate_home_daily_table_data, get_excel_data
from modules.style_helpers import add_header, apply_style_to_agg_data, custom_page_style

st.set_page_config(page_title="Home", layout="wide", page_icon="🏠")

with streamlit_analytics.track(unsafe_password="oppоrtunity"):

    add_header(
        "<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/><br/> Fieldwork Progress Dashboard",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        size="large",
    )



    data_dict = get_excel_data("data/dummy_data.xlsx")
    daily_df = data_dict["daily_data"]
    targets_df = data_dict["targets"]

    # Sidebar
    selected_countries, selected_group, selected_methods = sidebar_main(
        daily_df["Country_Label"], daily_df["Group"], daily_df["Methodology"]
    )
    if selected_group:
        daily_df = daily_df[daily_df["Group"].isin(selected_group)]
    if selected_countries:
        daily_df = daily_df[daily_df["Country_Label"].isin(selected_countries)]
    if selected_methods:
        daily_df = daily_df[daily_df["Methodology"].isin(selected_methods)]

    daily_country_flt_df = daily_df.copy()

    # Top-level metrics container
    with st.container(border=True) as cont:
        options = ["1d", "7d", "14d", "max"]
        if not st.session_state.get("date_filter"):
            st.session_state["date_filter"] = options[0]
        selection = st.segmented_control(
            label="date_filter",
            options=options,
            selection_mode="single",
            key="date_filter",
            label_visibility="collapsed",
            on_change=date_filter_change_callback,
        )

        # LOGIC:
        back_days = None
        if selection in ["1d", "7d", "14d"]:
            back_days = int(selection[:-1])
            period_selection_mask = daily_df["Date"] >= daily_df[
                "Date"
            ].max() - pd.Timedelta(days=back_days)
            daily_df = daily_df[period_selection_mask]

        # st.text(f'{daily_df["Date"].dt.date.min()} - {daily_df["Date"].dt.date.max()}')

        # Main KPIs
        completes_col, response_rate_col, sample_exhaustion_col, dq_issues_col = (
            st.columns(4)
        )
        with completes_col:
            with st.container():
                total_valid_completes = data_dict["daily_data"]["Valid Completes"].sum()
                filtered_valid_completes = daily_df["Valid Completes"].sum()
                filtered_percent = round(
                    filtered_valid_completes / total_valid_completes * 100, 1
                )
                delta_display = (
                    f"{filtered_valid_completes} ({filtered_percent}%)"
                    if back_days
                    else None
                )
                st.metric(
                    "Valid Completes", total_valid_completes, delta_display, border=True
                )
        with response_rate_col:
            with st.container():
                total_rr = round(
                    total_valid_completes
                    / data_dict["daily_data"]["Sample_Closed"].sum()
                    * 100,
                    1,
                )
                filtered_rr = round(
                    daily_df["Valid Completes"].sum()
                    / daily_df["Sample_Closed"].sum()
                    * 100,
                    1,
                )
                delta_rr = round(filtered_rr - total_rr, 1)
                delta_display = f"{delta_rr} ({filtered_rr}%)" if back_days else None
                st.metric("Response Rate", f"{total_rr} %", delta_display, border=True)

        with sample_exhaustion_col:
            with st.container():
                total_se = round(
                    data_dict["daily_data"]["Sample_Closed"].sum()
                    / targets_df["Sample_Available"].sum()
                    * 100,
                    1,
                )
                filtered_se = round(
                    daily_df["Sample_Closed"].sum()
                    / targets_df["Sample_Available"].sum()
                    * 100,
                    1,
                )

                delta_se = round(filtered_se - total_se, 1)
                delta_display = f"{delta_se} ({filtered_se}%)" if back_days else None
                st.metric(
                    "Sample Exhaustion",
                    f"{total_se} %",
                    delta_display,
                    delta_color="inverse",
                    border=True,
                )
        with dq_issues_col:
            with st.container():
                total_invalid_completes = data_dict["daily_data"][
                    "Invalid Completes"
                ].sum()
                filtered_invalid_completes = daily_df["Invalid Completes"].sum()
                filtered_percent = round(
                    filtered_invalid_completes / total_invalid_completes * 100, 1
                )
                delta_display = (
                    f"{filtered_invalid_completes} ({filtered_percent}%)"
                    if back_days
                    else None
                )
                st.metric(
                    "Data Quality Issues",
                    total_invalid_completes,
                    delta_display,
                    delta_color="inverse",
                    border=True,
                )

        # Chart

        ############################################################
        with st.spinner("### Loading..."):
            date_rng = pd.date_range(
                start=data_dict["daily_data"]["Date"].min(),
                end=data_dict["daily_data"]["Date"].max(),
                freq="D",
            )
            agg_df = (
                pd.pivot_table(
                    daily_country_flt_df,
                    index="Date",
                    values=["Valid Completes", "Invalid Completes"],
                    aggfunc=np.sum,
                )
                .reindex(date_rng)
                .reset_index(names=["Date"])
            )

            max_daily_completes = (
                data_dict["daily_data"].groupby("Date")["Valid Completes"].sum().max()
            )
            max_daily_completes_filtered = (
                daily_country_flt_df.groupby("Date")["Valid Completes"].sum().max()
            )
            if max_daily_completes / 2 > max_daily_completes_filtered:
                max_daily_completes /= 2

        _lock = RLock()
        with _lock:
            draw_completes_barchart(agg_df, max_daily_completes, back_days)

        # Country-level breakdown table

        ############################################################

        daily_agg_df = aggregate_home_daily_table_data(
            data_dict["daily_data"], daily_df, targets_df
        )
        if selected_countries:
            daily_agg_df = daily_agg_df[
                daily_agg_df["Country_Label"].isin(selected_countries)
            ]

        if not back_days:
            daily_agg_df.drop(
                columns=[
                    "𝛥 Completes",
                    "𝛥 Response Rate",
                    "𝛥 Refusal Rate",
                    "𝛥 Sample Exhaustion",
                    "𝛥 Data Quality Issues",
                ],
                inplace=True,
            )
        else:
            daily_agg_df = apply_style_to_agg_data(
                daily_agg_df,
                ["𝛥 Completes", "𝛥 Response Rate"],
                [
                    "𝛥 Refusal Rate",
                    "𝛥 Sample Exhaustion",
                    "𝛥 Data Quality Issues",
                ],
            )

        st.dataframe(
            daily_agg_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Country_Label": st.column_config.TextColumn(
                    label="Country", pinned=True
                ),
                "Methodology": st.column_config.TextColumn(),
                "Valid Completes": st.column_config.TextColumn(),
                "% Completion": st.column_config.ProgressColumn(
                    min_value=0,
                    max_value=100,
                    format="%d %%",
                    help="Percentage of target completes achieved",
                ),
                "Response Rate": st.column_config.NumberColumn(format="%f %%"),
                "Refusal Rate": st.column_config.NumberColumn(format="%f %%"),
                "Sample Exhaustion": st.column_config.NumberColumn(format="%f %%"),
                "Data Quality Issues": st.column_config.NumberColumn(format="plain"),
            },
        )


if __name__ == "__main__":
    custom_page_style("base.css")
    custom_page_style("home.css")
