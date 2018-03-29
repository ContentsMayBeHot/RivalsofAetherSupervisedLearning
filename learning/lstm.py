import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Reshape, GlobalAveragePooling2D, AveragePooling3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization

from loader import ROALoader

EPOCHS = 1
MODEL_FNAME = 'rival.h5'

IMG_U = 135
IMG_V = 240
IMG_C = 1
CLIP_LENGTH = 100
BATCH_SHAPE = (1, CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
CLASSES = 9

FILTERS = 8
POOL_SIZE = (1, 135, 240)
KERNEL_SIZE = (3, 3)

def main():
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIConvLSTM2D'] = '2'
    # Display device information
    tf.Session(config=tf.ConfigProto(log_device_placement=True))

    # Define ConvLSTM2D model
    model = Sequential()
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            batch_input_shape=BATCH_SHAPE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True))
    model.add(BatchNormalization())
    model.add(AveragePooling3D(POOL_SIZE))
    model.add(Reshape((-1, FILTERS)))
    model.add(Dense(CLASSES, activation='sigmoid'))
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adadelta',
            metrics=['accuracy']
    )
    model.summary()
    quit()

    roa = ROALoader()

    # # Train model
    n = roa.load_training_set()
    for e in range(EPOCHS):
        print('Epoch: {}/{}'.format(e+1, EPOCHS))
        for i in range(n):
            print('\tBatch: {}/{}'.format(i+1, n))
            # Get a single replay
            batch = roa.next_training_batch()
            if not batch:
                break
            x, y = batch
            x = np.array(x)  # (frames, 135, 240, 1)
            y = np.array(y)  # (frames, 9)
            # Get clips of the replay
            for j in range(0, x.shape[0], 100):
                x_clip = x[j:j+100]
                y_clip = y[j:j+100]
                scalars = model.train_on_batch(x_clip, y_clip)
            # Reset LSTM for next video
            model.reset_states()

    # Test model
    roa.load_testing_set()
    # TODO Testing loop

    # Save model
    model.save(MODEL_FNAME)


if __name__ == '__main__':
    main()
