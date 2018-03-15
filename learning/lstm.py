import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM

import loader

def main():
    batch_size = 5
    input_shape = (batch_size, 135, 240, 3)
    num_classes = 26

    # Compile model
    model = Sequential()
    model.add(Dense(32, input_shape=input_shape))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Load data
    roa = loader.ReplayLoader()
    roa.load_training()
    (data,labels) = roa.next_training_batch(n=batch_size)

    model.fit(data, labels)

if __name__ == '__main__':
    main()
