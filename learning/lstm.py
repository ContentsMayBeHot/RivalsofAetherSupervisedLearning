import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten

import loader

def main():
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Data attributes
    input_shape = (135, 240)
    classes = 9
    # Output file
    model_fname = 'rival.h5'
    # Data flow control
    batch_size = 1

    # Initialize loader
    roa = loader.ROALoader()

    # Compile model
    # model = Sequential()
    # model.add(Dense(units=32, input_shape=input_shape))
    # model.add(Dense(units=10))
    # model.add(Flatten())
    # model.add(Dense(units=classes, activation='relu'))
    # model.add(Dense(units=classes, activation='relu'))
    # model.add(Dense(units=classes, activation='sigmoid'))
    # model.compile(optimizer='rmsprop',
    #               loss='categorical_crossentropy',
    #               metrics=['accuracy'])

    #LSTM Test
    model = Sequential()
    model.add(LSTM(classes, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.1))
    model.add(LSTM(classes, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.1))
    model.add(Flatten())
    model.add(Dense(classes,activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train model
    roa.load_training_set()
    seq = roa.get_training_sequence(batch_size=batch_size)
    model.fit_generator(seq)
    #for i in range(batches):
    #    print('Training [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_training_batch(n=batch_size)
    #    model.fit(x, y)

    # Test model
    roa.load_testing_set()
    seq = roa.get_testing_sequence(batch_size=batch_size)
    model.evaluate_generator(seq)
    #for i in range(batches):
    #    print('Testing [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_testing_batch(n=batch_size)
    #    model.evaluate(x, y)

    # Save model
    model.save(model_fname)

if __name__ == '__main__':
    main()
