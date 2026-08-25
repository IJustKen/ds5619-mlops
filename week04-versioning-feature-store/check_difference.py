"""
I created this just to check the difference between the 2 seeded datasets
inside data - v1 and v2.
It does not do anything to any of the other code, just exploratory
"""

import pandas as pd

df1 = pd.read_csv("data/v1/transactions.csv")
df2 = pd.read_csv("data/v2/transactions.csv")

matching = []
not_matching = {"v1":[], "v2":[]}

for col in df1.columns:
    if col in df2.columns:
        matching.append(col)
    else:
        not_matching["v1"].append(col)

for col in df2.columns:
    if col not in matching:
        not_matching["v2"].append(col)

print("\nThese columns are common to both")
print(matching)
print("\nThese columns do NOT match")
print(not_matching)
print()

print("\nShowing the values of non matching columns of v1\n")
print(df1[not_matching["v1"]].head())

print("\nShowing the values of non matching columns of v2\n")
print(df2[not_matching["v2"]].head())
