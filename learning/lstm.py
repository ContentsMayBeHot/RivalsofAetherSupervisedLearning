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
    epochs = 3
    batch_size = 5

    # Initialize loader
    roa = loader.ROALoader(autoload_training=True, autoload_testing=True)

    # Compile model
    model = Sequential()
    model.add(Dense(units=32, input_shape=input_shape))
    model.add(Dense(units=32, activation='sigmoid'))
    model.add(Flatten())
    model.add(Dense(units=classes, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Train model
    for e in range(epochs):
        print('Run [{}/{}]'.format(e+1, epochs))
        (x_train, y_train) = roa.next_testing_batch(n=batch_size)
        if y_train.size == 0:
            break
        model.train_on_batch(x_train, y_train)

    # Test model
    x_test, y_test = roa.next_testing_batch(n=batch_size)
    model.evaluate(x_test, y_test)

    # Save model
    model.save(model_fname)

if __name__ == '__main__':
    main()
