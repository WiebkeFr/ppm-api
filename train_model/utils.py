import json
import os
from os.path import isfile, join
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, CSVLogger, LambdaCallback
from gensim.models import Word2Vec
from keras.utils import pad_sequences
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

WINDOW_SIZE = 4

##
## CALLBACKS AND LOGGING
##

early_stopping = EarlyStopping(monitor='val_loss', patience=3)
lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=0, mode='auto',
                               min_delta=0.0003, cooldown=0, min_lr=0)


def log_state(progress_path: str, state: str):
    """
    Writes 'state' in file.
    If file is not empty, the content is overwritten.

    Args:
        progress_path (string): path to file
        state (string): string to be written in file
    """
    with open(progress_path, 'w') as f:
        f.write(state)
        f.close()


def log_model(path):
    return ModelCheckpoint(path, monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=False,
                           mode='auto')


def log_history(path):
    return CSVLogger(path, separator=',', append=True)


def log_epoch(path):
    return LambdaCallback(on_epoch_end=lambda epoch, _: log_state(path, str(epoch)))


##
## ENCODING FUNCTION
##

def one_hot_enc(unique_events):
    """
    Returns a dictionary to encode event-names using One-Hot-Encoding

    Args:
        unique_events (Array): Array of unique event-names (str)

    Returns:
        event_encoding_dic (Dictionary):
            Dictionary to map event-names on array of numbers (length equals number of events)
    """
    reshaped_cases = np.reshape(unique_events, (len(unique_events), 1))
    enc = OneHotEncoder()
    enc_data = enc.fit_transform(reshaped_cases).toarray()
    event_encoding_dic = {}
    for case, enc_case in zip(unique_events, enc_data):
        event_encoding_dic[case] = list(enc_case)
    return event_encoding_dic


def embedded_encoding(log):
    """
    Returns a dictionary to encode event-names using Word2Vec
        (more infomation: https://radimrehurek.com/gensim/models/word2vec.html)

    Args:
        log (DataFrame): Dataframe of events (rows) of a process log with the following columns
                            'concept:name': name of event
                            'case:concept:name': trace/case of event
                            'time:timestamp': timestamp of event

    Returns:
        event_encoding_dic (Dictionary): Dictionary to map event-names on array of numbers
    """
    all_events = log["concept:name"]
    unique_events = np.unique(all_events.values)
    traces = log.groupby('case:concept:name', group_keys=False).apply(collect_events)\
        .reset_index().drop(['case:concept:name'], axis=1, errors='ignore')
    model = Word2Vec(sentences=traces[0].tolist(), vector_size=len(unique_events), window=3, min_count=1, workers=4)
    model.train([unique_events.tolist()], total_examples=1, epochs=1)
    event_encoding_dic = {}
    for case in unique_events:
        event_encoding_dic[case] = list(map(lambda x: np.float64(x), list(model.wv[case])))
    return event_encoding_dic


def extract_labels(log, event_encoding_dic, sequ_enc, event_enc, path):
    """
    Returns the encoded X-Data and Y-Label to train model

    Args:
        log (DataFrame): Dataframe of events (rows) of a process log with the following columns
                            'concept:name': name of event
                            'case:concept:name': trace/case of event
                            'time:timestamp': timestamp of event
        event_encoding_dic (Dictionary): Dictionary to encode event-names (key) to pre-determined array of numbers
        sequ_enc (String): Type of sequence encoding ('PREPAD' or 'CONT')
        event_enc (String) Type of event encoding ('ONEHOT' or 'EMBEDDED' or 'FREQBASED')

    Returns:
        X (Array): Array of encoded traces
        Y (Array): Array of encoded labels
    """
    trace_df = log.groupby('case:concept:name', group_keys=False).apply(collect_events) \
        .reset_index().drop(['index', 'case:concept:name'], axis=1, errors='ignore')
    X = []
    Y = []

    for index, row in trace_df.iterrows():
        trace = row[0]

        for i in range(len(trace) - 1):
            # Trace encoding
            if i >= WINDOW_SIZE - 1 and sequ_enc == 'CONT':
                encoded_trace = map(lambda x: event_encoding_dic[x], trace[i - WINDOW_SIZE + 2:i + 1])
                X.append(list(encoded_trace))
                Y.append(trace[i + 1])
            else:
                encoded_trace = map(lambda x: event_encoding_dic[x], trace[:i + 1])
                X.append(list(encoded_trace))
                Y.append(trace[i + 1])

    if event_enc == 'FREQBASED':
        corpus = list(map(lambda x: ' '.join(x), X))
        all_events = log["concept:name"]
        unique_events = np.unique(all_events.values)
        lens = [len(x.split()) for x in unique_events]
        vectorizer = CountVectorizer(vocabulary=unique_events, preprocessor=lambda x: x,
                                     token_pattern='[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+', lowercase=False,
                                     ngram_range=(1, max(lens)))
        print(corpus[:5])
        X = vectorizer.fit_transform(corpus).toarray()
        print(X[:5])

    else:
        X = pad_sequences(X, value=0.0, dtype=object)

    X = np.asarray(X).astype('float32')

    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(Y)
    labels = list(label_encoder.classes_)
    transform_classes = label_encoder.transform(labels)

    label_encoding_dic = {}
    for label, transform_class in zip(labels, transform_classes):
        label_encoding_dic[label] = str(transform_class)

    dic_path = os.path.join(os.curdir, "data", "encodings", path.split('.')[0] + '_label' + '.json')
    with open(dic_path, "w") as outfile:
        json.dump(label_encoding_dic, outfile)
        outfile.close()

    return X, Y


#
# HELPER FUNCTIONS
#
def remove_lower_accuracies(id, ending):
    """
    Deletes all model-files which do not score the maximal accuracy
    -> only the best model is kept

    Args:
        id (String): id of model
        ending (String): file type of the model (keras or sav)
    """
    file_names = [f for f in os.listdir("data/models/") if isfile(join("data/models/", f)) and (id in f)]
    model_accuracies = [file_name.split("_")[-1].rsplit(".", 1)[0] for file_name in file_names]
    max_accuracy = max(list(model_accuracies), default=0)

    for f in file_names:
        if not (f == f"{id}_{str(max_accuracy)}.{ending}"):
            print(f"remove {f}")
            os.remove(f"data/models/{f}")


def collect_events(trace):
    """
    Generates a list of events based on the given trace

    Args:
        trace (DataFrame):  Dataframe of events with the columns
                            'concept:name': name of event
                            'time:timestamp': timestamp of event (optional)
    Returns:
        x (list): list of event-names
    """
    if "time:timestamp" in trace:
        return trace.sort_values(by=["time:timestamp"])['concept:name'].tolist()
    return trace['concept:name'].tolist()