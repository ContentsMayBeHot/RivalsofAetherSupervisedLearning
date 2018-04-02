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
CLIP_X_SHAPE = (CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
CLIP_Y_SHAPE = (CLIP_LENGTH, CLASSES)
BATCH_X_SHAPE = (1, CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
BATCH_Y_SHAPE = (1, CLIP_LENGTH, CLASSES)

FILTERS = 10
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
            batch_input_shape=BATCH_X_SHAPE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True))
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True
    ))
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
            print('\tTraining batch: {}/{}'.format(i+1, n))
            # Get a single replay
            batch = roa_loader.next_training_batch()
            if not batch:
                break
            batch_x, batch_y = batch
            batch_x = np.array(batch_x, dtype=np.int32)
            batch_y = np.array(batch_y, dtype=np.int32)
            # Get clips of the replay
            for j in range(0, batch_x.shape[0], CLIP_LENGTH):
                x_clip = batch_x[j:j+CLIP_LENGTH]
                y_clip = batch_y[j:j+CLIP_LENGTH]
                # Check if clip is required length
                if x_clip.shape[0] < CLIP_LENGTH:
                    continue
                timesteps = batch_x.shape[0] // 100
                print('\t\tClip: {}/{}'.format((j//100)+1, timesteps), end='\t')
                x_clip = x_clip.reshape(BATCH_X_SHAPE)
                y_clip = y_clip.reshape(BATCH_Y_SHAPE)
                scalars = model.train_on_batch(x_clip, y_clip)
                loss = scalars[0]
                accuracy = scalars[1]
                print('Loss: {0:.2f}'.format(loss), end='\t')
                print('Accuracy: {0:.2f}'.format(accuracy))
            # Reset LSTM for next video
            model.reset_states()
            print()
        print()

    # Test model
    testing_set_path = config['SETS']['PathToTesting']
    n = roa_loader.load_testing_set(testing_set_path)
    for i in range(n):
        print('Testing batch: {}/{}'.format(i+1, n))
        batch = roa_loader.next_testing_batch()
        if not batch:
            break
        batch_x, batch_y = batch
        batch_x = np.array(batch_x, dtype=np.int32)
        batch_y = np.array(batch_y, dtype=np.int32)
        for j in range(0, batch_x.shape, CLIP_LENGTH):
            x_clip = batch_x[j:j+CLIP_LENGTH]
            y_clip = batch_y[j:j+CLIP_LENGTH]
            # Check if clip is required length
            if x_clip.shape[0] < CLIP_LENGTH:
                continue
            timesteps = batch_x.shape[0] // 100
            print('\t\tClip: {}/{}'.format((j//100)+1, timesteps), end='\t')
            x_clip = x_clip.reshape(BATCH_X_SHAPE)
            y_clip = y_clip.reshape(BATCH_Y_SHAPE)
            scalars = model.test_on_batch(x_clip, y_clip)
            loss = scalars[0]
            accuracy = scalars[1]
            print('Loss: {0:.2f}'.format(loss), end='\t')
            print('Accuracy: {0:.2f}'.format(accuracy))
        # Reset LSTM for next video
        model.reset_states()
        print()
    print()

    # Save model
    model_path = os.path.join('..', 'models', MODEL_FNAME)
    model.save(model_path)

if __name__ == '__main__':
    main()
