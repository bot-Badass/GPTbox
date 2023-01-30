# Unit test code:
import os
import unittest
import numpy as np
from main import BinanceData
from sklearn.preprocessing import MinMaxScaler

headers = {'X-MBX-APIKEY': os.getenv('BINANCE_API_KEY')}

class TestBinanceData(unittest.TestCase):

    def setUp(self):  # Refactoring: Initialization of class object and its members  
        self.binance_data = BinanceData() 

    def test_retrieve_data(self): 
        self.assertEqual(self.binance_data.retrieve_data(headers), {'symbol', 'price'})

    def test_format_data(self): 
        self.assertEqual(self.binance_data.format_data(), np.float)

    def test_create_new_df(self): 
        self.assertEqual(list(self.binance_data.create_new_df()), ['Close'])

    def test_reverse_df(self): 
        self.assertTrue((self.binance_data[0][0] > self.binance[-1][0]))

    def testSetIndex(self): 
        self.assertTrue('Timestamp' in list(self.binance[0]))

    def testPreprocessData(self): 
        data = np.array([1, 2, 3, 4])   # Sample data to be tested against the result of preprocessData()    
        self.assertTrue((MinMaxScaler().fit_transform([[1], [2], [3], [4]]) == data).all())

     # Test for ModelBuilder class    
class TestModelBuilder (unittest.TestCase): 

    # Initialization of class object and its members  
    def setUp (self):  
        Xtrain = np.array([1, 2, 3, 4])   # Sample training data to be tested against the result of buildModel()      
        ytrain = np
        