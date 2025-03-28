import numpy as np
import pandas as pd
import streamlit as st
import streamlit_analytics2 as streamlit_analytics

from modules.control_helpers import draw_gauge, sidebar_main
from modules.data_helpers import get_excel_data, map_meth_icons
from modules.style_helpers import add_header, custom_page_style, global_page_style

st.set_page_config(page_title="Quality", layout="wide", page_icon="🔍")
with streamlit_analytics.track(unsafe_password="ping-pong"):
    add_header(
        "<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/><br/> Fieldwork Progress Dashboard - Quality Metrics",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        size="large",
    )

    with st.spinner("Loading..."):
        data_dict = get_excel_data("data/dummy_data.xlsx")
        daily_df = data_dict["daily_data"]
        kpi_df = data_dict["quality_kpi"]
        quality_df = data_dict["quality_table"].copy()

        selected_countries, selected_group, selected_methods = sidebar_main(
            daily_df["Country_Label"], daily_df["Group"], daily_df["Methodology"]
        )
        if selected_group:
            daily_df = daily_df[daily_df["Group"].isin(selected_group)]
            quality_df = quality_df[quality_df["Group"].isin(selected_group)]
        if selected_countries:
            daily_df = daily_df[daily_df["Country_Label"].isin(selected_countries)]
            quality_df = quality_df[
                quality_df["Country_Label"].isin(selected_countries)
            ]
        if selected_methods:
            daily_df = daily_df[daily_df["Methodology"].isin(selected_methods)]
            quality_df = quality_df[quality_df["Methodology"].isin(selected_methods)]

        quality_df = map_meth_icons(quality_df)

        with st.container(border=True) as cont:
            loi_col, nr_col, sl_col, dqi_col = st.columns(4)
            with loi_col:
                kpi_mask = (kpi_df["kpi"] == "LOI Median",)
                kpi_value = kpi_df.loc[kpi_mask, "value"].values[0]
                draw_gauge(
                    kpi_value,
                    " min",
                    "LOI Median",
                    max_value=60,
                    bar_color="#165769",
                    mode="gauge+number",
                    ranges=[
                        {"range": [0, 5], "color": "#ff9191"},
                        {"range": [5, 20], "color": "#FFF4CC"},
                        {"range": [20, 30], "color": "#DDFFDD"},
                        {"range": [30, 45], "color": "#FFF4CC"},
                        {"range": [45, 60], "color": "#ff9191"},
                    ],
                )
            with nr_col:
                kpi_mask = (kpi_df["kpi"] == "NR% Aveage",)
                kpi_value = kpi_df.loc[kpi_mask, "value"].values[0] * 100
                draw_gauge(
                    kpi_value,
                    " %",
                    "Non-response AVG",
                    max_value=100,
                    bar_color="#165769",
                    mode="gauge+number",
                    ranges=[
                        {"range": [0, 5], "color": "#ff9191"},
                        {"range": [5, 10], "color": "#FFF4CC"},
                        {"range": [10, 30], "color": "#DDFFDD"},
                        {"range": [30, 40], "color": "#FFF4CC"},
                        {"range": [40, 100], "color": "#ff9191"},
                    ],
                )
            with sl_col:
                kpi_mask = (kpi_df["kpi"] == "SL% Average",)
                kpi_value = kpi_df.loc[kpi_mask, "value"].values[0] * 100
                draw_gauge(
                    kpi_value,
                    " %",
                    "Straightliners AVG",
                    max_value=100,
                    bar_color="#165769",
                    mode="gauge+number",
                    ranges=[
                        {"range": [0, 5], "color": "#DDFFDD"},
                        {"range": [5, 10], "color": "#FFF4CC"},
                        {"range": [10, 100], "color": "#ff9191"},
                    ],
                )
            with dqi_col:
                kpi_value = data_dict["daily_data"]["Invalid Completes"].sum()
                max_value = data_dict["daily_data"]["Valid Completes"].sum()
                draw_gauge(
                    kpi_value,
                    None,
                    "Data Quality Issues",
                    max_value=max_value,
                    bar_color="#165769",
                    mode="gauge+number",
                    tick_spacing=200,
                    ranges=[
                        {"range": [0, max_value], "color": "#ff9191"},
                        {"range": [10, max_value * 0.2], "color": "#FFF4CC"},
                        {"range": [0, max_value * 0.1], "color": "#DDFFDD"},
                    ],
                )
            quality_df = quality_df.drop(columns=["Group"])
            st.dataframe(
                quality_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Country_Label": st.column_config.TextColumn(
                        label="Country", pinned=True
                    ),
                    "Methodology": st.column_config.TextColumn(),
                    "Completes": st.column_config.TextColumn(label="Valid Completes"),
                    "LOI_median": st.column_config.NumberColumn(
                        label="Median LOI", format="%f %%"
                    ),
                    "Flagg_50%_LOI": st.column_config.NumberColumn(
                        label="0.5 x Median LOI", format="%f %%"
                    ),
                    "Flagg_200%_LOI": st.column_config.NumberColumn(
                        label="2 x Median LOI", format="%f %%"
                    ),
                    "NR%": st.column_config.NumberColumn(format="%f %%"),
                    "NR%_Max": st.column_config.NumberColumn(
                        label="NR % max", format="%f %%"
                    ),
                    "NR%_95th_percentile": st.column_config.NumberColumn(
                        label="NR % 95th percentile", format="%f %%"
                    ),
                    "SL%": st.column_config.NumberColumn(format="%f %%"),
                    "Sl_40%+": st.column_config.NumberColumn(
                        label="SL > 40%", format="%f %%"
                    ),
                },
            )

if __name__ == "__main__":
    global_page_style()
    custom_page_style("quality.css")
