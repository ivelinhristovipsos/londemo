from functools import lru_cache

import pandas as pd
import streamlit as st


@lru_cache(maxsize=1)
def get_excel_data(path_to_excel, sheet_name=None):
    df = pd.read_excel(path_to_excel, sheet_name=sheet_name)
    return df


def aggregate_daily_data(daily_df, filtered_daily_df, targets_df):
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
