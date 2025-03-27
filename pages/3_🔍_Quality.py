import numpy as np
import pandas as pd
import streamlit as st

from data.data_helpers import get_excel_data
from modules.control_helpers import sidebar_main
from modules.style_helpers import add_header, custom_page_style, global_page_style
from data.data_helpers import map_meth_icons

st.set_page_config(page_title="Quality", layout="wide", page_icon="🔍")
with st.spinner("Loading..."):
    add_header(
        "<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/><br/> Fieldwork Progress Dashboard - Quality Metrics",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
    )

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
        quality_df = quality_df[quality_df["Country_Label"].isin(selected_countries)]
    if selected_methods:
        daily_df = daily_df[daily_df["Methodology"].isin(selected_methods)]
        quality_df = quality_df[quality_df["Methodology"].isin(selected_methods)]

    quality_df = map_meth_icons(quality_df)

    with st.container(border=True) as cont:
        loi_col, nr_col, sl_col, dqi_col = st.columns(4)
        st.text("KPI TBD, the control shared only shows %, and some specs unclear.")
        with loi_col:
            kpi_mask = (kpi_df["kpi"] == "LOI Median",)
            kpi_value = kpi_df.loc[kpi_mask, "value"].values[0]
            st.write(f"LOI Median: {kpi_value}")
        with nr_col:
            kpi_mask = (kpi_df["kpi"] == "NR% Aveage",)
            kpi_value = kpi_df.loc[kpi_mask, "value"].values[0]
            st.write(f"NR% Aveage {kpi_value}")
        with sl_col:
            kpi_mask = (kpi_df["kpi"] == "SL% Average",)
            kpi_value = kpi_df.loc[kpi_mask, "value"].values[0]
            st.write(f"SL% Average {kpi_value}")
        with dqi_col:
            kpi_value = data_dict["daily_data"]["Invalid Completes"].sum()
            st.write(f"Data Quality Issues {kpi_value}")

        
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
                "LOI_median": st.column_config.NumberColumn(label="LOI /median/", format="%f %%"),
                "Flagg_50%_LOI": st.column_config.NumberColumn(label="0.5xMedian LOI", format="%f %%"),
                "Flagg_200%_LOI": st.column_config.NumberColumn(label="2xMedian LOI", format="%f %%"),
                "NR%": st.column_config.NumberColumn(format="%f %%"),
                "NR%_Max": st.column_config.NumberColumn(label="NR% max", format="%f %%"),
                "NR%_95th_percentile": st.column_config.NumberColumn(label="NR% 95th percentile", format="%f %%"),
                "SL%": st.column_config.NumberColumn(format="%f %%"),
                "Sl_40%+": st.column_config.NumberColumn(label="SL 40%+", format="%f %%"),
            },
        )

if __name__ == "__main__":
    global_page_style()
    custom_page_style("3_quality.css")
