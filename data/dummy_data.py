import random
import pandas as pd
def dummy_df():
    dataframe_dict = {
    "Country": ["🇫🇷", "🇩🇪", "🇮🇹", "🇪🇸", "🇵🇱", "🇭🇺", "🇬🇷", "🇫🇮", "🇧🇬"],
    "Methodology": ["🌐Web", "🌐Web", "🧑‍🤝‍🧑F2F", "📞CATI", "🧑‍🤝‍🧑F2F", "🧑‍🤝‍🧑F2F", "📞CATI", "📞CATI", "📞CATI"],
    "Valid Completes": [753, 642, 580, 490, 520, 610, 450, 470, 430],
    "% Completion": [75, 68, 60, 55, 58, 62, 50, 52, 48],
    "Response Rate": [35.2, 32.5, 30.1, 28.7, 29.5, 31.0, 27.8, 28.2, 26.9],
    "Refusal Rate": ["-NA-", "12.3%", "10.5%", "9.8%", "11.0%", "10.2%", "9.5%", "10.0%", "8.7%"],
    "Sample Exhaustion": [98, 95, 92, 90, 91, 93, 89, 88, 87],
    "Data Quality Issues": [98, 85, 80, 75, 78, 82, 70, 72, 68]
}

    return pd.DataFrame(dataframe_dict)

# Reporting groups - random combinations of countries and methodologies
def generate_reporting_groups(df):
    reporting_groups = {}
    for i in range(1, 4):  # Create 3 random groups
        random_countries = random.sample(list(df["Country"].unique()), random.randint(2, len(df["Country"].unique())))
        random_methods = random.sample(list(df["Methodology"].unique()), random.randint(1, len(df["Methodology"].unique())))
        group_name = f"Group {i}"
        reporting_groups[group_name] = df[(df["Country"].isin(random_countries)) & (df["Methodology"].isin(random_methods))]
    return reporting_groups