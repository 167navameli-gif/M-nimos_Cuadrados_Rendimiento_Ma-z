import numpy as np


def entrenar_modelo(datos):
    x = datos["Año"].to_numpy(dtype=float)
    y = datos["Produccion"].to_numpy(dtype=float)

    promedio_x = np.mean(x)
    promedio_y = np.mean(y)

    numerador = np.sum((x - promedio_x) * (y - promedio_y))
    denominador = np.sum((x - promedio_x) ** 2)

    if denominador == 0:
        raise ValueError("No se puede calcular la pendiente.")

    pendiente = numerador / denominador
    intercepto = promedio_y - pendiente * promedio_x

    predicciones = pendiente * x + intercepto

    suma_errores = np.sum((y - predicciones) ** 2)
    suma_total = np.sum((y - promedio_y) ** 2)

    if suma_total == 0:
        r2 = 1.0 if suma_errores == 0 else 0.0
    else:
        r2 = 1 - (suma_errores / suma_total)

    error = np.sqrt(np.mean((y - predicciones) ** 2))

    modelo = {
        "pendiente": pendiente,
        "intercepto": intercepto
    }

    return modelo, pendiente, intercepto, r2, error


def predecir_produccion(modelo, año):
    return (
        modelo["pendiente"] * año
        + modelo["intercepto"]
    )