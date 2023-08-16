import pandas as pd
import numpy as np
from scipy.stats import stats

filename = "../training_results.csv"
df = pd.read_csv(filename)
df = df[df["metric"] == "Time"]

all_times = []

for i, row in df.iterrows():
    row = list(row)[2:]
    times = [float(e.split(";")[0]) for e in row]
    all_times.append(times)

time_df = pd.DataFrame(data=all_times)
removed_outliers = time_df[(np.abs(stats.zscore(time_df)) < 2).all(axis=1)]

avg = list(np.round(removed_outliers.mean(), 3))
std = list(np.round(removed_outliers.std(), 3))
median = list(np.round(removed_outliers.median(), 3))

mean_avg = []
for mean, std in zip(avg, std):
    mean_avg.append(f"{mean}±{std}")

print(mean_avg)
print(median)
