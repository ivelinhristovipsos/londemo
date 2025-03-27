import streamlit as st

from matplotlib.patches import Circle, Wedge, Rectangle
import numpy as np
import matplotlib.pyplot as plt

def global_page_style():
    with open("static/base.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def add_header(text, size):
    st.markdown(
        f"<h{size} style='text-align: center;'>{text}</h{size}>", unsafe_allow_html=True
    )


def format_font(text, color, size):
    st.markdown(
        f"<p style='color: {color}; font-size: {size}px;'>{text}</p>",
        unsafe_allow_html=True,
    )


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

def degree_range(n): 
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points
def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation
def gauge(labels=[ "em_5", "em_4", "em_3", "em_2", "em_1"],
          colors=['red','orangered','orange','skyblue','blue'], 
          arrow="", 
          title="", 
          fname=False):     
    
    """
    some sanity checks first
    
    """
    
    N = len(labels)
    
    if arrow > N: 
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow, N)) 
 

    """
    begins the plotting
    """
    
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.subplots_adjust(0,0,2,1)

    ang_range, mid_points = degree_range(N)

    labels = labels[::-1]
    
    """
    plots the sectors and the arcs
    """
    patches = []
    for ang, c in zip(ang_range, colors): 
        # sectors
        patches.append(Wedge((0.,0.), .4,*ang, facecolor='w', lw=2 ))
        # arcs
        patches.append(Wedge((0.,0.), .4,*ang, width=0.2, facecolor=c, lw=2, alpha=0.5,))
    
    [ax.add_patch(p) for p in patches]

    
    """
    set the labels
    """

    for mid, lab in zip(mid_points, labels): 

        ax.text(0.42 * np.cos(np.radians(mid)), 0.42 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=40, \
            fontweight='bold', rotation = rot_text(mid))

    """
    set the bottom banner and the title
    """
    
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)
    

    
    ax.text(0, -0.1, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=18 )

    """
    plots the arrow now
    """
    
    pos = mid_points[abs(arrow - N)]
    
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

    """
    removes frame and ticks, and makes axis equal and tight
    """
    
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    
    st.pyplot(fig)
    
