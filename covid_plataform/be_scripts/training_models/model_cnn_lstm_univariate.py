# univariate cnn lstm example
import pandas as pd
import tensorflow as tf
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from statistics import mean
import etl_dataset
from matplotlib import pyplot
import statistics
#Country
country = 'India'
#Parameters
n_steps = 4
units = 100
layers = 3
drop = 0.2
epochs = 2
batch_size = 10
optimizer = 'adam'
dim_test = 5
#Cross Validation
#validation = [0, 5, 10, 15, 20]
validation = [0, 5]

result_train = []
result_test = []

df_model = etl_dataset.create_dataset()

df_model = df_model[df_model['country']==country]
#df_model = df_model.groupby(['year_week'])['weekly_count','rate_14_day','cumulative_count','week_deaths','cumulative_deaths'].agg('sum')
df_model = df_model.groupby(['year_week'])['weekly_count'].agg('sum')
df_model = df_model.values.tolist()
#df_model.plot()
#pyplot.show()
for k in validation:
    X = df_model
    i = k
    while i != 0:
        X = X[:-1]
        i = i-1

    """PART1 - DATA PROCESSING"""
    X = pd.DataFrame(X)
    sc = MinMaxScaler(feature_range = (0,1))
    X = sc.fit_transform(X)
    Y = []
    for i in range(0,len(X)):
        Y.append(X[i][0])
    X = Y


    # split a univariate sequence
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps
		    # check if we are beyond the sequence
            if end_ix > len(sequence)-1:
                break
		    # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    # define input sequence
    raw_seq = X
    # choose a number of time steps
    n_steps = n_steps
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    #reshape from [samples, timesteps] into [samples, subsequences, timesteps, features]
    n_features = 1
    n_seq = 2
    n_steps = 2
    print(X)
    X = X.reshape((X.shape[0], n_seq, n_steps, n_features))
    #print(X)

    """PART2 - BUILDING THE CNN - LSTM"""
    # define model
    model = Sequential()
    model.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation='relu'), input_shape=(None, n_steps, n_features)))
    model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model.add(TimeDistributed(Flatten()))
    model.add(LSTM(units, return_sequences = True, activation='relu'))
    i = 0
    while i < layers:
        model.add(LSTM(units = units, return_sequences = True))
        i += 1
    model.add(LSTM(units = units, return_sequences = False))
    model.add(Dense(1))

    """Part3 - Training The CNN - LSTM """
    # Compiling the RNN
    model.compile(optimizer = optimizer, loss = 'mean_squared_error')

    #Fitting the RNN to Training set

    #history = model.fit(X, y, epochs = epochs, batch_size = batch_size)
