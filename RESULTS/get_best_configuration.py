import pandas as pd

METRIC = "Accuracy"

filename = "training_results.csv"
df = pd.read_csv(filename)
datasets = df[df["metric"] == METRIC]

# iterate through accuracies of the dataset
collect = []

for row in datasets.iterrows():
    result = row[1]
    if result[2:].notna().all():
        # find maximal accuracies
        accuracies = map(lambda x: x.split(";")[0], result[2:])
        max_acc = max(list(accuracies))

        # find config of maximal accuracies
        for index, value in result.items():
            if max_acc in value:
                collect.append([result[0], index, value])

df = pd.DataFrame(data=collect)
max_per_file = df.set_index(0)
print(max_per_file)

