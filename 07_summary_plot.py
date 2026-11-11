import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

summary = pd.read_csv("results/summary_all_cities.csv", index_col=0)

cities = summary.index
x = np.arange(len(cities))      # positions of the cities on the x axis: 0, 1, 2, ...
width = 0.38                    # width of each bar

fig, ax = plt.subplots(figsize=(9, 5))

# two bars per city: before and after 1990
ax.bar(x - width / 2, summary["compound_1961_1990"], width,
       color="#c9b3d9", label="1961-1990")
ax.bar(x + width / 2, summary["compound_1991_2025"], width,
       color="purple", label="1991-2025")

# expected number if heat and drought were independent
ax.axhline(3.65, color="black", linestyle="--", linewidth=1,
           label="expected if independent (3.65)")

# star above the bar if the trend is significant (p < 0.05)
for i, city in enumerate(cities):
    p = summary.loc[city, "compound_p"]
    label = "*" if p < 0.05 else f"p={p:.2f}"
    ax.text(x[i] + width / 2, summary.loc[city, "compound_1991_2025"] + 0.4,
            label, ha="center", fontsize=12 if p < 0.05 else 8)

ax.set_xticks(x)
ax.set_xticklabels(cities)
ax.set_ylabel("Compound hot-dry days per year")
ax.set_title("Compound hot-dry days in the Po Valley have more than doubled (ERA5)",
             loc="left", fontsize=12)
ax.set_ylim(0, 23)
ax.legend(loc="upper left", ncol=3, fontsize=9, frameon=False)
ax.text(0, -0.13, "* significant increasing trend 1950-2025 "
        "(modified Mann-Kendall, Hamed-Rao, p < 0.05)",
        transform=ax.transAxes, fontsize=8, color="gray")

ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("results/summary_compound.png", dpi=150)
plt.show()