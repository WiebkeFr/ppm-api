import os
import sys

from numpy import newaxis

from train_model.model import one_hot_enc
from train_model.utils import WINDOW_SIZE

sys.path.append("..")
import pandas as pd
import pm4py
import numpy as np
from evaluate_dataset.complexity import generate_pm4py_log

from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Input, BatchNormalization
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Masking
from keras.utils import to_categorical
from keras.metrics import Precision
from keras.utils import pad_sequences
from gensim.models import Word2Vec

from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics


id = '5c015e59-4369-44c1-8066-682048be81f5.xes'
SEQ_ENCODING = 'PREPAD'

path = os.path.join(os.pardir, "data", id)
log = pm4py.read_xes(path)

pm4py_log = generate_pm4py_log(path)
max_length = max([len(trace) for trace in pm4py_log])

all_events = log["concept:name"]
unique_events = np.unique(all_events.values)
event_encoding_dic = {}

def extract_labels(df):
    trace_df = df.groupby('case:concept:name', group_keys=False).apply(lambda x: x.sort_values(by=["time:timestamp"])['concept:name'].tolist())\
        .reset_index().drop(['index', 'case:concept:name'], axis=1, errors='ignore')
    X = []
    Y = []
    for index, row in trace_df.iterrows():
        trace = row[0]
        for i in range(len(trace)-1):
            if i >= WINDOW_SIZE - 1 and SEQ_ENCODING == 'CONT':
                encoded_trace = map(lambda x: event_encoding_dic[x], trace[i-WINDOW_SIZE+2:i+1])
                X.append(list(encoded_trace))
                Y.append(trace[i+1])
            else:
                encoded_trace = map(lambda x: event_encoding_dic[x], trace[:i+1])
                X.append(list(encoded_trace))
                Y.append(trace[i+1])
    X = pad_sequences(X, value=0.0, dtype=object)
    return X, Y

def encode_sequence(trace):
    if SEQ_ENCODING == 'PREPAD':
        encoded_trace = ['' for _ in range(max_length)]
        encoded_trace[-len(trace):] = trace
        return encoded_trace
    else:
        if len(trace) > WINDOW_SIZE:
            return trace[-WINDOW_SIZE:]
        else:
            empty_trace = ['' for _ in range(WINDOW_SIZE)]
            empty_trace[-len(trace):] = trace
            return empty_trace

def encode_prefix(df):
    sorted_event_of_case = df[["concept:name", "time:timestamp"]].sort_values(by=["time:timestamp"])
    none_value = np.array(sorted_event_of_case['concept:name'].iloc[0]) * 0
    encode_cases = [none_value for x in range(max_length)]
    encode_cases[-len(sorted_event_of_case):] = sorted_event_of_case['concept:name']
    return pd.Series(data = encode_cases)

def continous_prefix(df):
    sorted_event_with_case = df[["concept:name", "time:timestamp"]].sort_values(by=["time:timestamp"])
    sorted_events = sorted_event_with_case['concept:name'].values
    length_of_sequ = len(sorted_events)
    encode_cases = [pd.Series(sorted_events[x: x + WINDOW_SIZE]) for x in range(length_of_sequ - WINDOW_SIZE + 1)]
    return pd.DataFrame(data = encode_cases)


def number_encoding():
    for case, index in zip(unique_events, range(len(unique_events))):
        event_encoding_dic[case] = index * 1.

def freq_encoding(df):
    corpus = ['This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
        ]

    corpus2 = df.groupby('case:concept:name', group_keys=False).apply(lambda x: x.sort_values(by=["time:timestamp"])['concept:name'].tolist())\
        .reset_index().drop(['case:concept:name'], axis=1, errors='ignore')
    corpus2 = corpus2[0].tolist()
    print(corpus2)

    cases = df["concept:name"]
    unique_cases = np.unique(cases.values)
    cases = np.reshape(cases, (len(cases), 1))

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()
    print(X)


event_encoding_dic = one_hot_enc(unique_events)
X, Y = extract_labels(log)

# X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
Y = list(map(lambda y: event_encoding_dic[y], Y))

X = np.asarray(X).astype('float32')
Y = np.asarray(Y).astype('float32')

X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.4, random_state=42)
split_index = round(len(X_test) / 2)

X_validate = X_test[:split_index]
Y_validate = Y_test[:split_index]

X_test = X_test[split_index:]
Y_test = Y_test[split_index:]

BATCH_SIZE = 50
EPOCH_SIZE = 20

model = Sequential()
# model.add(Input(shape=(X.shape[1], X.shape[2], X.shape[3])))
# model.add(Masking(mask_value=0.))
model.add(LSTM(100, input_shape=(X.shape[1], X.shape[2]), return_sequences=True, implementation=2, kernel_initializer='glorot_uniform'))
model.add(BatchNormalization())
model.add(LSTM(100, implementation=2, kernel_initializer='glorot_uniform'))
model.add(Dense(len(unique_events), activation='softmax'))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.summary()
history = model.fit(X_train, Y_train, batch_size=BATCH_SIZE, epochs=EPOCH_SIZE, validation_data=(X_validate,Y_validate))
results = model.evaluate(X_test, Y_test, batch_size=round(BATCH_SIZE / 2))

def DF():
    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier()

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, Y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))



