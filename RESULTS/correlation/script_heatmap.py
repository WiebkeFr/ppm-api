import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = "correlation_accuracy_latex.csv"
df = pd.read_csv(filename)

filename = "correlation_f1_latex.csv"
df2 = pd.read_csv(filename)

result = []
for index, r in df.iterrows():
    d = r[1:]
    d = [ float(value.replace("\\textbf{", "").replace("\\underline{", "").replace("}", "")) if "{" in str(value) else 0.0 for value in d]
    result.append(d)

result2 = []
for index, r in df2.iterrows():
    d = r[1:]
    d = [ float(value.replace("\\textbf{", "").replace("\\underline{", "").replace("}", "")) if "{" in str(value) else 0.0 for value in d]
    result2.append(d)

result_df = pd.DataFrame(data=result).iloc[:, :-1]
result_df2 = pd.DataFrame(data=result2).iloc[:, :-1]

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(9, 4))

im1 = ax1.imshow(result_df, cmap='bwr',vmin=-1, vmax=1)
im2 = ax2.imshow(result_df2, cmap='bwr', vmin=-1, vmax=1)

ax1.set_title('Accuracy')
ax2.set_title('F1-Score')

measures = list(df["metrics"])
ax1.set_yticks(np.arange(len(measures)), labels=measures)
ax2.set_yticks(np.arange(len(measures)), labels=measures)
ax1.set_xticks([])
ax2.set_xticks([])

fig.subplots_adjust(wspace=0.03)
plt.savefig("heatmap.png", dpi=300)
