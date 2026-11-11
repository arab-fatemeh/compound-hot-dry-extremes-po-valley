import pandas as pd

df = pd.read_csv("data/Padova.csv", parse_dates=["date"])
df = df.set_index("date")

# reference period (climate "normal")
ref = df.loc["1961":"1990"]

# 90th percentile of Tmax for each month (12 values)
thr = ref["tmax"].groupby(ref.index.month).quantile(0.9)
print(thr)

# give each day the threshold of its own month
df["tmax_thr"] = df.index.month.map(thr)

# hot day = Tmax above the threshold
df["hot"] = df["tmax"] > df["tmax_thr"]

# number of hot days per year
hot_per_year = df["hot"].resample("Y").sum()
print(hot_per_year)

# Fatemeh note: 365*0.1(90th percentile means 10% of days are above it )=36 hot days per year means if we have more than 36 hot days per year, It means 

# rainfall of the last 30 days (rolling sum)
df["precip30"] = df["precip"].rolling(30).sum()

# reference period again (now it has the precip30 column)
ref = df.loc["1961":"1990"]

# 10th percentile of 30-day rainfall for each month
pthr = ref["precip30"].groupby(ref.index.month).quantile(0.1)
print(pthr)

# give each day the threshold of its own month
df["precip_thr"] = df.index.month.map(pthr)

# dry day = 30-day rainfall below the threshold
df["dry"] = df["precip30"] < df["precip_thr"]

# number of dry days per year
dry_per_year = df["dry"].resample("Y").sum()
print(dry_per_year)

import pandas as pd

df = pd.read_csv("data/Padova.csv", parse_dates=["date"])
df = df.set_index("date")

# ================= HOT DAYS =================
# reference period (climate "normal")
ref = df.loc["1961":"1990"]

# 90th percentile of Tmax for each month (12 values)
thr = ref["tmax"].groupby(ref.index.month).quantile(0.9)
print(thr)

# give each day the threshold of its own month
df["tmax_thr"] = df.index.month.map(thr)

# hot day = Tmax above the threshold
df["hot"] = df["tmax"] > df["tmax_thr"]

# number of hot days per year
hot_per_year = df["hot"].resample("Y").sum()

# Fatemeh note: 90th percentile means 10% of days are above it,
# so in the reference climate we expect about 365 * 0.1 = 36 hot days per year.

# ================= DRY DAYS =================
# rainfall of the last 30 days (rolling sum)
df["precip30"] = df["precip"].rolling(30).sum()

# reference period again (now it has the precip30 column)
ref = df.loc["1961":"1990"]

# 10th percentile of 30-day rainfall for each month
pthr = ref["precip30"].groupby(ref.index.month).quantile(0.1)
print(pthr)

# give each day the threshold of its own month
df["precip_thr"] = df.index.month.map(pthr)

# dry day = 30-day rainfall below the threshold
df["dry"] = df["precip30"] < df["precip_thr"]

# number of dry days per year
dry_per_year = df["dry"].resample("Y").sum()

# ================= COMPOUND DAYS =================
# compound day = hot AND dry on the same day
df["compound"] = df["hot"] & df["dry"]

# number of compound days per year
compound_per_year = df["compound"].resample("Y").sum()

# Fatemeh note: if heat and drought were independent,
# we would expect 0.1 * 0.1 = 1% of days, about 3.6 compound days per year.

# ================= SAVE AND PRINT =================
yearly = pd.DataFrame({
    "hot": hot_per_year,
    "dry": dry_per_year,
    "compound": compound_per_year,
})
yearly.index = yearly.index.year
yearly.to_csv("padova_yearly_counts.csv")

print(yearly.to_string())
print("\nMean compound days per year:", round(yearly["compound"].mean(), 1))