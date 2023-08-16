from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import metrics

df = pd.read_csv("../complete_complexity_measures.csv")
labels_type = df[["type"]]
labels_best = df[["best"]]

X = df.iloc[:, 4:-3]
print(df)
print(df.columns)
feature_cols = X.columns

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels_type, test_size=0.3, random_state=42)

# Initialize a RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Fit the classifier on the training data
print(y_train[:5])
print(y_train.values[:5])
print(y_train.values.ravel()[:5])
clf.fit(X_train, y_train.values.ravel())

# Predict class probabilities on the test data
class_probs = clf.predict_proba(X_test)

# Print the predicted class probabilities for the first few samples
for probs in class_probs[:5]:
    for class_idx, prob in enumerate(probs):
        print(f"Class {class_idx}: {prob:.2f}")
    print()

y_pred = clf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

print(clf.feature_importances_)
