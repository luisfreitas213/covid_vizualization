#import numpy as np
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

#Country
country = 'India'
#Parameters
n_steps = 7
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5
#Cross Validation
validation = [0, 5, 10, 15, 20]
#validation = [0, 5]

result_train = []
result_test = []

df_model = etl_dataset.create_dataset()

df_model = df_model[df_model['country']==country]
#df_model = df_model.groupby(['year_week'])['weekly_count','rate_14_day','cumulative_count','week_deaths','cumulative_deaths'].agg('sum')
df_model = df_model.groupby(['year_week'])['weekly_count'].agg('sum')

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

    X_test = X[-dim_test:]
    y_test = y[-dim_test:]
    X = X[:-dim_test]
    y = y[:-dim_test]

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

    predicted_stock_price = model.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    y_test = sc.inverse_transform(y_test)
    # Vizualizing the Results
    plt.plot(y_test, color = 'red', label = 'Real')
    plt.plot(predicted_stock_price, color = 'green', label = 'Predicted')
    plt.title('Covid Predicton')
    plt.xlabel('week')
    plt.ylabel('cases')
    plt.legend()
    #plt.show()

    result_train.append(min(history.history['loss']))
    #result_test.append(abs(sum((predicted_stock_price-y_test)**2)/dim_test))
    from sklearn.metrics import mean_squared_error
    result_test.append(mean_squared_error(y_test, predicted_stock_price))
    print(min(history.history['loss']))
    print(abs(sum((predicted_stock_price-y_test)**2)/dim_test))

dim = len(result_train)
d = dim-1
tr = 0
te = 0
while d >= 0:
    tr += result_train[d]
    te += result_test[d]
    d = d-1

result_train = tr/dim
result_test = te/dim
#result_test = result_test[0]
print(result_train)
print(result_test)
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now)

import pandas.io.sql as psql
from sqlalchemy import create_engine
from sqlalchemy import insert
engine = create_engine(r"postgresql://postgres:postgres@localhost/postgres")
c = engine.connect()
conn = c.connection
args = (country,n_steps,units,layers,drop,epochs,batch_size,optimizer,dim_test,result_train,result_test)
c.execute(''' Insert into covid_plataform.results_lstm_model ( country, n_steps,units, layers, drops, epochs, batch_size, optimizer, dim_test, result_train, result_test)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', args)

conn.close()
