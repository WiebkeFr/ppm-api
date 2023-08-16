import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NAME = "Pdc_2021_4"
METRICS = ["Accuracy", "Precision", "Recall", "F1", ]
colors = ["blue", "green", "orange", "black"]
marker = ["o", "o", "o", "o"]
filename = "../training_results.csv"

training_result = pd.read_csv(filename)
training_result = training_result[training_result["name"] == NAME]
CATEGORY = ['PREPAD_ONEHOT', 'PREPAD_EMB', 'PREPAD_FREQ', 'CONT_ONEHOT', 'CONT_EMB', 'CONT_FREQ']

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(10, 4))

for index, metric in enumerate(METRICS):
    result = training_result[training_result["metric"] == metric].iloc[:, 2:].reset_index(drop=True).iloc[0]
    mean = [float(mean_std.split(";")[0]) for mean_std in result]
    std = [float(mean_std.split(";")[1]) for mean_std in result]
    zorder = 4 - index

    ax1.scatter(CATEGORY, mean[:6], label=metric, color=colors[index], marker=marker[index])
    ax1.errorbar(CATEGORY, mean[:6], yerr=std[:6], fmt=marker[index], color=colors[index], zorder=zorder)

    ax2.scatter(CATEGORY, mean[6:12], label=metric, color=colors[index], marker=marker[index])
    ax2.errorbar(CATEGORY, mean[6:12], yerr=std[6:12], fmt=marker[index], color=colors[index], zorder=zorder)

    ax3.scatter(CATEGORY, mean[12:], label=metric, color=colors[index], marker=marker[index])
    ax3.errorbar(CATEGORY, mean[12:], yerr=std[12:], fmt=marker[index], color=colors[index], zorder=zorder)

ax1.set_title('LSTM')
ax2.set_title('CNN')
ax3.set_title('DT')

for ax in [ax1, ax2, ax3]:
    ax.set_xticks(CATEGORY)
    ax.set_xticklabels(CATEGORY, rotation=35, ha='right', rotation_mode='anchor')
    ax.grid(True)

fig.subplots_adjust(left=0.1, bottom=0.35, wspace=0.1)
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.38),fancybox=False, shadow=False, ncol=2)
fig.text(0.5, 0.03, 'Techniques', ha='center', size='large')
plt.savefig("pdc_2021_4.png", dpi=300)