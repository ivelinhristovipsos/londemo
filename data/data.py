from functools import lru_cache
import pandas as pd


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
            }
        )
        .reset_index()
        .rename(columns={"Invalid Completes": "Data Quality Issues", "Sample_Closed": "Sample_Closed"})
    )

    filtered_data = (
        filtered_daily_df.groupby(["Country_Label", "Methodology"], as_index=False)
        .agg(
            {
                "Valid Completes": "sum",
            }
        )
        .reset_index()
        .rename(columns={"Valid Completes": "𝛥 Completes"})
    )
    aggregated_data = pd.merge(
        aggregated_data,
        filtered_data[["𝛥 Completes", "Country_Label"]],
        on="Country_Label",
    )

    aggregated_data["𝛥 Completes"] = "+" + aggregated_data["𝛥 Completes"].map(str) + " (" + round(aggregated_data["𝛥 Completes"] / aggregated_data["Valid Completes"] * 100, 1).map(str) + "%)"


    aggregated_data = pd.merge(
        aggregated_data,
        targets_df[["Target_Completes", "Country_Label"]],
        on="Country_Label",
    )
    aggregated_data["% Completion"] = (
        aggregated_data["Valid Completes"] / aggregated_data["Target_Completes"] * 100
    )

    aggregated_data["Response Rate"] = round(aggregated_data["Valid Completes"] / aggregated_data["Sample_Closed"] * 100, 1)

    aggregated_data.drop(columns=["index", "Sample_Closed"], inplace=True)

    aggregated_data = aggregated_data[["Country_Label", "Methodology", "Target_Completes", "Valid Completes", "𝛥 Completes", "% Completion", "Response Rate", "Data Quality Issues" ]]
    
    return aggregated_data
