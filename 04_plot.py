import pandas as pd
import matplotlib.pyplot as plt

# read the yearly counts saved by 03_compound_events.py
yearly = pd.read_csv("padova_yearly_counts.csv", index_col=0)

# what each panel shows: (column, title, colour, expected value in a stable climate)
panels = [
    ("hot",      "Hot days (Tmax > 90th percentile)",          "firebrick", 36.5),
    ("dry",      "Dry days (30-day rain < 10th percentile)",   "darkorange", 36.5),
    ("compound", "Compound hot-dry days",                      "purple",     3.65),
]

fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

for ax, (col, title, color, expected) in zip(axes, panels):
    # bars: number of days in each year
    ax.bar(yearly.index, yearly[col], color=color, alpha=0.4)

    # line: 10-year moving average (shows the long-term behaviour)
    smooth = yearly[col].rolling(10, center=True).mean()
    ax.plot(yearly.index, smooth, color=color, linewidth=2.5, label="10-year moving average")

    # dashed line: what we expect in the 1961-1990 climate
    ax.axhline(expected, color="black", linestyle="--", linewidth=1,
               label=f"expected ({expected} days/year)")

    ax.set_title(title, loc="left", fontsize=11)
    ax.set_ylabel("days per year")
    ax.legend(loc="upper left", fontsize=8)

axes[-1].set_xlabel("Year")
fig.suptitle("Padova (ERA5, 1950-2025): hot, dry and compound hot-dry days", fontsize=13)

plt.tight_layout()
plt.savefig("padova_compound.png", dpi=150)
plt.show()