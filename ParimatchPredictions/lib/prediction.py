#### `prediction.py`


def make_predictions(df):
    """
    Делает предсказание исходов событий.
    :param df:  Данные для построения модели (в виде DataFrame) 
    :return: Предсказанный результат 
    """
    
    # Делает предсказание исходов событий. :param df:  Данные для построения модели (в виде DataFrame) :return: Предсказанный результат 

    df_predictions = df.copy()
    df_predictions['result'] = 'win'

    return df_predictions
