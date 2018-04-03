import configparser
import datetime as dt
import os
import numpy as np
import pandas as pd
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Reshape, GlobalAveragePooling2D, AveragePooling3D  # noqa
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

    # Instantiate batch loader
    roa_loader = ROALoader()
    # Load training set
    training_set_path = config['SETS']['PathToTraining']
    train_n = roa_loader.load_training_set(training_set_path)
    # Load testing set
    testing_set_path = config['SETS']['PathToTesting']
    test_n = roa_loader.load_testing_set(testing_set_path)

    # Define ConvLSTM2D model
    model = Sequential()
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            batch_input_shape=BATCH_X_SHAPE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True
    ))  # noqa
    model.add(BatchNormalization())
    model.add(ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True
    ))  # noqa
    model.add(BatchNormalization())
    model.add(AveragePooling3D(POOL_SIZE))
    model.add(Reshape((-1, FILTERS)))
    model.add(Dense(CLASSES, activation='sigmoid'))
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adadelta',
            metrics=['accuracy']
    )  # noqa
    model.summary()
    print()

    # Train model
    train_data = []
    for e in range(EPOCHS):
        print('Epoch: {}/{}'.format(e + 1, EPOCHS))
        for i in range(train_n):
            utls.print_label('\tTraining Batch', '{}/{}', [i + 1, train_n])
            # Get a single replay
            batch = roa_loader.next_training_batch()
            if not batch:
                break
            batch_x, batch_y = utls.generate_batches(batch)
            timesteps = batch_x.shape[0] // 100
            # Get clips of the replay
            clips = utls.generate_clips(
                    batch_x, batch_y,
                    BATCH_X_SHAPE, BATCH_Y_SHAPE,
                    CLIP_LENGTH)  # noqa
            batch_scalars = utls.run_method(model.train_on_batch, clips, timesteps)  # noqa
            for clip, (loss, accuracy) in enumerate(batch_scalars):
                train_data.append([e + 1, i + 1, clip + 1, loss, accuracy])
            model.reset_states()
            print()
            break
        print()

    # Save training CSV
    train_cols = ['Epoch', 'Replay', 'Clip', 'Loss', 'Accuracy']
    train_df = pd.DataFrame(data=train_data, columns=train_cols)
    train_csv_fpath = utls.get_csv_fpath('training')
    train_df.to_csv(train_csv_fpath)
    print('Saving training metrics to:', os.path.realpath(train_csv_fpath))
    print()

    # Test model
    test_data = []
    for i in range(test_n):
        utls.print_label('\tTesting Batch', '{}/{}', [i + 1, test_n])
        batch = roa_loader.next_testing_batch()
        if not batch:
            break
        batch_x, batch_y = utls.generate_batches(batch)
        timesteps = batch_x.shape[0] // 100

        clips = utls.generate_clips(
                batch_x, batch_y,
                BATCH_X_SHAPE, BATCH_Y_SHAPE,
                CLIP_LENGTH)  # noqa
        batch_scalars = utls.run_method(model.test_on_batch, clips, timesteps)
        for clip, (loss, accuracy) in enumerate(batch_scalars):
            test_data.append([i + 1, clip + 1, loss, accuracy])
        model.reset_states()
        print()
        break

    # Save testing CSV
    test_cols = ['Replay', 'Clip', 'Loss', 'Accuracy']
    test_df = pd.DataFrame(data=test_data, columns=test_cols)
    test_csv_fpath = utls.get_csv_fpath('testing')
    test_df.to_csv(test_csv_fpath)
    print('Saving testing metrics to:', os.path.realpath(test_csv_fpath))

    # Save model
    model_path = os.path.join('..', 'models', MODEL_FNAME)
    print('Saving model as:', os.path.realpath(model_path))
    model.save(model_path)


if __name__ == '__main__':
    main()
