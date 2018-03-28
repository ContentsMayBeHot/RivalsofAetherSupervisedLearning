import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten, Conv2D, MaxPooling2D, Reshape, GlobalAveragePooling2D, Conv1D, AveragePooling3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization

import loader

BATCH_SIZE = 1
CLASSES = 9
FILTERS = 4
INPUT_SHAPE = (None, 135, 240, 1)
POOL_SIZE = (1, 135, 240)
KERNEL_SIZE = (3, 3)
MODEL_FNAME = 'rival.h5'

def main():
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIConvLSTM2D'] = '2'
    # Display device information
    tf.Session(config=tf.ConfigProto(log_device_placement=True))
    tf.GPUOptions(per_process_gpu_memory_fraction=0.2)

    model = Sequential()
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            input_shape=INPUT_SHAPE,
            padding='same',
            return_sequences=True))
    model.add(BatchNormalization())
#     model.add(ConvLSTM2D(
#             filters=FILTERS,
#             kernel_size=KERNEL_SIZE,
#             padding='same',
#             return_sequences=True))
#     model.add(BatchNormalization())
#     model.add(ConvLSTM2D(
#             filters=FILTERS,
#             kernel_size=KERNEL_SIZE,
#             padding='same',
#             return_sequences=True))
#     model.add(BatchNormalization())
    model.add(AveragePooling3D(POOL_SIZE))
    model.add(Reshape((-1, FILTERS)))
    model.add(Dense(CLASSES, activation='sigmoid'))
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adadelta'
    )
    model.summary()

    roa = loader.ROALoader()

    # # Train model
    roa.load_training_set()
    training_sequence = roa.get_training_sequence(batch_size=BATCH_SIZE)
    model.fit_generator(
        generator=training_sequence,
        max_queue_size=1,
        workers=1,
        verbose=2)

    # Test model
    roa.load_testing_set()
    testing_sequence = roa.get_testing_sequence(batch_size=BATCH_SIZE)
    model.evaluate_generator(
        generator=testing_sequence,
        max_queue_size=1,
        workers=1)

    # Save model
    model.save(MODEL_FNAME)


if __name__ == '__main__':
    main()
