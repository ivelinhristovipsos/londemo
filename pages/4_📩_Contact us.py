import streamlit as st

# Set page configuration
st.set_page_config(page_title='Contact us', layout='wide', page_icon="📩")
from modules.style_helpers import add_header, global_page_style,custom_page_style

add_header("<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='100px'/>", 2)

st.logo('https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg', icon_image='https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg')

with st.container(border=True) as cont:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="contact-header">Let\'s Create Something Amazing Together</h1>', unsafe_allow_html=True)
    st.markdown('<p class="contact-subheader">You like what you see and want to chat about adding value to your project?<br/> We\'re just a message away!</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    global_page_style()
    custom_page_style("4_contact_us.css")