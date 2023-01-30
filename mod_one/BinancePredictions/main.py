
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import binance
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Flatten  # Add these two libraries to be imported
from keras.optimizers import Adam
import matplotlib.pyplot as plt  # Add this library to be imported 
import requests  # To request data from Binance API  # Added missing import statement 
import json      # To format data retrieved from Binance API  # Added missing import statement

load_dotenv()
# url = 'https://api.binance.com/api/v1/klines?symbol='+BINANCE_TICKER+'&interval=1h'

headers = {'X-MBX-APIKEY': os.getenv('BINANCE_API_KEY')}


# Refactoring:
class BinanceData: 
    def __init__(self): 
        # Initialize Binance API Keys 
        self.client = binance.Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
        # Initialize Binance Ticker 
        self.ticker = self.client.get_ticker()

    def retrieve_data(self, headers): 
       
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.ticker}&interval=1h"
        # In the retrieve_data() method, the URL was incorrect, so it needed to be corrected 
        response = requests.get(url=url, headers=headers) 
        data = response.json() 
        print(data)
        # Format data into a pandas DataFrame
        self.df = pd.DataFrame(data) 
        print(self.df)

    def format_data(self): 
        # Convert Timestamp column to datetime format  
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'],unit='s')
        # Converting columns to float format 
        self.data[['Open', 'High', 'Low', 'Close']] = self.data[['Open','High','Low','Close']].astype(float)

    def create_new_df(self):
        # Create new DataFrame with only the 'Close' column 
        close_df = self.df[['Close']] 

    def reverse_df(self): 
        # Reverse order of dataframe so row 0 is the oldest record and highest index is most recent record   
        self.df.iloc[::-1]

    def set_index(self): 

        self.df.set_index('Timestamp', inplace=True) 

    def preprocess_data(self):  
        self.convert_to_numpy()  
        self.create_train_and_test()  
        self.scale_data()  

class ModelBuilder:     
    def __init__(self, Xtrain, ytrain): 
        # self.model = Sequential() 
        self.Xtrain = Xtrain
        self.ytrain = ytrain
        self.Xtrain_shape = Xtrain.shape[2] 
        

    def addLSTM(self, Xtrain, shape): 
        self.model.add(LSTM(units=128, input_shape=(Xtrain.shape[1], shape)))
 

    def build_model(self): 
        self.model = Sequential() 
        self.addLSTM(self.Xtrain, self.Xtrain_shape)
        

    def addDropout(self, model):
        # check if model is defined
        if model == None:
            return None

        # define dropout layer 
        dropout_layer = Dropout(rate=0.2)
        model.add(dropout_layer)
        return model
        

    def compileNetwork(model, layers): 
        if (model.layers[0].shape != layers[0] or model.layers[1].shape != layers[1]): 
            print("Error: Network model does not match shape of parameters") 
            return None 
        else: 
            model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy']) 
            return model


    def fitNetwork(model, layers):
        # Check that the model and layers match in shape
        if model.shape != layers.shape:
            raise ValueError('Model and layers do not match')

        # Fit the network with the given model and layers 
        model.fit(layers)
        
        




"""
# def compileNetwork(self, optimizer, loss): 
#     self.model.add(Dense(20, activation='relu', input_dim=10))  
#     self.model.add(Dense(8, activation='relu'))  
#     self.model.add(Dense(1, activation='sigmoid'))  

#     self.model.compile(optimizer=optimizer, loss=loss)
#     # The compileNetwork() method did not have a model defined with the correct shapes of layers to match those passed in as parameters 
"""

"""
# def addLSTM(self, Xtrain, shape2): 
        
#     model = Sequential()  # define the model
#     model.add(LSTM(units=50, return_sequences=True, input_shape=(Xtrain.shape[1], shape2)))  # add an LSTM layer with the given input shape  
#     model.add(Dense(1))  # add a dense layer with one node as output

#     # compile the model
#     model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
#     # In the addLSTM() method, self.Xtrain and self.Xtrain.shape[2] were not defined, so it will not know what the input shape should be; this can be fixed by adding a parameter to init which sets Xtrain and Xtrain.shape[2] and then passing those into addLSTM as parameters 
#     return model
"""