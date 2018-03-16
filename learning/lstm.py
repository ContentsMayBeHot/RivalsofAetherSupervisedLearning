import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding, LSTM, Flatten

import loader

def main():
    batch_size = 1
    input_shape = (135, 240, 3)
    num_classes = 26

    # Compile model
    model = Sequential()
    model.add(Dense(units=32, input_shape=input_shape))
    model.add(Dense(units=10))
    model.add(Flatten())
    model.add(Dense(units=num_classes))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Load data
    roa = loader.ReplayLoader()
    roa.load_training()
    x_train = []
    y_train = []
    n = 10
    for i in range(n):
        print('Fetching sample [{}/{}]'.format(i+1, n))
        (x,y) = roa.next_training_sample()
        x_train += x
        y_train += y
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    # Train model
    model.fit(x_train, y_train)

if __name__ == '__main__':
    main()
