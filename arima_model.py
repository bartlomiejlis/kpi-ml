import random
from data_preparation import train, test, y
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
import glob
import re
import os
import matplotlib.pyplot as plt


def train_and_save_model(order):
    arima_model = ARIMA(y, order=order)
    arima_model = arima_model.fit()

    # Generujemy prognozy za pomocą wytrenowanego modelu ARMA na taki sam okres, jak długość zestawu danych testowych
    y_pred = arima_model.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha=0.05)
    y_pred_df['predictions'] = arima_model.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
    y_pred_df.index = test.index

    rmse = np.sqrt(mean_squared_error(test['pct_turnover'].values, y_pred_df['predictions']))
    if rmse <= 0.03:
        model_name = 'ARIMA_model_with_score_' + str(rmse)
        joblib.dump(arima_model, model_name)
        print(f'Saved model {model_name}')
    else:
        print(f'Model was not good enough')


def find_files_with_prefix(directory, prefix):
    # Wyszukujemy wszystkie pliki w systemie plików, które pasują do zadanego wzorca pattern i zwracamy je w formie
    # listy
    pattern = os.path.join(directory, f"{prefix}*")
    return glob.glob(pattern)


def extract_score(filename, prefix):
    match = re.search(rf"{prefix}(\d+\.\d+)", filename)
    if match:
        return float(match.group(1))
    return None


def remove_files_except_best_model(directory, prefix):
    files = find_files_with_prefix(directory, prefix)

    # Jeśli nie znaleziono żadnych plików to poinformujmy o tym użytkownika
    if not files:
        return print("No files were found for the given prefix.")

    scores = {file: extract_score(file, prefix) for file in files}

    best_model = min(scores, key=scores.get)

    for file in files:
        if file != best_model:
            os.remove(file)
            print(f"File removed: {file}")

    print(f"File saved: {best_model}")

    return best_model


def create_plot(model_name):
    arma_model = joblib.load(model_name)

    # Generujemy prognozy za pomocą wytrenowanego modelu ARMA na taki sam okres, jak długość zestawu danych testowych
    y_pred = arma_model.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha=0.05)
    y_pred_df['predictions'] = arma_model.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df['predictions']

    plt.plot(train, color='black', label='Dane treningowe')
    plt.plot(test, color='red', label='Dane testowe')
    plt.plot(y_pred_out, color='green', label='Prognoza ARIMA')
    plt.legend()
    plt.ylabel('Procent obrotu')
    plt.xlabel('Okres')
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.title('Prognoza procentu obrotu wg modelu ARIMA')
    plt.show()


def model_generator(x):
    for _ in range(x):
        p = random.randint(0, 5)
        d = random.randint(0, 5)
        q = random.randint(0, 5)
        train_and_save_model((p, d, q))


# Jako argument podajemy liczbę modeli jaką chcemy wytrenować
model_generator(1000)

directory = os.path.dirname(os.path.abspath(__file__))
prefix = "ARIMA_model_with_score_"
best_model = remove_files_except_best_model(directory, prefix)

create_plot(best_model)