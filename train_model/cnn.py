from keras.optimizers import Adam
from train_model.model import PPM_Model
from keras.models import Sequential
from keras.layers import MaxPooling1D, Conv1D, Dense, Flatten, ReLU, BatchNormalization
import numpy as np


class CNN_Model(PPM_Model):
    def __init__(self, sequ: str, event: str, path: str):
        super().__init__(sequ, event, path)
        self.model = None
        self.type = "CNN"
        self.BATCH_SIZE = len(self.unique_events)

    def create(self):
        """
            Create of CNN-Model based on
        """
        if len(self.X_train.shape) != 3:
            self.X_train = np.reshape(self.X_train, (*self.X_train.shape, 1))
            self.X_test = np.reshape(self.X_test, (*self.X_test.shape, 1))

        print(self.X_train.shape[1:])
        model = Sequential()
        model.add(Conv1D(128, 10, padding='same', strides=1,
                         input_shape=self.X_train.shape[1:]))
        model.add(BatchNormalization())
        model.add(ReLU())
        model.add(MaxPooling1D(pool_size=2, strides=1, padding="same"))

        for i in range(4):
            model.add(Conv1D(128, 10, padding='same', strides=1))
            model.add(BatchNormalization())
            model.add(ReLU())
            model.add(MaxPooling1D(pool_size=2, strides=1, padding="same"))
        model.add(Flatten())
        model.add(Dense(len(self.unique_events), activation='softmax'))
        opt = Adam(learning_rate=0.001)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
        self.model = model
        self.model.summary()
