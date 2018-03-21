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
    nb_classes = 9
    nb_timesteps = None  # TODO: Specify this
    img_height = 135
    img_width = 240
    img_colors = 1
    input_shape = (nb_timesteps, img_height, img_width, img_colors)
    # Output file
    model_fname = 'rival.h5'
    # Data flow control
    batch_size = 1

    # Initialize loader
    roa = loader.ROALoader()

    model = Sequential()

    model.add(TimeDistributed(
        Conv2D(8, kernel_size=(2, 2), activation='relu'),
        input_shape=input_shape))
    model.add(TimeDistributed(
        Conv2D(8, kernel_size=(2, 2), activation='relu')))
    model.add(TimeDistributed(
        MaxPooling2D(pool_size=(2, 2))))
    model.add(TimeDistributed(
        Dropout(0.1)))
    model.add(TimeDistributed(
        Flatten()
    ))
    model.add(LSTM(4))
    model.add(Dense(16))
    model.add(Dense(nb_classes))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()
    quit()


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

    # Conv2D test
    #model.add(Conv2D(4,
    #                 kernel_size=(3, 3),
    #                 activation='relu',
    #                 input_shape=input_shape))
    #model.add(Conv2D(8,
    #                kernel_size=(3, 3),
    #                activation='relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(Dropout(0.25))
    #model.add(Flatten())
    #model.add(Dense(16, activation='relu'))
    #model.add(Dropout(0.5))
    #model.add(Dense(nb_classes, activation='softmax'))
    #model.compile(loss='categorical_crossentropy',
    #              optimizer='adam',
    #              metrics=['accuracy'])

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
