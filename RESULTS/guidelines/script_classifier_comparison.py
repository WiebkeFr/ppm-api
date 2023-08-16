import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn import metrics, preprocessing
from csv import writer

classifiers = {
    "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=4),
    "RandomForestClassifier": RandomForestClassifier(n_estimators=10),
    "LogisticRegression": LogisticRegression(multi_class="ovr"),
    "Support Vector Classifier": SVC(kernel="linear", C=0.02),
}

df = pd.read_csv("../complete_complexity_measures.csv")

labels_type = df[["type"]]
y = labels_type.values.ravel()
X = df.iloc[:, 4:-3]

features = ['#total_events', '#events', '#traces', 'min_trace', 'max_trace',
       'avg_trace', 'l_detail', 'lz_compl', 'unique_t', 'struc', 'avg_aff',
       'dev_rand', '#ties', 'var_ent', 'nvar_ent', 'seq_ent',
       'nseq_ent']

min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X.values)
labels = np.unique(labels_type)

skf = StratifiedKFold(n_splits=4, shuffle=True)
summarized = []
imps = []
for i, (train_index, test_index) in enumerate(skf.split(X, y)):
    print(f"Fold {i}:")
    X_train = X[train_index]
    y_train = y[train_index]
    X_test = X[test_index]
    y_test = y[test_index]

    accuracies = []
    for i, (key, classifier) in enumerate(classifiers.items()):
        clf = classifier.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        if key == "DecisionTreeClassifier":
            imps.append(clf.feature_importances_)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        accuracies.append(round(accuracy, 3))

    summarized.append(accuracies)

df = pd.DataFrame(data=summarized)
print(df)
means = np.array(df.mean())
std = np.array(df.std())
print(list(np.round(means, 4)))
print(list(np.round(std, 4)))

df2 = pd.DataFrame(data=imps)
means2 = np.array(df2.mean())
std2 = np.array(df2.std())
print(list(np.round(means2, 4)))
print(list(np.round(std2, 4)))

with open('classifier_evaluation.csv', 'a', newline='') as file:
    writer_object = writer(file)
    writer_object.writerow(np.round(means, 4))
    file.close()



