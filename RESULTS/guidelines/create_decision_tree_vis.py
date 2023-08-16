import pickle
from io import StringIO

import pandas as pd
from sklearn import tree

path = "decision_tree_technique.sav"
clf = pickle.load(open(path, 'rb'))
scaler = pickle.load(open("min_max_scaler.sav", 'rb'))

used_features = ['#total_events', '#events', '#traces', 'max_trace', 'avg_trace', 'l_detail', 'lz_compl', 'unique_t', 'struc', 'avg_aff', 'nvar_ent', 'seq_ent']

dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,feature_names = used_features,class_names=['LSTM','CNN','DT'])

print(dot_data.getvalue())

df = pd.read_csv("../complete_complexity_measures.csv")
df = df[used_features]
print(df)

example_row = list(df.iloc[5])
example_row2 = list(df.iloc[7])
example_row3 = list(df.iloc[42])

scaled_row = scaler.transform([example_row])
scaled_row2 = scaler.transform([example_row2])
scaled_row3 = scaler.transform([example_row3])
scaled_df = scaler.transform(df)


print(example_row)
pred_result = clf.predict(scaled_row)
pred_result_proba = clf.predict_proba(scaled_row)
print(pred_result_proba)
print(pred_result)

print(example_row2)
pred_result2 = clf.predict(scaled_row2)
pred_result_proba2 = clf.predict_proba(scaled_row2)
print(pred_result_proba2)
print(pred_result2)

print(example_row3)
print(example_row3)
print(scaled_df)
pred_result3 = clf.predict(scaled_row3)
pred_result_proba3 = clf.predict_proba(scaled_row3)


pred_result4 = clf.predict(scaled_df)
pred_result_proba4 = clf.predict_proba(scaled_df)
print(pred_result4)
