from datetime import timedelta

import matplotlib.pyplot as plt
import plotly.graph_objects as go

# import mpld3
import pandas as pd
import streamlit as st

# import streamlit.components.v1 as components


def keep_state(key):
    # Copy from temporary widget key to permanent key
    st.session_state["_" + key] = st.session_state[key]


def load_state(key, default_value=None):
    # Copy from permanent key to temporary widget key
    if not st.session_state.get("_" + key):
        st.session_state["_" + key] = default_value
    st.session_state[key] = st.session_state["_" + key]

def sidebar_main(country: pd.Series, group: pd.Series, methodology: pd.Series) -> tuple:
    """Sidebar for the main page
    Returns:
        tuple: selected_countries, selected_group, selected_methods
    """
    with st.sidebar:
        st.sidebar.title("Filters")

        country_options = sorted(country.unique())
        method_options = sorted(methodology.unique())
        group_options = sorted(group.unique())

        load_state("country_filter", [])
        selected_countries = st.sidebar.multiselect(
            "Countries",
            country_options,
            placeholder="All countries",
            key="country_filter",
            on_change=keep_state,
            args=["country_filter"],
        )

        load_state("group_filter", [])
        selected_group = st.sidebar.multiselect(
            "Reporting group",
            group_options,
            max_selections=1,
            placeholder="All groups",
            key="group_filter",
            on_change=keep_state,
            args=["group_filter"],
        )

        load_state("method_filter", [])
        selected_methods = st.sidebar.multiselect(
            "Methodologies",
            method_options,
            placeholder="All methodologies",
            key="method_filter",
            on_change=keep_state,
            args=["method_filter"],
        )
    return selected_countries, selected_group, selected_methods


def display_demo_table(agg_func, daily_df, targets_df, expander_title):
    with st.expander(expander_title):
        if not st.session_state.get(agg_func.__name__):
            st.session_state[agg_func.__name__] = "%"  # default selection
        options = ["%", "Abs", "Deviation"]
        selection = st.segmented_control(
            label=agg_func.__name__,
            options=options,
            selection_mode="single",
            key=agg_func.__name__,
            label_visibility="collapsed",
        )

        col_format = None
        if selection in ["%", "Deviation"]:
            col_format = "%f %%"

        if selection:
            agg_df = agg_func(daily_df, targets_df, selection)
            st.dataframe(
                agg_df,
                hide_index=True,
                column_config={
                    "Country_Label": st.column_config.TextColumn(
                        label="Country", pinned=True
                    ),
                    "Methodology": st.column_config.TextColumn(),
                    "Completes": st.column_config.TextColumn(),
                    "18-29": st.column_config.NumberColumn(format=col_format),
                    "30-44": st.column_config.NumberColumn(format=col_format),
                    "45-54": st.column_config.NumberColumn(format=col_format),
                    "55+": st.column_config.NumberColumn(format=col_format),
                    "Male": st.column_config.NumberColumn(format=col_format),
                    "Female": st.column_config.NumberColumn(format=col_format),
                    "Education I": st.column_config.NumberColumn(format=col_format),
                    "Education II": st.column_config.NumberColumn(format=col_format),
                    "Education III": st.column_config.NumberColumn(format=col_format),
                },
            )


def date_filter_change_callback():
    # if there is no selection, select the previous option
    if not st.session_state["date_filter"]:
        st.session_state["date_filter"] = "1d"

@st.cache_data
def draw_completes_barchart(agg_df, max_daily_completes, back_days):
    """
    Draws a bar chart visualizing valid and invalid completes over time.

    Args:
        agg_df (pd.DataFrame): Aggregated DataFrame containing 'Date', 'Valid Completes', and 'Invalid Completes' columns.
        max_daily_completes (int): Maximum daily completes to set the y-axis limit.
        back_days (int): Number of days to highlight in the chart.

    Returns:
        None: Displays the bar chart in the Streamlit app.
    """
    if (
        "Valid Completes" not in agg_df.columns
        or "Invalid Completes" not in agg_df.columns
    ):
        st.error("No data available for this set of filters.", icon="🚨")
        return
    chart_height = 4
    axis_label_size = 8
    tick_label_size = 6
    color_comp = "#165769"
    color_invalid = "#ff5000"
    max_bar_color_comp = "#1e81b0"  # Distinct color for max bar
    max_bar_color_invalid = "red"
    outline_color = "#000066"  # Bold outline for max bar

    # Determine selected range
    agg_df["Highlight"] = True
    if back_days:
        end_date = agg_df["Date"].max()
        start_date = end_date - timedelta(days=back_days)
        agg_df["Highlight"] = agg_df["Date"].between(start_date, end_date)

    # Identify max value in the selected range for Valid Completes
    max_idx_valid = agg_df[agg_df["Highlight"]]["Valid Completes"].idxmax()
    max_value_valid = agg_df.loc[max_idx_valid, "Valid Completes"]
    max_date_valid = agg_df.loc[max_idx_valid, "Date"]

    # Identify max value in the selected range for Invalid Completes
    max_idx_invalid = agg_df[agg_df["Highlight"]]["Invalid Completes"].idxmax()
    max_value_invalid = agg_df.loc[max_idx_invalid, "Invalid Completes"]
    max_date_invalid = agg_df.loc[max_idx_invalid, "Date"]

    # Calculate median completes for Valid and Invalid Completes
    median_valid = agg_df[agg_df["Highlight"]]["Valid Completes"].median()
    median_invalid = agg_df[agg_df["Highlight"]]["Invalid Completes"].median()

    # Plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, chart_height))
    fig.patch.set_alpha(0.0)  # Transparent background for the chart

    # Plot bars
    for i, row in agg_df.iterrows():
        alpha_comp = 1 if row["Highlight"] else 0.5
        alpha_invalid = 1 if row["Highlight"] else 0.5

        bar_valid = ax.bar(
            row["Date"],
            row["Valid Completes"],
            color=color_comp if i != max_idx_valid else max_bar_color_comp,
            alpha=alpha_comp,
        )
        bar_invalid = ax.bar(
            row["Date"],
            row["Invalid Completes"],
            color=color_invalid if i != max_idx_invalid else max_bar_color_invalid,
            alpha=alpha_invalid,
        )

        # Add value labels to all bars
        if row["Date"] != max_date_valid:
            ax.text(
                row["Date"],
                row["Valid Completes"] + (max_daily_completes * 0.02),
                f"{row['Valid Completes']}",
                ha="center",
                fontsize=6,
                color="black",
                rotation=0,
            )
        if row["Date"] != max_date_invalid:
            ax.text(
                row["Date"],
                row["Invalid Completes"] + (max_daily_completes * 0.02),
                f"{row['Invalid Completes']}",
                ha="center",
                fontsize=6,
                color="white",
                rotation=0,
            )

        # Add outline to max bars
        if i == max_idx_valid:
            for rect in bar_valid:
                rect.set_edgecolor(outline_color)
                rect.set_linewidth(1)
        if i == max_idx_invalid:
            for rect in bar_invalid:
                rect.set_edgecolor(outline_color)
                rect.set_linewidth(1)

    # Annotate max values on the correct bars
    ax.text(
        max_date_valid,
        max_value_valid + (max_daily_completes * 0.05),
        f"{max_value_valid}",
        color="black",
        ha="center",
        fontsize=axis_label_size,
        fontweight="bold",
    )
    ax.text(
        max_date_invalid,
        max_value_invalid + (max_daily_completes * 0.05),
        f"{max_value_invalid}",
        color="white",
        ha="center",
        fontsize=axis_label_size,
        fontweight="bold",
    )

    # Add median lines
    ax.axhline(
        median_valid,
        color=max_bar_color_comp,
        linestyle="--",
        linewidth=1,
        label=f"Median Valid Completes ({int(median_valid)})",
    )
    ax.axhline(
        median_invalid,
        color=max_bar_color_invalid,
        linestyle="--",
        linewidth=1,
        label=f"Median Invalid Completes ({int(median_invalid)})",
    )

    # Adjust y-axis limits to leave space above max bars
    ax.set_ylim(0, max_daily_completes * 1.2)

    # Customize X-axis labels
    xticks = list(agg_df["Date"][agg_df["Date"].dt.weekday == 0])  # Show every Monday
    ax.set_xticks(xticks)
    ax.set_xticklabels(
        pd.Series(xticks).dt.strftime("%b %d"), rotation=45, fontsize=tick_label_size
    )

    # Customize Y-axis labels
    ax.tick_params(axis="y", labelsize=tick_label_size)

    # Apply axis labels
    ax.set_xlabel("Date", fontsize=axis_label_size)
    ax.set_ylabel("Completes", fontsize=axis_label_size)

    # Add legend with forced colors
    ax.legend(
        [
            f"Median Valid Completes ({int(median_valid)})",
            f"Median Invalid Completes ({int(median_invalid)})",
            "Valid Completes",
            "Invalid Completes",
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),  # Moves the legend below the x-axis
        ncol=4,  # Places legend items in a single row
        fontsize=axis_label_size,
        frameon=True,  # Keeps the legend box
        handler_map={
            "Valid Completes": plt.Line2D([], [], color=color_comp, alpha=1),
            "Invalid Completes": plt.Line2D([], [], color=color_invalid, alpha=1),
            f"Median Valid Completes ({int(median_valid)})": plt.Line2D(
                [], [], color=max_bar_color_comp, linestyle="--", alpha=1
            ),
            f"Median Invalid Completes ({int(median_invalid)})": plt.Line2D(
                [], [], color=max_bar_color_invalid, linestyle="--", alpha=1
            ),
        },
    )

    st.pyplot(fig, dpi=150)


# fig_html = mpld3.fig_to_html(fig)
# components.html(fig_html, height=600)

@st.cache_data
def draw_gauge(
    value: int | float,
    value_suffix,
    title: str,
    max_value,
    bar_color="dodgerblue",
    tick_spacing=10,
    ranges=[
        {"range": [0, 5], "color": "#FFDDDD"},
        {"range": [5, 20], "color": "#FFF4CC"},
        {"range": [20, 30], "color": "#DDFFDD"},
        {"range": [30, 45], "color": "#FFF4CC"},
        {"range": [45, 60], "color": "#FFDDDD"},
    ],
    mode: str = "gauge+number+delta",
):
    fig = go.Figure(
        go.Indicator(
            mode=mode,
            value=value,
            title={"text": title, "font": {"size": 24, "color": "white"}, "align": "center"},
            gauge={
                "axis": {"range": (0, max_value),"tickcolor": "white", "tickwidth": 2, "tickmode": "linear", "dtick": tick_spacing, "tickfont": {"color": "white"}},
                "bar": {"color": bar_color},
                "steps": ranges,
                "threshold": {
                    "line": {"color": "black", "width": 2},
                    "thickness": 0.75,
                    "value": value,
                },
            },
            number={"suffix": value_suffix, "font": {"color": "white"}},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
       # Set padding and transparent background
    fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),  # Add more padding
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        autosize=False,
        width=400,  # Set width for square proportions
        height=400,  # Set height for square proportions
    )
    st.plotly_chart(fig, use_container_width=True)