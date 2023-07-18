from keras.optimizers import Adam
from sklearn.model_selection import StratifiedKFold

from train_model.model import PPM_Model
from keras.models import Sequential
from keras.layers import MaxPooling1D, Conv1D, Dense, Flatten, ReLU, BatchNormalization
from train_model.utils import early_stopping, log_model, lr_reducer, log_epoch, log_history, remove_lower_accuracies
import numpy as np

BATCH_SIZE = 20
EPOCH_SIZE = 100


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

    def train(self):
        """
            - Training of CNN-Model
            - Saves best model in '/data/models/{id}_{accuracy}.keras'
        """
        model_id = self.path.split('.')[0]
        model_path = f"data/models/{model_id}_" + '{val_accuracy:.2f}.keras'
        training_path = f"data/training/{model_id}.csv"
        progress_path = f"data/training/{model_id}.txt"

        skf = StratifiedKFold(n_splits=6, shuffle=True)

        for i, (train_index, validate_index) in enumerate(skf.split(self.X_train, self.Y_train.argmax(1))):
            print(f"Fold {i}:")
            self.create()
            self.model.fit(self.X_train[train_index], self.Y_train[train_index], batch_size=BATCH_SIZE, epochs=EPOCH_SIZE,
                                validation_data=(self.X_train[validate_index], self.Y_train[validate_index]),
                      callbacks=[early_stopping, log_model(model_path), lr_reducer, log_history(training_path),
                                 log_epoch(progress_path)]
                      )

        remove_lower_accuracies(model_id, "keras")

