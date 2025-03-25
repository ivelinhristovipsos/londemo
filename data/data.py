from functools import lru_cache

import pandas as pd
from modules.style_helpers import apply_style_to_agg_data
import matplotlib.pyplot as plt


@lru_cache(maxsize=1)
def get_excel_data(path_to_excel, sheet_name=None):
    df = pd.read_excel(path_to_excel, sheet_name=sheet_name)
    return df


def aggregate_home_daily_table_data(daily_df, filtered_daily_df, targets_df):
    aggregated_data = daily_df
    aggregated_data = (
        daily_df.groupby(["Country_Label", "Methodology"], as_index=False)
        .agg(
            {
                "Valid Completes": "sum",
                "Invalid Completes": "sum",
                "Sample_Closed": "sum",
                "Refusals": "sum",
            }
        )
        .reset_index()
        .rename(
            columns={
                "Invalid Completes": "Data Quality Issues",
                "Sample_Closed": "Sample_Closed",
            }
        )
    )

    filtered_data = (
        filtered_daily_df.groupby(["Country_Label", "Methodology"], as_index=False)
        .agg(
            {
                "Valid Completes": "sum",
                "Invalid Completes": "sum",
                "Sample_Closed": "sum",
                "Refusals": "sum",
            }
        )
        .reset_index()
        .rename(
            columns={
                "Valid Completes": "filtered_compltes",
                "Invalid Completes": "filtered_incompletes",
                "Sample_Closed": "filtered_sample_closed",
                "Refusals": "filtered_refusals",
            }
        )
    )
    aggregated_data = pd.merge(
        aggregated_data,
        filtered_data[
            [
                "filtered_compltes",
                "filtered_incompletes",
                "filtered_refusals",
                "filtered_sample_closed",
                "Country_Label",
            ]
        ],
        on="Country_Label",
    )

    aggregated_data["𝛥 Completes"] = (
        "+"
        + aggregated_data["filtered_compltes"].map(str)
        + " ("
        + round(
            aggregated_data["filtered_compltes"]
            / aggregated_data["Valid Completes"]
            * 100,
            1,
        ).map(str)
        + "%)"
    )

    aggregated_data = pd.merge(
        aggregated_data,
        targets_df[["Target_Completes", "Sample_Available", "Country_Label"]],
        on="Country_Label",
    )
    aggregated_data["% Completion"] = (
        aggregated_data["Valid Completes"] / aggregated_data["Target_Completes"] * 100
    )

    aggregated_data["Response Rate"] = round(
        aggregated_data["Valid Completes"] / aggregated_data["Sample_Closed"] * 100, 1
    )

    aggregated_data["Filtered Response Rate"] = (
        aggregated_data["filtered_compltes"]
        / aggregated_data["filtered_sample_closed"]
        * 100
    )

    aggregated_data["𝛥 Response Rate"] = (
        round(
            aggregated_data["Filtered Response Rate"]
            - aggregated_data["Response Rate"],
            1,
        )
        .apply(lambda x: f"+{x}" if x == abs(x) else x)
        .map(str)
        + " ( "
        + round(aggregated_data["Filtered Response Rate"], 1).map(str)
        + "%)"
    )

    aggregated_data["Refusal Rate"] = round(
        aggregated_data["Refusals"] / aggregated_data["Sample_Closed"] * 100, 1
    )

    aggregated_data["Filtered Refusal Rate"] = (
        aggregated_data["filtered_refusals"]
        / aggregated_data["filtered_sample_closed"]
        * 100
    )

    aggregated_data["𝛥 Refusal Rate"] = (
        round(
            aggregated_data["Filtered Refusal Rate"] - aggregated_data["Refusal Rate"],
            1,
        )
        .apply(lambda x: f"+{x}" if x == abs(x) else x)
        .map(str)
        + " ( "
        + round(aggregated_data["Filtered Refusal Rate"], 1).map(str)
        + "%)"
    )

    aggregated_data["Sample Exhaustion"] = round(
        aggregated_data["Sample_Closed"] / aggregated_data["Sample_Available"] * 100, 1
    )

    aggregated_data["Filtered Sample Exhaustion"] = round(
        aggregated_data["filtered_sample_closed"]
        / aggregated_data["Sample_Available"]
        * 100,
        1,
    )

    aggregated_data["𝛥 Sample Exhaustion"] = (
        round(
            aggregated_data["Filtered Sample Exhaustion"]
            - aggregated_data["Sample Exhaustion"],
            1,
        )
        .apply(lambda x: f"+{x}" if x == abs(x) else x)
        .map(str)
        + " ( "
        + round(aggregated_data["Filtered Sample Exhaustion"], 1).map(str)
        + "%)"
    )

    aggregated_data["Filtered Data Quality Issues"] = aggregated_data[
        "filtered_incompletes"
    ]

    aggregated_data["𝛥 Data Quality Issues"] = (
        "+"
        + aggregated_data["filtered_incompletes"].map(str)
        + " ("
        + round(
            aggregated_data["filtered_incompletes"]
            / aggregated_data["Data Quality Issues"]
            * 100,
            1,
        ).map(str)
        + "%)"
    )

    aggregated_data = aggregated_data[
        [
            "Country_Label",
            "Methodology",
            # "Target_Completes",
            "% Completion",
            "Valid Completes",
            "𝛥 Completes",
            "Response Rate",
            # "Filtered Response Rate"
            "𝛥 Response Rate",
            "Refusal Rate",
            # "Filtered Refusal Rate",
            "𝛥 Refusal Rate",
            "Sample Exhaustion",
            "𝛥 Sample Exhaustion",
            # "Filtered Sample Exhaustion",
            "Data Quality Issues",
            # "Filtered Data Quality Issues",
            "𝛥 Data Quality Issues",
        ]
    ]

    method_recode_dict = {
        "WEB": "Web 🌐",
        "F2F": "F2F 🧑‍🤝‍🧑",
        "CATI": "CATI 📞",
    }
    aggregated_data["Methodology"] = aggregated_data["Methodology"].map(
        method_recode_dict
    )

    return aggregated_data


def aggregate_demo_table(daily_df, target_df, ci):
    if ci not in ["%", "Abs", "Deviation"]:
        raise ValueError("ci must be one of '%', 'Abs', 'Deviation'")

    counts_df = daily_df
    counts_df = (
        daily_df.groupby(["Country_Label", "Methodology"], as_index=False)
        .agg(
            {
                "Valid Completes": "sum",
                "Age_18_29": "sum",
                "Age_30_44": "sum",
                "Age_45_54": "sum",
                "Age_54_plus": "sum",
                "Gender_M": "sum",
                "Gender_F": "sum",
                "Education_I": "sum",
                "Education_II": "sum",
                "Education_III": "sum",
            }
        )
        .reset_index()
        .rename(
            columns={
                "Valid Completes": "Completes",
                "Age_18_29": "18-29",
                "Age_30_44": "30-44",
                "Age_45_54": "45-54",
                "Age_54_plus": "55+",
                "Gender_M": "Male",
                "Gender_F": "Female",
                "Education_I": "Education I",
                "Education_II": "Education II",
                "Education_III": "Education III",
            }
        )
    )

    method_recode_dict = {
        "WEB": "Web 🌐",
        "F2F": "F2F 🧑‍🤝‍🧑",
        "CATI": "CATI 📞",
    }
    counts_df["Methodology"] = counts_df["Methodology"].map(method_recode_dict)

    counts_df.drop("index", axis=1, inplace=True)

    if ci == "Abs":
        return counts_df

    target_count_df = target_df[
        [
            "Country_Label",
            # "Target_Completes",
            "Age_18_29",
            "Age_30_44",
            "Age_45_54",
            "Age_54_plus",
            "Gender_M",
            "Gender_F",
            "Education_I",
            "Education_II",
            "Education_III",
        ]
    ]

    target_count_df.rename(
        columns={
            # "Country_Label": "Country",
            # "Target_Completes": "Completes",
            "Age_18_29": "18-29",
            "Age_30_44": "30-44",
            "Age_45_54": "45-54",
            "Age_54_plus": "55+",
            "Gender_M": "Male",
            "Gender_F": "Female",
            "Education_I": "Education I",
            "Education_II": "Education II",
            "Education_III": "Education III",
        },
        inplace=True,
    )

    proc_df = (
        counts_df.set_index(["Country_Label", "Methodology", "Completes"])
        .div(
            target_count_df.set_index(
                [
                    "Country_Label",
                ]
            )
        )
        .mul(100)
        .round(1)
        .reset_index()
    )
    proc_df = proc_df[
        [
            "Country_Label",
            "Methodology",
            "Completes",
            "18-29",
            "30-44",
            "45-54",
            "55+",
            "Male",
            "Female",
            "Education I",
            "Education II",
            "Education III",
        ]
    ]
    if ci == "%":
        # color green values above 100:
        
        return proc_df.style.applymap(
            lambda x: "color: #09ab3b" if x >= 100 else "",
            subset=[
                "18-29",
                "30-44",
                "45-54",
                "55+",
                "Male",
                "Female",
                "Education I",
                "Education II",
                "Education III",
            ],
        )

    target_perc_df = target_df[
        [
            "Country_Label",
            "Age_18_29_%",
            "Age_30_44_%",
            "Age_45_54_%",
            "Age_54_plus_%",
            "Gender_M_%",
            "Gender_F_%",
            "Education_I_%",
            "Education_II_%",
            "Education_III_%",
        ]
    ]
    target_perc_df.rename(
        columns={
            # "Country_Label": "Country",
            # "Target_Completes": "Completes",
            "Age_18_29_%": "18-29",
            "Age_30_44_%": "30-44",
            "Age_45_54_%": "45-54",
            "Age_54_plus_%": "55+",
            "Gender_M_%": "Male",
            "Gender_F_%": "Female",
            "Education_I_%": "Education I",
            "Education_II_%": "Education II",
            "Education_III_%": "Education III",
        },
        inplace=True,
    )

    diff_df = (
        target_perc_df.set_index(
            [
                "Country_Label",
            ]
        )
        .mul(100)
        .sub(proc_df.set_index(["Country_Label", "Methodology", "Completes"]))
        .round(1)
        .reset_index()
    )
    diff_df = diff_df[
        [
            "Country_Label",
            "Methodology",
            "Completes",
            "18-29",
            "30-44",
            "45-54",
            "55+",
            "Male",
            "Female",
            "Education I",
            "Education II",
            "Education III",
        ]
    ]
    if ci == "Deviation":
        return apply_style_to_agg_data(
            diff_df,
            [
                "18-29",
                "30-44",
                "45-54",
                "55+",
                "Male",
                "Female",
                "Education I",
                "Education II",
                "Education III",
            ],
            None,
        )
        # return diff_df.style.background_gradient(
        #     axis=None,
        #     cmap="PiYG",
        #     subset=[
        #         "18-29",
        #         "30-44",
        #         "45-54",
        #         "55+",
        #         "Male",
        #         "Female",
        #         "Education I",
        #         "Education II",
        #         "Education III",
        #     ],
        # )
