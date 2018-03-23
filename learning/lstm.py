import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, TimeDistributed, LSTM, Flatten, Conv2D, MaxPooling2D

import loader


def main():
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Display device information
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    # Data attributes
    nb_timesteps = 1  # TODO: Specify this
    img_u = 135
    img_v = 240
    img_channels = 1
    input_shape = (img_u, img_v, img_channels)
    kernel_size = (3, 3)
    pool_size = (2, 2)
    nb_classes = 9
    # Output file
    model_fname = 'rival.h5'
    # Data flow control
    batch_size = 1

    # Initialize loader
    roa = loader.ROALoader()

    # Create sequential model instance
    model = Sequential()

    # Convolutional LSTM test
    # model.add(TimeDistributed(
    #     Conv2D(1, kernel_size=kernel_size, activation='relu'),
    #     input_shape=input_shape))
    # model.add(TimeDistributed(
    #     Conv2D(1, kernel_size=kernel_size, activation='relu')))
    # model.add(TimeDistributed(
    #     MaxPooling2D(pool_size=kernel_size)))
    # model.add(TimeDistributed(
    #     Dropout(0.1)))
    # model.add(TimeDistributed(
    #     Flatten()
    # ))
    # model.add(LSTM(1))
    # model.add(Dense(16))
    # model.add(Dense(nb_classes))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])
    # model_fname = 'rival_conv2d-lstm.h5'

    # Basic test
    # model.add(Dense(units=32, input_shape=input_shape))
    # model.add(Dense(units=10))
    # model.add(Flatten())
    # model.add(Dense(units=nb_classes, activation='relu'))
    # model.add(Dense(units=nb_classes, activation='relu'))
    # model.add(Dense(units=nb_classes, activation='sigmoid'))
    # model.compile(optimizer='rmsprop',
    #               loss='categorical_crossentropy',
    #               metrics=['accuracy'])

    # LSTM test
    # model.add(LSTM(nb_classes, input_shape=input_shape, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(LSTM(nb_classes, input_shape=input_shape, return_sequences=True))
    # model.add(Dropout(0.1))
    # model.add(Flatten())
    # model.add(Dense(nb_classes, activation='softmax'))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer='adam',
    #               metrics=['accuracy'])
    # model_fname = 'rival_lstm.h5'

    # Conv2D test
    model.add(Conv2D(filters=16,
                    kernel_size=kernel_size,
                    activation='relu',
                    padding='same',
                    input_shape=input_shape))
    model.add(Conv2D(filters=16,
                     kernel_size=kernel_size,
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))

    model.add(Conv2D(filters=32,
                     kernel_size=kernel_size,
                     activation='relu',
                     padding='same'))
    model.add(Conv2D(filters=32,
                     kernel_size=kernel_size,
                     activation='relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(units=128,
                    activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=nb_classes,
                    activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                 optimizer='adam',
                 metrics=['accuracy'])
    model_fname = 'rival_conv2d.h5'

    # Print model summary
    model.summary()

    # Train model
    roa.load_training_set()
    seq = roa.get_training_sequence(batch_size=batch_size)
    model.fit_generator(seq)
    # for i in range(batches):
    #    print('Training [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_training_batch(n=batch_size)
    #    model.fit(x, y)

    # Test model
    roa.load_testing_set()
    seq = roa.get_testing_sequence(batch_size=batch_size)
    model.evaluate_generator(seq)
    # for i in range(batches):
    #    print('Testing [{}/{}]'.format(i+1, batches))
    #    x, y = roa.next_testing_batch(n=batch_size)
    #    model.evaluate(x, y)

    # Save model
    model.save(model_fname)


if __name__ == '__main__':
    main()
