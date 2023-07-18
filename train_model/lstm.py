from keras.optimizers import Nadam
from sklearn.model_selection import StratifiedKFold

from train_model.utils import early_stopping, log_model, lr_reducer, log_epoch, log_history, remove_lower_accuracies

from train_model.model import PPM_Model
from keras.models import Sequential
from keras.layers import LSTM, BatchNormalization, Dense
import numpy as np

EPOCH_SIZE = 100


class LSTM_Model(PPM_Model):
    def __init__(self, sequ: str, event: str, path: str):
        super().__init__(sequ, event, path)
        self.model = None
        self.type = "LSTM"
        self.BATCH_SIZE = len(self.unique_events)

    def create(self):
        """
            Create of LSTM-Model based on N.Tax et.al. [23]
        """
        if len(self.X_train.shape) != 3:
            self.X_train = np.reshape(self.X_train, (self.X_train.shape[0], self.X_train.shape[1], 1))
            self.X_test = np.reshape(self.X_test, (self.X_test.shape[0], self.X_test.shape[1], 1))

        model = Sequential()
        model.add(LSTM(100, input_shape=self.X_train.shape[1:], return_sequences=True,
                       implementation=2, kernel_initializer='glorot_uniform', dropout=0.2))
        model.add(BatchNormalization())
        model.add(LSTM(100, implementation=2, kernel_initializer='glorot_uniform', dropout=0.2))
        model.add(Dense(len(self.unique_events), activation='softmax', kernel_initializer='glorot_uniform'))
        opt = Nadam(learning_rate=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, clipvalue=3)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
        self.model = model
        self.model.summary()

    def train(self):
        """
            - Training of LSTM-Model
            - Saves best model in '/data/models/{id}_{accuracy}.keras'
        """
        model_id = self.path.split('.')[0]
        training_path = f"data/training/{model_id}.csv"
        progress_path = f"data/training/{model_id}.txt"
        model_path = f"data/models/{model_id}_" + '{val_accuracy:.2f}.keras'

        skf = StratifiedKFold(n_splits=6, shuffle=True)

        for i, (train_index, validate_index) in enumerate(skf.split(self.X_train, self.Y_train.argmax(1))):
            print(f"Fold {i}:")
            self.create()
            self.model.fit(self.X_train[train_index], self.Y_train[train_index], batch_size=self.BATCH_SIZE,
                           epochs=EPOCH_SIZE,
                           validation_data=(self.X_train[validate_index], self.Y_train[validate_index]),
                           callbacks=[early_stopping, log_model(model_path), lr_reducer, log_history(training_path),
                                      log_epoch(progress_path)])

        remove_lower_accuracies(model_id, "keras")
