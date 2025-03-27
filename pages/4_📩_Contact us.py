import streamlit as st


from modules.style_helpers import add_header, custom_page_style, global_page_style

st.set_page_config(page_title="Contact us", layout="wide", page_icon="📩")


with st.spinner("Loading..."):
    add_header(
        "<div class='header-banner'><img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/contact_us_banner.png' width='100%'/>",
        2,
    )

    st.logo(
        "https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
        icon_image="https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg",
    )

    st.markdown("<div class='overlap-container'>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown(
            '<h1 class="contact-header">Let\'s Create Something Amazing Together</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="contact-subheader">You like what you see and want to chat about adding value to your project?<br/> We\'re just a message away!</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="mailto-subheader">Reach out by emailing <a href="mailto:"BG-PA-HUB-Management@ipsos.com">BG-PA-HUB-Management@ipsos.com</a> and let\'s give you the data access you need!</p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    global_page_style()
    custom_page_style("4_contact_us.css")
