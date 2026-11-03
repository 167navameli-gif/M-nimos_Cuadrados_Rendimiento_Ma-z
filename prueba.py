import pandas as pd
from modelo import entrenar_modelo, predecir_produccion

# Cargar los datos
datos = pd.read_csv("data/produccion_maiz.csv")

# Entrenar el modelo
modelo, pendiente, intercepto, r2, error = entrenar_modelo(datos)

# Mostrar resultados
print("===== PRUEBA DEL MODELO =====")
print("Pendiente:", pendiente)
print("Intercepto:", intercepto)
print("Coeficiente R²:", r2)
print("Error RMSE:", error)

# Realizar una predicción
año = 2025
resultado = predecir_produccion(modelo, año)

print(f"Producción estimada para {año}: {resultado:,.2f} toneladas")
