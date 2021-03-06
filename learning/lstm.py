import configparser
import datetime as dt
import os
import numpy as np
import pandas as pd
import keras
import sys
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Reshape, GlobalAveragePooling2D, AveragePooling3D, Input, LSTM, TimeDistributed, Dropout, Conv2D # noqa
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization

from loader import ROALoader
import utilities as utls


EPOCHS = 10
MODEL_FNAME = 'rival.h5'
WEIGHTS_FNAME = 'rival-w.h5'

CLASSES = 9
IMG_U = 45
IMG_V = 80
IMG_C = 1
CLIP_LENGTH = 100
VISION_INPUT_SHAPE = (1, CLIP_LENGTH, IMG_U, IMG_V, IMG_C)
ACTIONS_INPUT_SHAPE = (1, CLIP_LENGTH, CLASSES)
OUTPUT_SHAPE = (1, CLIP_LENGTH, CLASSES)

FILTERS = 32
POOL_SIZE = (1, IMG_U, IMG_V)
KERNEL_SIZE = (3, 3)

LSTM_UNITS = 48

DEEP_UNITS = 256
DROPOUT_RATE = 0.2

TRAIN_LIMIT = 2
TEST_LIMIT = 2


def model_functional():
    # Primary input: Image data
    vision_input = Input(
            batch_shape=VISION_INPUT_SHAPE,
            name='vision_input')
    # Primary model: 2D convolutional LSTM
    vision_x = ConvLSTM2D(
            filters=FILTERS,
            kernel_size=KERNEL_SIZE,
            batch_input_shape=VISION_INPUT_SHAPE,
            data_format='channels_last',
            padding='same',
            return_sequences=True,
            stateful=True)(vision_input)
    vision_x = BatchNormalization()(vision_x)
    vision_x = AveragePooling3D(pool_size=POOL_SIZE)(vision_x)
    vision_output = Reshape(target_shape=(-1, FILTERS))(vision_x)

    # Auxiliary input: Previous labels
    actions_input = Input(
            batch_shape=ACTIONS_INPUT_SHAPE,
            name='actions_input'
    )

    # Concatenate primary and auxiliary
    main_x = keras.layers.concatenate([vision_output, actions_input])

    # Deep neural network
    main_x = LSTM(
            units=LSTM_UNITS,
            return_sequences=True,
            stateful=True)(main_x)

    # Output layer
    main_output = Dense(
        units=CLASSES,
        activation='sigmoid',
        name='main_output')(main_x)

    # Finished model
    model = Model(
            inputs=[vision_input, actions_input],
            outputs=[main_output])
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
    return model


def main():
    resume_session = False
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '--resume' or arg == '-r':
                resume_session = True
            else:
                print('Invalid argument "', arg, '"; terminating')
                sys.exit(1)

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
    # Load testing set
    testing_set_path = config['SETS']['PathToTesting']

    # Get model
    model = model_functional()
    model.summary()

    # Optionally, load weights from prior session
    if resume_session:
        weights_path = os.path.join('..', 'models', WEIGHTS_FNAME)
        print('Loading weights from', os.path.realpath(weights_path))
        model.load_weights(weights_path)
    print()

    # Train model
    train_data = []
    # For each epoch
    for e in range(EPOCHS):
        print('Loading Training set for EPOCH ' + str(e + 1))
        train_n = roa_loader.load_training_set(
                training_set_path, max_queue_size=32)
        print('Epoch: {}/{}'.format(e + 1, EPOCHS))
        # For each replay
        for i in range(train_n):
            utls.print_label('\tTraining Batch', '{}/{}', [i + 1, train_n])
            # Get a single replay
            batch = roa_loader.next_training_batch()
            if not batch:
                break
            batch_x, batch_y, batch_y1 = utls.generate_batches(batch)
            tsteps = batch_x.shape[0] // CLIP_LENGTH
            # Split batch into equal-length clips
            clips = utls.generate_clips(
                    batch_x, batch_y, batch_y1,
                    VISION_INPUT_SHAPE, OUTPUT_SHAPE, CLIP_LENGTH)
            batch_scalars = utls.run_method(model.train_on_batch, clips, tsteps)
            ts = dt.datetime.now()
            for clip, (loss, accuracy) in enumerate(batch_scalars):
                train_data.append([e + 1, i + 1, clip + 1, loss, accuracy, ts])
            model.reset_states()
            print()
        print("Terminating subprocess for EPOCH " + str(e + 1))
        roa_loader.kill_training_subprocess()
        print()

    # Save training CSV
    train_cols = ['Epoch', 'Replay', 'Clip', 'Loss', 'Accuracy', 'Timestamp']
    train_df = pd.DataFrame(data=train_data, columns=train_cols)
    train_csv_fpath = utls.get_csv_fpath('training')
    train_df.to_csv(train_csv_fpath)
    print('Saving training metrics to:', os.path.realpath(train_csv_fpath))
    print()

    # Start loading testing data
    test_n = roa_loader.load_testing_set(testing_set_path, max_queue_size=32)

    # Test model
    test_data = []
    for i in range(test_n):
        utls.print_label('\tTesting Batch', '{}/{}', [i + 1, test_n])
        batch = roa_loader.next_testing_batch()
        if not batch:
            break
        batch_x, batch_y, batch_y1 = utls.generate_batches(batch)
        timesteps = batch_x.shape[0] // CLIP_LENGTH
        # Split batch into equal-length clips
        clips = utls.generate_clips(
                batch_x, batch_y, batch_y1,
                VISION_INPUT_SHAPE, OUTPUT_SHAPE, CLIP_LENGTH)  # noqa
        batch_scalars = utls.run_method(model.test_on_batch, clips, timesteps)
        ts = dt.datetime.now()
        for clip, (loss, accuracy) in enumerate(batch_scalars):
            test_data.append([i + 1, clip + 1, loss, accuracy, ts])
        model.reset_states()
        print()
    print()

    # Save testing CSV
    test_cols = ['Replay', 'Clip', 'Loss', 'Accuracy', 'Timestamp']
    test_df = pd.DataFrame(data=test_data, columns=test_cols)
    test_csv_fpath = utls.get_csv_fpath('testing')
    test_df.to_csv(test_csv_fpath)
    print('Saving testing metrics to:', os.path.realpath(test_csv_fpath))

    # Save model
    model_path = os.path.join('..', 'models', MODEL_FNAME)
    print('Saving model as:', os.path.realpath(model_path))
    model.save(model_path)

    # Save weights
    weights_path = os.path.join('..', 'models', WEIGHTS_FNAME)
    print('Saving weights as:', os.path.realpath(weights_path))
    model.save_weights(weights_path)


if __name__ == '__main__':
    main()
