
def calcular_mco(fertilizante, rendimiento):
    """
    Calcula la pendiente y el intercepto
    mediante minimos cuadrados ordinarios.
    """

    # Validar las cantidades de datos
    if len(fertilizante) != len(rendimiento):
        raise ValueError(
            "Debe existir un rendimiento por cada dato de fertilizante."
        )

    if len(fertilizante) < 2:
        raise ValueError(
            "Se necesitan al menos dos observaciones."
        )

    n = len(fertilizante)

    # Calcular los promedios
    promedio_x = sum(fertilizante) / n
    promedio_y = sum(rendimiento) / n

    # Calcular numerador y denominador
    numerador = 0
    denominador = 0

    for i in range(n):
        numerador += (
            (fertilizante[i] - promedio_x)
            * (rendimiento[i] - promedio_y)
        )

        denominador += (
            fertilizante[i] - promedio_x
        ) ** 2

    # Evitar division entre cero
    if denominador == 0:
        raise ValueError(
            "Los valores de fertilizante deben variar."
        )

    # Calcular los coeficientes
    pendiente = numerador / denominador
    intercepto = promedio_y - pendiente * promedio_x

    return pendiente, intercepto
