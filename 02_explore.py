import pandas as pd
import matplotlib.pyplot as plt

#read the CSV file by pandas
df = pd.read_csv("data/Padova.csv", parse_dates=["date"])

df = df.set_index("date")
print(df.head())
print(df.describe())

# Fatemeh note:Era5 is a reanalysis with a grid of about 30km,so it is not a reall rain gauge. so values will be smoothed over the all area:)

# mean Tmax of each year
tmax_year =df ["tmax"].resample("Y").mean()

# total precipitation of each year
precip_year = df["precip"].resample("Y").sum()
# Fatemeh note:Y=year_end

# ---- plots ----
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

ax[0].plot(tmax_year.index.year, tmax_year.values, color="firebrick")
ax[0].set_ylabel("Mean Tmax (°C)")
ax[0].set_title("Padova, ERA5 1950–2025")

ax[1].bar(precip_year.index.year, precip_year.values, color="steelblue")
ax[1].set_ylabel("Annual precipitation (mm)")
ax[1].set_xlabel("Year")

plt.tight_layout()
plt.savefig("padova_annual.png", dpi=150)
plt.show()
