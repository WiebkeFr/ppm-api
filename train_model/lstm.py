from keras.optimizers import Nadam
from train_model.model import PPMModel
from keras.models import Sequential
from keras.layers import LSTM, BatchNormalization, Dense
import numpy as np


class LSTM_Model(PPMModel):
    def __init__(self, sequ: str, event: str, path: str):
        super().__init__(sequ, event, path)
        self.model = None
        self.type = "LSTM"
        self.BATCH_SIZE = min(len(self.unique_events), 15)

    def create(self):
        """
            Creates an LSTM-Model based on N.Tax et.al. [23]
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
