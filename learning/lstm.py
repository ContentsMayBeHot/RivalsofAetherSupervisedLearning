import os
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten

import loader

MODEL_FNAME = 'rival.h5'

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Turn off CPU feature warnings
    batch_size = 1
    input_shape = (135, 240, 3)
    num_classes = 26
    num_batches = 2

    # Initialize loader
    roa = loader.ReplayLoader()
    roa.load_training()
    roa.load_testing()

    # Compile model
    model = Sequential()
    model.add(Dense(units=32, input_shape=input_shape))
    model.add(Dense(units=10))
    model.add(Flatten())
    model.add(Dense(units=num_classes))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Train model
    x_train, y_train = roa.next_training_batch(n=num_batches)
    model.fit(x_train, y_train)

    # Test model
    x_test, y_test = roa.next_testing_batch(n=num_batches)
    model.evaluate(x_test, y_test)

    # Save model
    model.save(MODEL_FNAME)

if __name__ == '__main__':
    main()
