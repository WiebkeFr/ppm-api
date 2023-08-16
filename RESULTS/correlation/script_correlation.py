import pandas as pd
from scipy import stats

METRIC = "Accuracy"

filename = "../complete_complexity_measures.csv"
complexity_result = pd.read_csv(filename)

abbr = complexity_result[["abbreviation"]]
complexity_result = complexity_result.iloc[:, 4:-3]
CATEGORIES = complexity_result.columns
complexity_result["name"] = abbr

complexity_result = complexity_result.sort_values(by=['name']).reset_index(drop=True)
filename = "../training_results.csv"
training_result = pd.read_csv(filename)

TYPES = training_result.columns[2:]
training_result = training_result[training_result["metric"] == METRIC].sort_values(by=['name']).reset_index(drop=True)

for index, row in training_result.iterrows():
    training_result.iloc[index, 2:] = [mean_std.split(";")[0] for mean_std in row[2:]]

result = []
num_low_sign = 0
num_high_sign = 0

for category in CATEGORIES:
    result_types = []
    for type in TYPES:
        x = complexity_result[category].astype(float)
        y = training_result[type].astype(float)
        ken = stats.pearsonr(x, y)
        if ken.pvalue <= 0.01:
            num_high_sign = num_high_sign + 1
        elif ken.pvalue <= 0.05:
            num_low_sign = num_low_sign + 1
        else:
            result_types.append(f"{round(ken.statistic, 3)};{round(ken.pvalue, 3)}")

    result.append([category, *result_types])

df = pd.DataFrame(data=result)
df.columns = ["metrics", *TYPES]
df.to_csv("correlation_pearson_accuracy_pvalue.csv", index=False)

print(num_low_sign, num_high_sign)


