
import os
import requests
import time
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
HEADERS = {'X-MBX-APIKEY': os.getenv('BINANCE_API_KEY')}


class BinanceData:
    def __init__(self, ticker):
        self.client = binance.Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
        self.ticker = os.getenv('BINANCE_TICKER')

    def retrieve_data(self):
        url = f"https://api.binance.com/api/v3/klines?symbol={self.ticker}&interval=1h&limit=500"
        response = requests.get(url=url)
        data = response.json()
        self.df = pd.DataFrame(data, columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close time', 'Quote asset volume', 'Number of trades',
            'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
        ])
        self.df['Open time'] = pd.to_datetime(self.df['Open time'], unit='ms')
        self.df.set_index('Open time', inplace=True)
        self.df = self.df.astype(float)

        if self.df.shape[0] < 1:
            raise ValueError("Data does not have at least one sample.")


class Preprocessor(BinanceData):
    def init(self, data):
        self.data = data
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(self.data)
        self.train_size = int(len(self.scaled_data) * 0.8)
        self.train_data = self.scaled_data[0:self.train_size, :]
        self.test_data = self.scaled_data[self.train_size:, :]


class ModelBuilder:
    def init(self, data, window_size=60):
        self.data = data
        self.window_size = window_size
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(self.window_size, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(100, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(25, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mean_squared_error', optimizer='adam')

        return model

    def fit_model(self, Xtrain, ytrain, epochs=1, batch_size=64):
        self.model.fit(Xtrain, ytrain, epochs=epochs, batch_size=batch_size)

    def predict(self, Xtest, batch_size=64):
        return self.model.predict(Xtest, batch_size=batch_size)

    def evaluate_model(self, Xtest, ytest):
        y_pred = self.model.predict(Xtest)
        y_test_scaled = self.data.scaler.inverse_transform(ytest.reshape(-1, 1))
        y_pred_scaled = self.data.scaler.inverse_transform(y_pred)
        print("R2 Score: ", r2_score(y_test_scaled, y_pred_scaled))
        print("Mean Absolute Error: ", mean_absolute_error(y_test_scaled, y_pred_scaled))

    def plot_prediction(self, Xtest, ytest):
        y_pred = self.model.predict(Xtest)
        y_test_scaled = self.data.scaler.inverse_transform(ytest.reshape(-1, 1))
        y_pred_scaled = self.data.scaler.inverse_transform(y_pred)
        plt.plot(y_test_scaled, label='True Price')
        plt.plot(y_pred_scaled, label='Predicted Price')
        plt.title("Price prediction")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend(loc='best')
        plt.show()


if __name__ == '__main__':
    bd = BinanceData('BTCUSDT')
    bd.retrieve_data()
    # bd.preprocess_data()
    Preprocessor(bd)
    Xtrain, Xtest, ytrain, ytest = bd.train_data, bd.test_data, bd.ytrain, bd.ytest
    mb = ModelBuilder(bd)
    mb.fit_model(Xtrain, ytrain, epochs=5)
    mb.evaluate_model(Xtest, ytest)
    mb.plot_prediction(Xtest, ytest)
