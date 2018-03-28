import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten, Conv2D, MaxPooling2D, Reshape, GlobalAveragePooling2D, Conv1D, AveragePooling3D
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

    # ConvLSTM test
    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            input_shape=input_shape,
            padding='same',
            return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            padding='same',
            return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(
            filters=40,
            kernel_size=(3, 3),
            padding='same',
            return_sequences=True))
    model.add(BatchNormalization())

    model.add(AveragePooling3D((1, 135, 240)))
    model.add(Reshape((-1, 40)))
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
