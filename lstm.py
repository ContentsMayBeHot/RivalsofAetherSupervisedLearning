from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM

def main():
    model = Sequential()
    model.add(LSTM(128))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    # Reference: https://keras.io/getting-started/sequential-model-guide/

if __name__ == '__main__':
    main()
