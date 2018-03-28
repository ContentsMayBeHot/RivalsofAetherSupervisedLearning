import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten, Conv2D, MaxPooling2D, Reshape, GlobalAveragePooling2D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization

import loader


def main():
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIConvLSTM2D'] = '2'
    # Display device information
    tf.Session(config=tf.ConfigProto(log_device_placement=True))
    # Data attributes
    input_shape = (None, 135, 240, 1)
    classes = 9
    # Output file
    model_fname = 'rival.h5'
    # Data flow control
    batch_size = 1

    # Initialize loader
    roa = loader.ROALoader()

    # Initialize Keras model
    model = Sequential()

    # Basic test
    # model.add(Dense(units=32, input_shape=input_shape))
    # model.add(Dense(units=10))
    # model.add(Flatten())
    # model.add(Dense(units=classes, activation='relu'))
    # model.add(Dense(units=classes, activation='relu'))
    # model.add(Dense(units=classes, activation='sigmoid'))
    # model.compile(optimizer='rmsprop',
    #               loss='categorical_crossentropy',
    #               metrics=['accuracy'])

    # LSTM test
    # model.add(LSTM(classes, input_shape=input_shape, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(LSTM(classes, input_shape=input_shape, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(Flatten())
    # model.add(Dense(classes, activation='softmax'))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])

    # Conv2D test
    # model.add(Conv2D(4,
    #                  kernel_size=(3, 3),
    #                  activation='relu',
    #                  input_shape=input_shape))
    # model.add(Conv2D(8,
    #                 kernel_size=(3, 3),
    #                 activation='relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
    # model.add(Flatten())
    # model.add(Dense(16, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(classes, activation='softmax'))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])

    # ConvLSTM test
    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            input_shape=input_shape,
            padding='same',
            data_format='channels_last',
            return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            padding='same',
            data_format='channels_last',
            return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            padding='same',
            data_format='channels_last'))
    model.add(BatchNormalization())

    model.add(GlobalAveragePooling2D(data_format='channels_last'))
    model.add(Dense(
            units=classes,
            activation='softmax'))

    model.compile(
            loss='categorical_crossentropy',
            optimizer='adadelta'
    )
    model.summary()

    # Train model
    roa.load_training_set()
    training_sequence = roa.get_training_sequence(batch_size=batch_size)
    model.fit_generator(generator=training_sequence)
    # for i in range(batches):
    #    print('Training [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_training_batch(n=batch_size)
    #    model.fit(x, y)

    # Test model
    roa.load_testing_set()
    testing_sequence = roa.get_testing_sequence(batch_size=batch_size)
    model.evaluate_generator(generator=testing_sequence)
    # for i in range(batches):
    #    print('Testing [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_testing_batch(n=batch_size)
    #    model.evaluate(x, y)

    # Save model
    model.save(model_fname)


if __name__ == '__main__':
    main()
