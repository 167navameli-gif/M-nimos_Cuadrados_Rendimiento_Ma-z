import streamlit as st
import pandas as pd

from Modelo import entrenar_modelo, predecir_produccion
from Graficas import crear_grafica


st.set_page_config(
    page_title="Predicción de maíz en México",
    layout="wide"
)

st.title(" Predicción de la producción de maíz en México")

st.write(
    "Sistema de análisis y predicción de producción agrícola "
    "mediante mínimos cuadrados ordinarios."
)

st.markdown("### Fuente de datos: FAOSTAT")


# Cargar datos históricos
@st.cache_data
def cargar_datos():
    return pd.read_csv("data/produccion_maiz.csv")


try:
    datos = cargar_datos()

     
    st.subheader(" Editar datos históricos")

    st.write(
        "Puedes modificar los años y la producción, "
        " y/ o agregar nuevos registros o eliminar los existentes."
    )

    datos_editados = st.data_editor(
        datos,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Año": st.column_config.NumberColumn(
                "Año",
                format="%d",
                step=1
            ),
            "Produccion": st.column_config.NumberColumn(
                "Producción (toneladas)",
                format="%.2f",
                min_value=0
            )
        },
        key="editor_datos"
    )

    datos = datos_editados.copy()

    datos["Año"] = pd.to_numeric(
        datos["Año"], errors="coerce"
    )

    datos["Produccion"] = pd.to_numeric(
        datos["Produccion"], errors="coerce"
    )

    if (
        datos.empty
        or datos.isnull().any().any()
        or not (datos["Año"] % 1 == 0).all()
        or (datos["Produccion"] < 0).any()
        or datos["Año"].duplicated().any()
    ):
        st.error(
            "Revisa los datos: no puede haber celdas vacías, "
            "años repetidos, años no enteros ni producciones negativas."
        )
        st.stop()

    datos["Año"] = datos["Año"].astype(int)

    datos = datos.sort_values("Año").reset_index(drop=True)
    
    if st.button(" Guardar cambios", type="primary"):

        datos.to_csv(
            "data/produccion_maiz.csv",
            index=False
        )

        cargar_datos.clear()

        st.success("¡Los datos se guardaron correctamente!")

    st.info(
        "Los cambios realizados en la tabla se reflejan "
        "en los cálculos. Presiona Guardar cambios para "
        "conservarlos en el archivo CSV."
    )    

    st.subheader("Resultados del modelo")

    modelo, pendiente, intercepto, r2, error = entrenar_modelo(datos)

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
        
    )

    st.write(
        "R² indica qué tan dispersos están los datos alrededor de la línea de tendencia. "
        "cuanto más cerca esté de 1, mejor será la ajuste del modelo."
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

    st.dataframe(
        años_futuros,
        use_container_width=True
    )

    st.info(
        "Las predicciones son estimaciones matemáticas basadas en "
        "la tendencia lineal de los datos históricos. No representan "
        "una garantía de producción futura."
    )

    st.caption(
        "Proyecto académico | Datos proporcionados de FAOSTAT"
    )

except Exception as e:
    st.error(
        f"Ocurrió un error al cargar o procesar los datos: {e}"
    )