import matplotlib.pyplot as plt


def crear_grafica(datos, modelo, año_futuro):
    años = datos["Año"]
    produccion = datos["Produccion"]

    años_modelo = list(range(int(años.min()), año_futuro + 1))

    produccion_modelo = modelo.predict(
        [[año] for año in años_modelo]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        años,
        produccion,
        color="blue",
        label="Producción histórica"
    )

    ax.plot(
        años_modelo,
        produccion_modelo,
        color="red",
        label="Tendencia del modelo"
    )

    ax.set_title("Producción de maíz en México")
    ax.set_xlabel("Año")
    ax.set_ylabel("Producción (toneladas)")
    ax.legend()
    ax.grid(True)

    return fig