import streamlit as st

# Set page configuration
st.set_page_config(page_title='Quality', layout='wide', page_icon="🔍")
from modules.style_helpers import add_header, global_page_style,custom_page_style

add_header("<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/> Fieldwork Progress Dashboard - Quality Metrics", 2)

st.logo('https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg', icon_image='https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg')

if __name__ == "__main__":
    global_page_style()
    custom_page_style("3_quality.css")