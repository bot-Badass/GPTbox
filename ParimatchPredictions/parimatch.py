#### `parimatch.py`

# Импорт библиотек
import pandas as pd
import json
from lib.prediction import make_predictions

# Загрузка данных
with open('ParimatchPredictions\config.json') as json_data_file:
    config = json.load(json_data_file)

df_past = pd.read_csv(config['input_file'])

# Предсказание
df_predictions = make_predictions(df_past)

# Запись в файл
df_predictions.to_csv(config['output_file'], index=False)


