import streamlit as st


def global_page_style():  
    with open("static/stylesheets.css") as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def add_header(text, size):
    st.markdown(f"<h{size} style='text-align: center;'>{text}</h{size}>", unsafe_allow_html=True)
