
import streamlit as st

@st.cache_data
def global_page_style():
    with open("static/base.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

@st.cache_data
def add_header(text, size):
    st.markdown(
        f"<h{size} style='text-align: center;'>{text}</h{size}>", unsafe_allow_html=True
    )

@st.cache_data
def format_font(text, color, size):
    st.markdown(
        f"<p style='color: {color}; font-size: {size}px;'>{text}</p>",
        unsafe_allow_html=True,
    )

@st.cache_data
def custom_page_style(css_file_name):
    with open("static/" + css_file_name) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def apply_style_to_agg_data(aggdata_df, green_pos_cols: list, red_pos_cols: list):
    def color_positive_green(val):
        color = "red" if "-" in str(val) else "#09ab3b"
        return f"color: {color}"

    def color_positive_red(val):
        color = "#09ab3b" if "-" in str(val) else "red"
        return f"color: {color}"

    if green_pos_cols:
        aggdata_style = aggdata_df.style.applymap(
            color_positive_green,
            subset=green_pos_cols,
        )

    if red_pos_cols:
        aggdata_style = aggdata_style.applymap(
            color_positive_red,
            subset=red_pos_cols,
        )
    return aggdata_style



# ###############################



