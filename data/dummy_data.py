import random
import pandas as pd


from functools import lru_cache

@lru_cache
def raw_dummy_data(filter=None, no_of_rows=200):
    raw_data = {
        "Date": pd.date_range(start="2025-01-01", periods=no_of_rows, freq="D").tolist(),
        "Group": [random.choice(["Group 1", "Group 2", "Group 3", "Group 4", "Group 5"]) for _ in range(no_of_rows)],
        "Country": [random.choice(["🇫🇷", "🇩🇪", "🇮🇹", "🇪🇸", "🇵🇱", "🇭🇺", "🇬🇷", "🇫🇮", "🇧🇬"]) for _ in range(no_of_rows)],
        "Methodology": [random.choice(["🌐Web", "🧑‍🤝‍🧑F2F", "📞CATI"]) for _ in range(no_of_rows)],
        "Valid Completes": [random.randint(1, 50) for _ in range(no_of_rows)],
        "% Completion": [random.randint(0, 100) for _ in range(no_of_rows)],
        "Response Rate": [random.randint(0, 100) for _ in range(no_of_rows)],
        "Refusal Rate": [random.choice(["-NA-", random.randint(0, 50)]) for _ in range(no_of_rows)],
        "Sample Exhaustion": [random.randint(0, 100) for _ in range(no_of_rows)],
        "Data Quality Issues": [random.randint(1, 10) for _ in range(no_of_rows)],
    }
    
    df = pd.DataFrame(raw_data)
    if filter:
        df = df.loc[filter]

    return df

def dummy_df(df):
    aggregated_data = df.groupby(["Country", "Methodology"]).agg(
        {
            "Valid Completes": "sum",
            "% Completion": "mean",
            "Response Rate": "mean",
            "Refusal Rate": lambda x: "-NA-" if all(v == "-NA-" for v in x) else sum(float(v) for v in x if v != '-NA-') / len([v for v in x if v != '-NA-']),
            "Sample Exhaustion": "mean",
            "Data Quality Issues": "sum",
        }
    ).reset_index()
    return aggregated_data
