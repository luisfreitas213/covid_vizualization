import pandas as pd
import numpy as np
import predict_lstm
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import matplotlib.pyplot as plt
import etl_dataset
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine



def db_predicton(pred,country,n_steps,units,layers,drop,epochs,batch_size,optimizer,dim_test):
    result_train = []
    result_test = []

    df_model = etl_dataset.create_dataset()

    df_model = df_model[df_model['country']==country]
    #df_model = df_model.groupby(['year_week'])['weekly_count','rate_14_day','cumulative_count','week_deaths','cumulative_deaths'].agg('sum')
    df_model = df_model.groupby(['year_week'])['weekly_count'].agg('sum')

    #df_model.plot()
    #pyplot.show()

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
    train_pred = []
    i = 0
    while i<5:
        train_pred.append(int(predicted_stock_price[i][0]))
        i += 1

    #predictons
    predictons = predict_lstm.pred(country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)
    predictons = [int(predictons[0][0][0]), int(predictons[1][0][0]), int(predictons[2][0][0]), int(predictons[3][0][0]), int(predictons[4][0][0])]

    #real data
    df_model=df_model.reset_index()
    df_model['country'] = country



    x = df_model[-5:]
    data_train_pred = [x.iloc[0][0],x.iloc[1][0],x.iloc[2][0],x.iloc[3][0],x.iloc[4][0]]

    i = 4
    data_pred = []
    data = x.iloc[4][0]
    while i >= 0:
        data = data.split("-")
        year = data[0]
        week = int(data[1])+1
        data = str(year)+"-"+str(week)
        data_pred.append(data)
        i += -1
    country = [country, country, country, country, country]
    predictons = pd.DataFrame(list(zip(country, data_pred,predictons)), columns = ['country','year_week','predictons'])
    train_pred = pd.DataFrame(list(zip(country, data_train_pred,train_pred)), columns = ['country','year_week','train_predictons'])


    frames = [df_model, train_pred, predictons]
    result = pd.concat(frames)
    result = result.reset_index()

    engine = create_engine(r"postgresql://postgres:postgres@localhost/postgres")
    c = engine.connect()
    conn = c.connection
    c.execute(f'drop view if exists public.{pred};')
    c.execute(f'drop table if exists covid_plataform.{pred};')
    result.to_sql(pred, engine,schema = 'covid_plataform')
    c.execute(f'''create or replace view public.{pred} as
    select  row_number() OVER (ORDER BY year_week ASC) AS id,year_week ,country, max(weekly_count) as weekly_count ,  max(train_predictons) as train_predictons, max(predictons) as predictons from covid_plataform.{pred}
    group by year_week ,country
    order by year_week''')
    conn.close()
