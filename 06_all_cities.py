import pandas as pd
import pymannkendall as mk

from pathlib import Path
Path("results").mkdir(exist_ok=True)

CITIES = ["Milano", "Piacenza", "Mantova", "Bologna", "Padova", "Rovigo"]


def yearly_counts(city):
    """Hot, dry and compound days per year for one city (same steps as 03_compound_events.py)."""
    df = pd.read_csv(f"data/{city}.csv", parse_dates=["date"]).set_index("date")

    # hot days: Tmax above the monthly 90th percentile of 1961-1990
    ref = df.loc["1961":"1990"]
    thr = ref["tmax"].groupby(ref.index.month).quantile(0.9)
    df["hot"] = df["tmax"] > df.index.month.map(thr)

    # dry days: 30-day rain below the monthly 10th percentile of 1961-1990
    df["precip30"] = df["precip"].rolling(30).sum()
    ref = df.loc["1961":"1990"]
    pthr = ref["precip30"].groupby(ref.index.month).quantile(0.1)
    df["dry"] = df["precip30"] < df.index.month.map(pthr)

    # compound days: hot AND dry
    df["compound"] = df["hot"] & df["dry"]

    yearly = df[["hot", "dry", "compound"]].resample("Y").sum()
    yearly.index = yearly.index.year
    return yearly


rows = []
for city in CITIES:
    yearly = yearly_counts(city)
    yearly.to_csv(f"results/{city}_yearly_counts.csv")

    row = {"city": city}
    for col in ["hot", "dry", "compound"]:
        result = mk.hamed_rao_modification_test(yearly[col])
        row[f"{col}_slope"] = round(result.slope * 10, 1)    # days per decade
        row[f"{col}_p"] = round(result.p, 3)
    # mean compound days before and after 1990
    row["compound_1961_1990"] = round(yearly.loc[1961:1990, "compound"].mean(), 1)
    row["compound_1991_2025"] = round(yearly.loc[1991:2025, "compound"].mean(), 1)
    rows.append(row)

summary = pd.DataFrame(rows).set_index("city")
summary.to_csv("results/summary_all_cities.csv")
print(summary.to_string())