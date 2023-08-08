import json
import os
import pickle
from time import time
from os import listdir
from os.path import isfile, join
import pandas as pd
from keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pm4py
from sklearn.model_selection import train_test_split
from keras.models import load_model
from evaluate_dataset.complexity import generate_pm4py_log
from train_model.utils import embedded_encoding, one_hot_enc, extract_labels
from sklearn.model_selection import StratifiedKFold
from train_model.utils import early_stopping, log_model, lr_reducer, log_epoch, log_history, remove_lower_accuracies
from sklearn import metrics

matplotlib.use('agg')

EPOCH_SIZE = 100


class PPMModel:
    def __init__(self, sequ_enc: str, event_enc: str, path: str):
        """
            - Initializing of additional information for models
            - Encoding of events according selected type ('ONEHOT' or 'EMBEDDED' or 'FREQBASED')
            - Encoding of traces according selected type ('PREPAD' or 'CONT')
            - Preprocessing the data into traces (X) and next event (Y)
            - Split data into training-data (0.6), validation-data (0.2) and testing-data (0.2)
        """
        if path == "DEFAULT":
            return

        self.sequ = sequ_enc
        self.event = event_enc

        self.path = path
        self.log = []
        self.unique_events = []
        self.event_encoding_dic = {}
        self.X_train = []
        self.Y_train = []
        self.X_test = []
        self.Y_test = []

        log_path = os.path.join(os.curdir, "data", "logs", path)
        self.log = pd.read_csv(log_path) if path.split(".")[-1] == "csv" else pm4py.read_xes(log_path)
        if path.split(".")[-1] == "csv":
            self.log.rename(columns={self.log.columns[0]: 'case:concept:name', self.log.columns[1]: 'concept:name',
                                     self.log.columns[2]: 'time:timestamp'}, inplace=True)
        if self.log.dtypes["case:concept:name"] != "str":
            self.log["case:concept:name"] = self.log["case:concept:name"].apply(str)
        if self.log.dtypes["concept:name"] != "str":
            self.log["concept:name"] = self.log["concept:name"].apply(str)

        # Prepare event encoding
        all_events = self.log["concept:name"]
        self.unique_events = np.unique(all_events.values)
        if event_enc == 'EMBEDDED':
            self.event_encoding_dic = embedded_encoding(self.log)
        elif event_enc == 'FREQBASED':
            event_encoding_dic = {}
            for event_name in self.unique_events:
                event_encoding_dic[event_name] = event_name
            self.event_encoding_dic = event_encoding_dic
        else:
            self.event_encoding_dic = one_hot_enc(self.unique_events)

        dic_path = os.path.join(os.curdir, "data", "encodings", path.split('.')[0] + '.json')
        with open(dic_path, "w") as outfile:
            json.dump(self.event_encoding_dic, outfile)

        # Preprocess data
        X, Y = extract_labels(self.log, self.event_encoding_dic, sequ_enc, event_enc, path)

        # Data-splitting
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # convert label vector to categorical values
        self.Y_train = to_categorical(self.Y_train, len(self.unique_events))

    def create(self):
        """
            Default function which needs to be replaced
        """
        raise Exception("No type of model is provided")

    def train(self, evaluate: bool):
        """
            - Training of LSTM- or CNN-Model
            - Saves best model in '/data/models/{id}_{accuracy}.keras'

        Args:
            evaluate (bool): shows whether all epochs are evaluated after training
        """
        model_id = self.path.split('.')[0]
        training_path = f"data/training/{model_id}.csv"
        progress_path = f"data/training/{model_id}.txt"
        model_path = f"data/models/{model_id}_" + '{val_accuracy:.2f}.keras'
        scores = []
        skf = StratifiedKFold(n_splits=5, shuffle=True)

        for i, (train_index, validate_index) in enumerate(skf.split(self.X_train, self.Y_train.argmax(1))):
            print(f"Fold {i}:")
            if i > 2:
                break

            start_time = time()
            self.create()
            self.model.fit(self.X_train[train_index], self.Y_train[train_index], batch_size=self.BATCH_SIZE,
                           epochs=EPOCH_SIZE,
                           validation_data=(self.X_train[validate_index], self.Y_train[validate_index]),
                           callbacks=[early_stopping, log_model(model_path), lr_reducer, log_history(training_path),
                                      log_epoch(progress_path)])
            end_time = time()

            if evaluate:
                y_pred = self.model.predict(self.X_test, verbose=0)
                Y_pred = np.argmax(y_pred, axis=1)

                accuracy = metrics.accuracy_score(self.Y_test, Y_pred)
                precision = metrics.precision_score(self.Y_test, Y_pred, average="weighted", zero_division=0.0)
                recall = metrics.recall_score(self.Y_test, Y_pred, average="weighted", zero_division=0.0)
                f1 = metrics.f1_score(self.Y_test, Y_pred, average='weighted', zero_division=0.0)

                scores.append([accuracy, precision, recall, f1, end_time - start_time])

        remove_lower_accuracies(model_id, "keras")
        return scores

    def evaluate_test_prediction(self):
        """
            - Determines best saved model
            - Evaluates model with test data (X_test and y_test)
            - Generates and saves confusion-matrix in 'data/results/{id}_matrix.svg'
            - Calculation of classification report with test data 'data/results/{id}_report.json'
        """
        model_id = self.path.split('.')[0]
        result_path = f"data/results/{model_id}_matrix.svg"
        encoding_path = f"data/encodings/{model_id}_label.json"

        y_pred = []

        file_name = [f for f in listdir("data/models/") if isfile(join("data/models/", f)) and (model_id in f)][0]
        model_path = f"data/models/{file_name}"

        if self.type == "DT":
            model = pickle.load(open(model_path, 'rb'))
            y_pred = model.predict(self.X_test)
            y_pred = np.argmax(y_pred, axis=1)
        else:
            model = load_model(model_path)
            y_pred = model.predict(self.X_test, verbose=0)
            y_pred = np.argmax(y_pred, axis=1)

        reversed_encoding = {}
        with open(encoding_path) as f:
            encoding = json.load(f)
            reversed_encoding = {v: k for k, v in encoding.items()}

        labeled_test = list(map(lambda x: reversed_encoding[str(x)], self.Y_test))
        labeled_pred = list(map(lambda y: reversed_encoding[str(y)], y_pred))
        labels = list(map(lambda l: reversed_encoding[str(l)], np.unique(self.Y_test)))

        # Plot confusion matrix
        title = "Confusion Matrix"
        fig, ax = plt.subplots()
        ConfusionMatrixDisplay.from_predictions(
            labeled_test,
            labeled_pred,
            normalize='true',
            display_labels=labels,
            xticks_rotation=45,
            ax=ax,
        )
        ax.set_title(title)
        plt.rcParams.update({'font.size': 14})
        ax.set_xticklabels(labels=labels, rotation=40, ha="right")
        plt.tight_layout()
        plt.savefig(result_path, pad_inches=5)
        plt.close()

        # create classification report with previously predicted values
        report_path = f"data/results/{model_id}_report.json"
        report = classification_report(labeled_test, labeled_pred, target_names=labels, output_dict=True)
        with open(report_path, 'w') as fp:
            json.dump(report, fp)

    def evaluate_history(self):
        """
            - Evaluates training accuracies and testing accuracies per epoch (for LSTMs and CNNs)
            - Generates and saves line graph at 'data/results/{id}_history.svg'
        """
        plt.close()
        model_id = self.path.split('.')[0]
        result_path = f"data/results/{model_id}_history.svg"
        history_path = f'data/training/{model_id}.csv'

        if not os.path.isfile(history_path):
            return

        df = pd.read_csv(history_path)

        for value in ['accuracy', 'val_accuracy']:
            color = "blue" if value == 'accuracy' else 'orange'
            label = "Training" if value == 'accuracy' else 'Validation'

            df_grouped = (
                df[['epoch', value]].groupby(['epoch'])
                .agg(['mean', 'std', 'count'])
            )
            df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
            df_grouped['ci'] = 1.96 * df_grouped['std'] / np.sqrt(df_grouped['count'])
            df_grouped['ci_lower'] = (df_grouped['mean'] - df_grouped['ci']).clip(0, 1)
            df_grouped['ci_upper'] = (df_grouped['mean'] + df_grouped['ci']).clip(0, 1)

            plt.plot(df_grouped["epoch"], df_grouped["mean"], '-', label=label, color=color)
            plt.fill_between(
                df_grouped["epoch"], df_grouped['ci_lower'], df_grouped['ci_upper'], color=color, alpha=.15)

        title = "Model Accuracy per Epoch"
        plt.title(title, fontsize=13)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel("Accuracy", fontsize=12)
        plt.ylim(bottom=0, top=1.05)
        plt.grid(True)
        plt.legend(loc='lower right')
        plt.savefig(result_path)
        plt.close()
