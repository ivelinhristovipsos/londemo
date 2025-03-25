import streamlit as st


def global_page_style():  
    with open("static/base.css") as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def add_header(text, size):
    st.markdown(f"<h{size} style='text-align: center;'>{text}</h{size}>", unsafe_allow_html=True)

def format_font(text, color, size):
    st.markdown(f"<p style='color: {color}; font-size: {size}px;'>{text}</p>", unsafe_allow_html=True)

def custom_page_style(css_file_name):
    with open("static/"+css_file_name) as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def apply_style_to_agg_data(aggdata_df):

    def color_positive_green(val):
        color = "red" if "-" in val else "#09ab3b"
        return f"color: {color}"

    def color_positive_red(val):
        color = "red" if "+" in val else "#09ab3b"
        return f"color: {color}"

    aggdata_style = aggdata_df.style.applymap(
        color_positive_green,
        subset=[
            "𝛥 Completes",
            "𝛥 Response Rate",
            
        ],
    ).applymap(
        color_positive_red,
        subset=[
            
            "𝛥 Refusal Rate",
            "𝛥 Sample Exhaustion",
            "𝛥 Data Quality Issues",
        ],
    )
    return aggdata_style
