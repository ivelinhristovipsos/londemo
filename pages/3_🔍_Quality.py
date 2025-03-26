import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title='Quality', layout='wide', page_icon="🔍")
from modules.style_helpers import add_header, global_page_style,custom_page_style

with st.spinner("Loading..."):
        
    add_header("<img src='https://images1.ipsosinteractive.com/GOHBG/ISR/Admin/Reporting_Demo/images/client_logo.png' width='200px'/> <br/> Fieldwork Progress Dashboard - Quality Metrics", 2)

    st.logo('https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg', icon_image='https://upload.wikimedia.org/wikipedia/en/a/a6/Ipsos_logo.svg')


# Generate sample data
date_rng = pd.date_range(start="2024-01-01", end="2024-03-25", freq="D")
df = pd.DataFrame({
    "date": date_rng,
    "completes": np.random.randint(50, 200, size=len(date_rng))  # Random completion numbers
})

# Sidebar filter selection
st.sidebar.header("Filters")
date_options = {"No Filter (All Time)": None, "Last Day": 1, "Last 7 Days": 7, "Last 14 Days": 14}
selected_option = st.sidebar.radio("Select Period", list(date_options.keys()))

# Styling constants
chart_height = 2
axis_label_size = 8
tick_label_size = 6
selected_color = "#165769"
non_selected_color = "#16576980"  # 50% transparent
max_bar_color = "#FF5733"  # Distinct color for max bar
outline_color = "black"  # Bold outline for max bar

# Determine selected range
if date_options[selected_option] is not None:
    end_date = df["date"].max()
    start_date = end_date - timedelta(days=date_options[selected_option])
    df["highlight"] = df["date"].between(start_date, end_date)
else:
    df["highlight"] = True  # No filter applied, highlight all

# Identify max value in the selected range
max_idx = df[df["highlight"]]["completes"].idxmax()
max_value = df.loc[max_idx, "completes"]
max_date = df.loc[max_idx, "date"]

# Plot using Matplotlib
fig, ax = plt.subplots(figsize=(12, chart_height))

# Plot bars
for i, row in df.iterrows():
    color = max_bar_color if i == max_idx else (selected_color if row["highlight"] else non_selected_color)
    bar = ax.bar(row["date"], row["completes"], color=color)

    # Add outline to max bar
    if i == max_idx:
        for rect in bar:
            rect.set_edgecolor(outline_color)
            rect.set_linewidth(1.5)

# Annotate max value on the correct bar
ax.text(max_date, max_value + (max_value * 0.05), f"{max_value}", color="red", 
        ha="center", fontsize=axis_label_size, fontweight="bold")

# Adjust y-axis limits to leave space above max bar
ax.set_ylim(0, max_value * 1.2)

# Customize X-axis labels
ax.set_xticks(df["date"][::7])  # Show every 7th day
ax.set_xticklabels(df["date"][::7].dt.strftime("%b %d"), rotation=45, fontsize=tick_label_size)

# Customize Y-axis labels
ax.tick_params(axis='y', labelsize=tick_label_size)

# Apply axis labels
ax.set_xlabel("Date", fontsize=axis_label_size)
ax.set_ylabel("Completes", fontsize=axis_label_size)

# Legend positioned at the bottom right
#ax.legend(["Selected Period", "Other Days", "Max Value"], 
#          loc="upper center", 
#          bbox_to_anchor=(0.5, -0.3),  # Moves the legend below the x-axis
#          ncol=3,  # Places legend items in a single row
#          fontsize=axis_label_size)

# Show in Streamlit
st.pyplot(fig)

if __name__ == "__main__":
    global_page_style()
    custom_page_style("3_quality.css")