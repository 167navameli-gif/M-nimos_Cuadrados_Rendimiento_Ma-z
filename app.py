import streamlit as st
import pandas as pd

from Modelo import entrenar_modelo, predecir_produccion
from Graficas import crear_grafica


st.set_page_config(
    page_title="Predicción de maíz en México",
    page_icon="🌽",
    layout="wide"
)

st.title("🌽 Predicción de la producción de maíz en México")

st.write(
    "Sistema de análisis y predicción de producción agrícola "
    "mediante mínimos cuadrados ordinarios."
)

st.markdown("### Fuente de datos: FAOSTAT")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/produccion_maiz.csv")


try:
    datos = cargar_datos()

    st.subheader("Datos históricos")

    st.dataframe(datos, use_container_width=True)

    modelo, pendiente, intercepto, r2, error = entrenar_modelo(datos)

    st.subheader("Resultados del modelo")

    col1, col2, col3 = st.columns(3)

    col1.metric("Pendiente", f"{pendiente:,.2f}")
    col2.metric("Intercepto", f"{intercepto:,.2f}")
    col3.metric("R²", f"{r2:.4f}")

    st.write(
        "La pendiente representa el cambio estimado en la "
        "producción por cada año."
    )

    st.write(
        "El intercepto es el valor estimado cuando el año es cero; "
        "no tiene una interpretación práctica directa en este contexto."
    )

    st.write(
        "R² indica qué proporción de la variación histórica explica "
        "el modelo lineal."
    )

    st.subheader("Gráfica de producción histórica y tendencia")

    año_futuro = st.slider(
        "Selecciona el año que deseas estimar",
        min_value=2025,
        max_value=2035,
        value=2025
    )

    prediccion = predecir_produccion(modelo, año_futuro)

    st.metric(
        f"Producción estimada para {año_futuro}",
        f"{prediccion:,.2f} toneladas"
    )

    grafica = crear_grafica(datos, modelo, año_futuro)

    st.pyplot(grafica)

    st.subheader("Tabla de predicciones")

    años_futuros = pd.DataFrame({
        "Año": range(2025, 2036)
    })

    años_futuros["Producción estimada"] = años_futuros["Año"].apply(
    lambda año: predecir_produccion(modelo, año)
)

    st.dataframe(años_futuros, use_container_width=True)

    st.info(
        "Las predicciones son estimaciones matemáticas basadas en "
        "la tendencia lineal de los datos históricos. No representan "
        "una garantía de producción futura."
    )

    st.caption("Proyecto académico | Datos proporcionados de FAOSTAT")

except Exception as e:
    st.error(f"Ocurrió un error al cargar o procesar los datos: {e}")