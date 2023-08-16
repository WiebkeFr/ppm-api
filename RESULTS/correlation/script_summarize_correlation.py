import pandas as pd

filename = "correlation_accuracy_latex.csv"
df = pd.read_csv(filename)

filename2 = "correlation_f1_latex.csv"
df2 = pd.read_csv(filename2)

zu = []
for index, r in df.iterrows():
    lower_sign = r[0].count("underline")
    lower_sign_neg = r[0].count("underline{-")
    high_sign = r[0].count("textbf")
    high_sign_neg = r[0].count("textbf{-")
    metric = r[0].split(" & ")[0]

    zu.append([metric, lower_sign, f"-{lower_sign_neg}", f"+{ lower_sign - lower_sign_neg}", high_sign, f"-{high_sign_neg}", f"+{high_sign - high_sign_neg}"])

gh = pd.DataFrame(data=zu)
gh.to_csv("correlation_accuracy_analyse.csv", index=False)

overlap = 0
for index, r in df.iterrows():
    for j, c in enumerate(list(r)):
        f1 = df2.iloc[index][j]
        if c == f1:
            print("Achtung", c)

        elif "textbf" in c and "textbf" in f1:
            overlap = overlap + 1

        elif "under" in c and "under" in f1:
            overlap = overlap + 1

        elif not "textbf" in c and not "textbf" in f1 and not "under" in c and not "under" in f1:
            overlap = overlap + 1


print(overlap)


