import pickle
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics, preprocessing
import numpy as np

df = pd.read_csv("../complete_complexity_measures.csv")
labels_type = df[["type"]]
labels_best = df[["best"]]

X = df.iloc[:, 4:-3]

used_features = ['#total_events', '#events', '#traces', 'max_trace', 'avg_trace', 'l_detail', 'lz_compl', 'unique_t', 'struc', 'avg_aff', 'nvar_ent', 'seq_ent']

X = X[used_features]
feature_cols = X.columns
min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X.values)
model_path = f"min_max_scaler.sav"

pickle.dump(min_max_scaler, open(model_path, 'wb'))

y = np.array(labels_type)

skf = StratifiedKFold(n_splits=4, shuffle=True)
accuracies = []
for i, (train_index, test_index) in enumerate(skf.split(X, y)):
    print(f"Fold {i}:")
    X_train = X[train_index]
    y_train = y[train_index]
    X_test = X[test_index]
    y_test = y[test_index]

    # Train Decision Tree Classifer
    clf = DecisionTreeClassifier(max_depth=3).fit(X_train, y_train)
    # Predict the response for test dataset
    y_pred = clf.predict(X_test)
    print(clf.feature_importances_)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    model_path = f"fold{i}_{round(accuracy, 3)}_reduced_5_fold.sav"
    pickle.dump(clf, open(model_path, 'wb'))

print(accuracies)
print(np.mean(accuracies))
