import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np


def entrenar_modelo(datos):
    X = datos[["Año"]]
    y = datos["Produccion"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    predicciones = modelo.predict(X)

    r2 = r2_score(y, predicciones)
    error = np.sqrt(mean_squared_error(y, predicciones))

    pendiente = modelo.coef_[0]
    intercepto = modelo.intercept_

    return modelo, pendiente, intercepto, r2, error


def predecir_produccion(modelo, año):
    prediccion = modelo.predict(pd.DataFrame({"Año": [año]}))
    return prediccion[0]
