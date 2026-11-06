import pandas as pd
from Modelo import entrenar_modelo, predecir_produccion

datos = pd.read_csv("data/produccion_maiz.csv")

modelo, pendiente, intercepto, r2, error = entrenar_modelo(datos)

print("===== PRUEBA DEL MODELO =====")
print("Pendiente:", pendiente)
print("Intercepto:", intercepto)
print("Coeficiente R²:", r2)
print("Error RMSE:", error)

año = 2025
resultado = predecir_produccion(modelo, año)

print(f"Producción estimada para {año}: {resultado:,.2f} toneladas")
