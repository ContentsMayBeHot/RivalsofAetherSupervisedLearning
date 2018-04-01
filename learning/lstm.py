import configparser
import os
import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Reshape, GlobalAveragePooling2D, AveragePooling3D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization

from loader import ROALoader
import utilities as utls

EPOCHS = 1
MODEL_FNAME = 'rival.h5'

CLASSES = 9
IMG_U = 135
IMG_V = 240
IMG_C = 1
CLIP_LENGTH = 100
X_CLIP_SHAPE = (CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
Y_CLIP_SHAPE = (CLIP_LENGTH, CLASSES)
X_BATCH_SHAPE = (1, CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
Y_BATCH_SHAPE = (1, CLIP_LENGTH, CLASSES)

FILTERS = 8
POOL_SIZE = (1, 135, 240)
KERNEL_SIZE = (3, 3)

def main():
    # Read ini file
    config = configparser.ConfigParser()
    config.read(os.path.join('..', 'config.ini'))
    # Turn off CPU feature warnings
    os.environ['TF_CPP_MIConvLSTM2D'] = '2'
    # Display device information
    tf.Session(config=tf.ConfigProto(log_device_placement=True))

    # Define ConvLSTM2D model
    model = Sequential()
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            batch_input_shape=X_BATCH_SHAPE,
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

    # Instantiate batch loader
    roa_loader = ROALoader()

    # Train model
    training_set_path = config['SETS']['PathToTraining']
    n = roa_loader.load_training_set(training_set_path) 
    for e in range(EPOCHS):
        print('Epoch: {}/{}'.format(e+1, EPOCHS))
        for i in range(n):
            print('\tBatch: {}/{}'.format(i+1, n))
            # Get a single replay
            batch = roa_loader.next_training_batch()
            if not batch:
                break
            x, y = batch
            x = np.array(x, dtype=np.int32)
            y = np.array(y, dtype=np.int32)
            # Get clips of the replay
            for j in range(0, x.shape[0], CLIP_LENGTH):
                x_clip = x[j:j+CLIP_LENGTH]
                y_clip = y[j:j+CLIP_LENGTH]
                # Check if clip is required length
                if x_clip.shape[0] < CLIP_LENGTH:
                    continue # Drop clip
                    x_clip, y_clip = utls.pad_clip(
                            x_clip, X_CLIP_SHAPE,
                            y_clip, Y_CLIP_SHAPE)
                x_clip = x_clip.reshape(X_BATCH_SHAPE)
                y_clip = y_clip.reshape(Y_BATCH_SHAPE)
                scalars = model.train_on_batch(x_clip, y_clip)
                print(scalars)
            # Reset LSTM for next video
            model.reset_states()

    # Test model
    testing_set_path = config['SETS']['PathToTesting']
    roa_loader.load_testing_set(testing_set_path)
    # TODO Testing loop

    # Save model
    model_path = os.path.join('..', 'models', MODEL_FNAME)
    model.save(model_path)

if __name__ == '__main__':
    main()
