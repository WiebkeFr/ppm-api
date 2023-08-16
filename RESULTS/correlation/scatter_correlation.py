import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

METRIC = "Accuracy"
CATEGORY = "nvar_ent"
TYPE = "CNN_PREPAD_ONEHOT"

filename = "../complete_complexity_measures.csv"
complexity_result = pd.read_csv(filename)[["abbreviation", CATEGORY]]

filename = "../training_results.csv"
training_result = pd.read_csv(filename)
training_result = training_result[training_result["metric"] == METRIC][["name", TYPE]]

result = []
for index, row in complexity_result.iterrows():
    mean = training_result[training_result["name"] == row["abbreviation"]].reset_index()
    try:
        mean, std = mean[TYPE][0].split(";")
        result.append([row["abbreviation"], row[CATEGORY], mean, std])
    except:
        print(mean)

result_df = pd.DataFrame(data=result).sort_values(by=[1])

category = result_df[1].astype(float)
type_mean = result_df[2].astype(float)
std = result_df[3].astype(float)

plt.scatter(category, type_mean)
gradient, intercept = np.polyfit(category, type_mean, 1)
plt.plot(category, gradient * category + intercept, color='black', linewidth=1.5)
plt.savefig("correlation_nvar_ent.png")
