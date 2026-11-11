import pandas as pd
import pymannkendall as mk

# read the yearly counts
yearly = pd.read_csv("padova_yearly_counts.csv", index_col=0)

for col in ["hot", "dry", "compound"]:
    result = mk.hamed_rao_modification_test(yearly[col])

    # Sen's slope is in days per year -> multiply by 10 for days per decade
    slope_decade = result.slope * 10

    print(f"{col:9s} trend: {result.trend:12s} "
          f"p-value: {result.p:.4f}   "
          f"Sen's slope: {slope_decade:+.1f} days/decade")