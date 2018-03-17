import os
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten

import loader

def main():
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Data attributes
    input_shape = (135, 240, 3)
    classes = 26
    # Output file
    model_fname = 'rival.h5'
    # Data flow control
    batches = 3
    batch_size = 1

    # Initialize loader
    roa = loader.ROALoader()

    # Compile model
    model = Sequential()
    model.add(Dense(units=32, input_shape=input_shape))
    model.add(Dense(units=10))
    model.add(Flatten())
    model.add(Dense(units=classes))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Train model
    roa.load_training_set()
    for i in range(batches):
        print('Training [{}/{}]'.format(i, batches))
        x, y = roa.next_training_batch(n=batch_size)
        model.fit(x, y)

    # Test model
    roa.load_testing_set()
    for i in range(batches):
        print('Testing [{}/{}]'.format(i+1, batches))
        x, y = roa.next_testing_batch(n=batch_size)
        model.fit(x, y)

    # Save model
    model.save(model_fname)

if __name__ == '__main__':
    main()
