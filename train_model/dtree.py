import csv
import os
import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

from train_model.model import PPM_Model
from train_model.utils import remove_lower_accuracies


class DT_Model(PPM_Model):
    """
    https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    """
    def __init__(self, sequ: str, event: str, path: str):
        super().__init__(sequ, event, path)
        self.type = "DT"


    def create(self):
        """
            Create of DT-Model based on
        """
        if len(self.X_train.shape) != 2:
            samples, nx, ny = self.X_train.shape
            self.X_train = self.X_train.reshape((samples, nx * ny))
            samples, nx, ny = self.X_test.shape
            self.X_test = self.X_test.reshape((samples, nx * ny))

    def train(self, evaluate: bool):
        """
            - Training of Decision Tree
            - Saves best model in '/data/models/{id}_{accuracy}.keras'

        Args:
            evaluate (bool): shows whether all trees are evaluated after training
        """
        id = self.path.split('.')[0]
        training_path = f"data/training/{id}.csv"
        skf = StratifiedKFold(n_splits=6, shuffle=True)
        self.create()

        data = []
        for i, (train_index, validate_index) in enumerate(skf.split(self.X_train, self.Y_train.argmax(1))):
            for cr in ['gini', 'entropy', 'log_loss']:
                clf = DecisionTreeClassifier(criterion=cr)
                clf = clf.fit(self.X_train[train_index], self.Y_train[train_index])

                Y_pred = clf.predict(self.X_train[validate_index])
                accuracy = metrics.accuracy_score(self.Y_train[validate_index], Y_pred)
                precision = metrics.precision_score(self.Y_train[validate_index], Y_pred, average="weighted", zero_division=0.0)
                recall = metrics.recall_score(self.Y_train[validate_index], Y_pred, average="weighted", zero_division=0.0)
                f1 = metrics.f1_score(self.Y_train[validate_index], Y_pred, average='weighted', zero_division=0.0)

                model_path = f"data/models/{id}_{round(accuracy, 2)}.sav"
                pickle.dump(clf, open(model_path, 'wb'))
                data.append([f"Fold {i}", cr, accuracy, precision, recall, f1])

        with open(training_path, "a") as stream:
            writer = csv.writer(stream)
            writer.writerow(["Fold", "Criterion", "Accuracy", "Precision", "Recall", "F1"])
            writer.writerows(data)

        remove_lower_accuracies(id, "sav")
        return data

    def evaluate_history(self):
        """
            - Show accuracies, precision and recall per fold in diagram
            - Generates and saves line graph at 'data/results/{id}_history.svg'
        """
        plt.close()
        model_id = self.path.split('.')[0]
        result_path = f"data/results/{model_id}_history.svg"
        history_path = f'data/training/{model_id}.csv'

        if not os.path.isfile(history_path):
            return

        df = pd.read_csv(history_path)

        labels = np.unique(df["Criterion"])
        ind = np.arange(len(labels))

        columns = ['Accuracy', 'Precision', 'Recall']
        colors = ['blue', 'orange', 'green']
        width = 0.23

        fig, ax = plt.subplots()
        ax.set_xticks(ind + width, labels=labels)

        for index, (column, color) in enumerate(zip(columns, colors)):
            df_grouped = (
                df[['Criterion', column]].groupby(['Criterion'])
                .agg(['mean', 'std'])
            )
            df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
            ax.bar(ind + index * width, df_grouped["mean"], width, yerr=df_grouped["std"], label=column)

        title = "Evaluation of model in each criterion"
        plt.title(title, fontsize=13)
        plt.xlabel('Criterion', fontsize=12)
        plt.ylabel('Percentage', fontsize=12)
        plt.ylim(top=1.05)
        plt.grid(axis='y')
        plt.legend(loc='lower right')
        plt.savefig(result_path)
        plt.close()