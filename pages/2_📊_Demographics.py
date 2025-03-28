import streamlit as st
import streamlit_analytics2 as streamlit_analytics

from modules.control_helpers import display_demo_table, sidebar_main
from modules.data_helpers import (
    aggregate_demo_age_table,
    aggregate_demo_edu_table,
    aggregate_demo_gen_table,
    get_excel_data,
)
from modules.style_helpers import add_header, custom_page_style, global_page_style

st.set_page_config(page_title="Demographics", layout="wide", page_icon="📊")

with streamlit_analytics.track(unsafe_password="ping-pong"):
    add_header(
        "<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/><br/> Fieldwork Progress Dashboard - Demographics",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        size="large",
    )

    with st.spinner("### Loading..."):
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

        with st.container(border=True) as cont:
            # st.divider()
            # add_header("Age", 4)
            display_demo_table(
                aggregate_demo_age_table, daily_df, targets_df, "🔢  Age"
            )
            # st.divider()
            # add_header("Gender", 4)
            display_demo_table(
                aggregate_demo_gen_table, daily_df, targets_df, "👫 Gender"
            )
            # st.divider()
            # add_header("Education", 4)
            display_demo_table(
                aggregate_demo_edu_table, daily_df, targets_df, "📚 Education"
            )

if __name__ == "__main__":
    global_page_style()
    custom_page_style("demographics.css")
