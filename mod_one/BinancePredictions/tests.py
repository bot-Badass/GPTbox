import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from main import BinanceData, predict_profitability
import time
from unittest.mock import MagicMock
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import time

start_start = time.time()
# your code to measure runtime


def test_retrieve_data():
    bd = BinanceData("BTCUSDT")
    bd.retrieve_data()
    assert isinstance(bd.df, pd.DataFrame)
    assert bd.df.shape[0] == 500
    assert bd.df.shape[1] == 11
    assert bd.df.iloc[0, 0] == bd.df.index[0]


def test_preprocess_data():
    bd = BinanceData("BTCUSDT")
    bd.retrieve_data()
    bd.preprocess_data()
    assert isinstance(bd.data, np.ndarray)
    assert bd.data.shape[0] == 500
    assert bd.data.shape[1] == 1
    assert isinstance(bd.scaler, MinMaxScaler)
    assert isinstance(bd.scaled_data, np.ndarray)
    assert bd.scaled_data.shape[0] == 500
    assert bd.scaled_data.shape[1] == 1
    assert isinstance(bd.train_data, np.ndarray)
    assert bd.train_data.shape[0] == 400
    assert bd.train_data.shape[1] == 1
    assert isinstance(bd.test_data, np.ndarray)
    assert bd.test_data.shape[0] == 100
    assert bd.test_data.shape[1] == 1
    assert isinstance(bd.Xtrain, np.ndarray)
    assert bd.Xtrain.shape[0] == 340
    assert bd.Xtrain.shape[1] == 60
    assert bd.Xtrain.shape[2] == 1
    assert isinstance(bd.ytrain, np.ndarray)
    assert bd.ytrain.shape[0] == 340


def test_predict_profitability():
    # test data
    Xtest = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])
    ytest = np.array([[10],[9],[8],[7],[6],[5],[4],[3],[2],[1]])
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit(Xtest)
    Xtest = scaler.transform(Xtest)
    ytest = scaler.transform(ytest)

    # mock model
    model = MagicMock()
    model.predict.return_value = ytest

    # call predict_profitability
    start_time = time.time()
    predictions = predict_profitability(model, Xtest, scaler)
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))

    # assert
    assert len(predictions) == 10
    for i in range(len(predictions)):
        assert predictions[i] == ytest[i][0]

    test_predict_profitability()


end_end = time.time()
print("Total test runtime: {:.2f} seconds".format(end_end-start_start))

"""
Чтобы написать логику для поиска наиболее маржинальных ситуаций и входа в сделку, вам нужно следующее:

Понимание данных, которые вы используете, и их значения, в том числе цены, доходности, риски и т.д.

Определение метрики маржинальности, которую вы хотите использовать, например, отношение дохода к риску.

Реализация алгоритма, который будет оценивать эту метрику для каждой ситуации и выбирать наиболее маржинальные.

Реализация механизма входа в сделку, который будет использовать информацию из выбранных маржинальных ситуаций.

Тестирование и оптимизация вашей логики, чтобы убедиться, что она эффективно работает и дает желаемые результаты.

"""

#
# class ModelBuilder:
#     def __init__(self, data):
#         self.data = data
#
#     def train_model(self, X, y):
#         self.model = RandomForestRegressor()
#         self.model.fit(X, y)
#
#     def predict(self, X):
#         return self.model.predict(X)





"""The code seems to have some issues regarding the structure, readability, and coding practices. Here are some suggestions to improve the code:

The code should have a clear structure, with functions and classes defined in a separate file and imported into the main file.

All class and function names should be written in PascalCase, and all variables and attributes should be written in snake_case.

The preprocess_data() method should not be part of the BinanceData class but a separate preprocessing class.

Use environment variables for API keys and other sensitive data, rather than hardcoded values.

Remove unused imports and comments.

Add docstrings to classes and functions to explain what they do.

"""



# Для анализа данных по каждому тикеру индивидуально можно использовать алгоритм рекуррентной нейронной сети (RNN). Модель может выглядеть так:
#
# Предобработка данных: нормализация, заполнение пропущенных значений, разделение на тренировочный и тестовый набор данных.
#
# Определение слоев модели: входной слой, слой рекуррентной ячейки, выходной слой.
#
# Тренировка модели: использование оптимизатора, функции потерь и метрик для оценки точности модели.
#
# Оценка качества модели: использование тестовых данных для оценки точности модели и выявление возможных проблем.
#
# Применение модели для принятия решений: использование модели для прогнозирования значений и принятие решений по каждому тикеру индивидуаль