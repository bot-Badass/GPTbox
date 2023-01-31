import os
import requests
import time
import json
import pandas as pd
import numpy as np
import binance
from dotenv import load_dotenv
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Flatten
from keras.optimizers import Adam
import matplotlib.pyplot as plt

load_dotenv()
headers = {'X-MBX-APIKEY': os.getenv('BINANCE_API_KEY')}

start = time.time()


class BinanceData:
    def __init__(self, ticker):
        self.client = binance.Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
        self.ticker = os.getenv('BINANCE_TICKER')
        # print(self.ticker)

    def retrieve_data(self):
        url = f"https://api.binance.com/api/v3/klines?symbol={self.ticker}&interval=1h&limit=500"
        # print(url)
        response = requests.get(url=url)
        data = response.json()
        # print(data)
        self.df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                              'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                              'Taker buy quote asset volume', 'Ignore'])
        self.df['Open time'] = pd.to_datetime(self.df['Open time'], unit='ms')
        self.df.set_index('Open time', inplace=True)
        self.df = self.df.astype(float)

        # Check if the data has at least one sample
        if self.df.shape[0] < 1:
            raise ValueError("Data does not have at least one sample.")

    def preprocess_data(self):
        close_df = self.df[['Close']]
        close_df = close_df.iloc[::-1]
        self.data = close_df.values
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(self.data)
        self.train_size = int(len(self.scaled_data) * 0.8)
        self.train_data = self.scaled_data[0:self.train_size, :]
        self.test_data = self.scaled_data[self.train_size:, :]
        self.Xtrain, self.ytrain = [], []
        for i in range(60, len(self.train_data)):
            self.Xtrain.append(self.train_data[i - 60:i, 0])
            self.ytrain.append(self.train_data[i, 0])
        self.Xtrain, self.ytrain = np.array(self.Xtrain), np.array(self.ytrain)
        self.Xtrain = np.reshape(self.Xtrain, (self.Xtrain.shape[0], self.Xtrain.shape[1], 1))


class ModelBuilder:
    def __init__(self, data, window_size=60):
        self.data = data
        self.window_size = window_size
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(self.window_size, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def train_model(self, Xtrain, ytrain, epochs=50, batch_size=32):
        self.model.fit(Xtrain, ytrain, epochs=epochs, batch_size=batch_size, verbose=0)


data = BinanceData('ticker')
data.retrieve_data()
data.preprocess_data()

model_builder = ModelBuilder(data.scaled_data)
model_builder.train_model(data.Xtrain, data.ytrain)
print(model_builder.model.summary())


def predict_profitability(self, model, test_data, scaler):
    predictions = []
    for i in range(60, len(test_data)):
        Xtest = test_data[i - 60:i, 0]
        Xtest = np.reshape(Xtest, (1, Xtest.shape[0], 1))
        prediction = model.predict(Xtest)
        prediction = scaler.inverse_transform(prediction)
        predictions.append(prediction[0][0])
    return predictions


def calculate_profitability(self, predictions, test_data):
    profitability = []
    for i in range(len(predictions)):
        actual_price = test_data[i + 60, 0]
        predicted_price = predictions[i]
        if predicted_price > actual_price:
            profit = (predicted_price - actual_price) / actual_price
            profitability.append(profit)
        else:
            profitability.append(0)
    return profitability


def get_total_profit(self, profitability):
    total_profit = sum(profitability)

    return total_profit


def get_average_profit(self, profitability):
    average_profit = sum(profitability) / len(profitability)

    return average_profit


end = time.time()
print("Total runtime: {:.2f} seconds".format(end-start))


# Create a list of tickers
tickers = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'LINKUSDT']

for ticker in tickers:
    # Create BinanceData and ModelBuilder objects for each ticker
    bd = BinanceData(ticker)
    bd.retrieve_data()
    bd.preprocess_data()
    mb = ModelBuilder(bd.scaled_data)

    # Train and evaluate the model
    mb.model.fit(bd.Xtrain, bd.ytrain, epochs=1, batch_size=32)
    predictions = mb.model.predict(bd.Xtest)
    predictions = bd.scaler.inverse_transform(predictions)
    mae = mean_absolute_error(bd.ytest, predictions)
    print(f'Mean Absolute Error for {ticker}: {mae}')

    # Plot the results
    plt.plot(bd.ytest, label='True')
    plt.plot(predictions, label='Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'{ticker} Price Prediction')
    plt.legend()
    plt.show()


# Trade algorithm
def trade_algorithm(ytest, predictions):
    current_price = ytest[0]
    predicted_price = predictions[0][0]
    shares = 100
    cash = 1000
    for i in range(1, len(ytest)):
        current_price = ytest[i]
        predicted_price = predictions[i][0]
        if predicted_price > current_price:
            # Buy shares
            shares += cash / current_price
            cash = 0
        elif predicted_price < current_price:
            # Sell shares
            cash += shares * current_price
            shares = 0
    return cash + shares * current_price




