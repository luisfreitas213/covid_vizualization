
import pandas as pd
import tensorflow as tf
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from statistics import mean
import etl_dataset
from matplotlib import pyplot
import statistics

def pred(country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test):


    df_model = etl_dataset.create_dataset()

    df_model = df_model[df_model['country']==country]
    #df_model = df_model.groupby(['year_week'])['weekly_count','rate_14_day','cumulative_count','week_deaths','cumulative_deaths'].agg('sum')
    df_model = df_model.groupby(['year_week'])['weekly_count'].agg('sum')

    X = df_model


    """PART1 - DATA PROCESSING"""
    X = pd.DataFrame(X)
    sc = MinMaxScaler(feature_range = (0,1))
    X = sc.fit_transform(X)

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
    # summarize the data
    #for i in range(len(X)):
    #print(X[i], y[i])

    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    """PART2 - BUILDING THE LSTM"""
    # Adding the first LSTM layer and some dropout regularization
    model = Sequential()
    model.add(LSTM(units = units, return_sequences = True, input_shape=(n_steps, n_features)))
    model.add(Dropout(drop))

    # Adding the second LSTM layer and some dropout regularization
    i = 0
    while i < layers:
        model.add(LSTM(units = units, return_sequences = True))
        model.add(Dropout(drop))
        i += 1

    model.add(LSTM(units = units, return_sequences = False))
    model.add(Dropout(drop))

    #Adding the output layer
    model.add(Dense(units = 1))

    """Part3 - Training The LSTM """

    # Compiling the RNN
    model.compile(optimizer = optimizer, loss = 'mean_squared_error')

    #Fitting the RNN to Training set

    history = model.fit(X, y, epochs = epochs, batch_size = batch_size)

    predictons = []
    #mostrar valores a prever
    values_x = df_model[-n_steps:]


    p = 5
    while p!=0:
        #transformar em dataframe
        values = pd.DataFrame(values_x)
        values = sc.transform(values)
        # guardar o valor transformado
        x_input = array(values)
        #fazer o reshape
        x_input = x_input.reshape((1, n_steps, n_features))
        #fazer a previsão
        yhat = model.predict(x_input, verbose=0)
        #transformar o valor da previsão
        yhat = sc.inverse_transform(yhat)
        # guardar o valor da previsão
        predictons.append(yhat)

        df = pd.DataFrame(yhat)
        frames = [values_x, df]
        values = pd.concat(frames)
        values_x = values[-n_steps:]
        p = p-1
    return predictons
