import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

METRICS = ["Accuracy", "Precision", "Recall", "F1", ]
colors = ["blue", "green", "orange", "black"]
marker = ["o", "o", "o", "o"]

colors = {
    "LSTM": "blue",
    "CNN": "orange",
    "DT": "green"
}

filename = "../complete_complexity_measures.csv"
complexity_result = pd.read_csv(filename)
complexity_result = complexity_result[["abbreviation", "best", "type"]]

filename = "../training_results.csv"
training_result = pd.read_csv(filename)
training_result = training_result[training_result["metric"] == "Accuracy"]

lstm = []
cnn = []
dt = []
for index, row in complexity_result.iterrows():
    value = training_result[training_result["name"] == row["abbreviation"]][row["best"]].iloc[0]
    print(row["abbreviation"], row["best"], value)

    mean, std = value.split(";")
    if row["type"] == "LSTM":
        lstm.append([row["abbreviation"], float(mean), float(std)])
    if row["type"] == "CNN":
        cnn.append([row["abbreviation"], float(mean), float(std)])
    if row["type"] == "DT":
        dt.append([row["abbreviation"], float(mean), float(std)])

lstm = np.array(lstm)
lstm = lstm[lstm[:, 1].argsort()]
cnn = np.array(cnn)
cnn = cnn[cnn[:, 1].argsort()]
dt = np.array(dt)
dt = dt[dt[:, 1].argsort()]

plt.figure(figsize=(13, 3.5))

plt.scatter(lstm[:, 0], lstm[:, 1].astype(float), label="LSTM", color="orange")
plt.scatter(cnn[:, 0], cnn[:, 1].astype(float), label="CNN", color="green")
plt.scatter(dt[:, 0], dt[:, 1].astype(float), label="DT", color="purple")

plt.errorbar(lstm[:, 0], lstm[:, 1].astype(float), lstm[:, 2].astype(float), fmt="o", color="orange")
plt.errorbar(cnn[:, 0], cnn[:, 1].astype(float), cnn[:, 2].astype(float), fmt="o", color="green")
plt.errorbar(dt[:, 0], dt[:, 1].astype(float), dt[:, 2].astype(float), fmt="o", color="purple")

plt.xlabel("Event Logs")
plt.ylabel("Accuracy")
plt.ylim(0, 1.06)

plt.xticks(list(complexity_result["abbreviation"]), rotation=40, ha='right')

plt.grid(True)
plt.legend()
plt.subplots_adjust(left=0.1, bottom=0.35)

plt.savefig("best_accuracy.png", dpi=300)