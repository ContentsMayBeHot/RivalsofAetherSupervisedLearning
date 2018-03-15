#from keras.models import Sequential
#from keras.layers import Dense, Dropout
#from keras.layers import Embedding
#from keras.layers import LSTM

import loader

def main():
    roa = loader.ReplayLoader()
    roa.load_training()
    roa.load_testing()

    (batch_x,batch_y) = roa.next_testing()
    print('Loaded first batch. Batch size:', len(batch_x))

    #model = Sequential()
    #model.add(LSTM(128))
    #model.add(Dropout(0.5))
    #model.add(Dense(1, activation='sigmoid'))
    # Reference: https://keras.io/getting-started/sequential-model-guide/

if __name__ == '__main__':
    main()
