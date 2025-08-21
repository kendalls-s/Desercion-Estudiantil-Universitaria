import pandas as pd
from eda.eda_universidades import EDAUniversidades
from datos.Limpieza import Limpieza
from modelos.Modelo import Prediccion
import requests
from IPython.display import Image, display
from visualizaciones.app import DashboardGraduados
import streamlit as st
import warnings

warnings.filterwarnings('ignore')

# =========================== LIMPIEZA ============================================
# Crear instancia de la clase
# limpieza = Limpieza()

# Ejecutar métodos de limpieza
# limpieza.Limpieza_matricula_actual()
# limpieza.Limpieza_matricula_historicos()
# limpieza.Limpieza_graduados()
# limpieza.Sin_Graduar()

# =========================== MODELO ==============================================
# Crear la instancia
# lr = Prediccion()

# Llamar al método de instancia con los 4 parámetros
# resultado = lr.predecir_prob_graduacion(
#     r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Graduados_UCR.csv",
#     r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Solo_Matriculados_NoGraduados.csv",
#     r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Matriculados_UCR.csv",
#     r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Predicciones_Graduacion.csv"
# )

# =========================== EDA =================================================
df = pd.read_csv("C:/Users/kenda/OneDrive/CUC/Cuatri_4/BD/Progra_2/Proyecto_final/Proyecto_educacion/data/processed/Graduados.csv",
                 sep=';', encoding='utf-8-sig')

# Instancia EDA
eda = EDAUniversidades(df)

# Resumen general
eda.resumen_general()

# Visualizaciones
eda.diplomas_por_anio()
eda.diplomas_por_sector()
eda.diplomas_por_universidad(top_n=10)
eda.grados_academicos()
eda.carreras_mas_frecuentes(top_n=10)
eda.sedes_conare(top_n=10)


# =========================== API =================================================
# Probar análisis
# resp = requests.get("http://127.0.0.1:8000/consultar")
# print(resp.json())

# ========================== STREAMLIT ===========================================
# st.set_page_config(page_title="Dashboard Graduados", layout="wide")
# st.title("Dashboard de Graduados")
# df = pd.read_csv("C:/Users/kenda/OneDrive/CUC/Cuatri_4/BD/Progra_2/Proyecto_final/Proyecto_educacion/data/processed/Graduados.csv", sep=';', encoding='utf-8-sig')
# dashboard = DashboardGraduados(df)

# # ========================= Sidebar: filtros =========================
# st.sidebar.header("Filtros")
# carrera_seleccionada = st.sidebar.selectbox(
#     "Seleccionar carrera",
#     options=[None] + df["CARRERA"].dropna().unique().tolist()
# )
# regiones_seleccionadas = st.sidebar.multiselect(
#     "Seleccionar región(es)",
#     options=df["REGION_PLANIFICACION_GRADUADO"].dropna().unique().tolist()
# )

# # ========================= Aplicar filtros =========================
# df_filtrado = dashboard.filtrar_datos(
#     carrera=carrera_seleccionada,
#     regiones=regiones_seleccionadas
# )

# # ========================= Mostrar métricas ========================
# dashboard.mostrar_metricas(df_filtrado)

# # ========================= Mostrar gráficos ========================
# dashboard.grafico_distribucion_edad(df_filtrado)
# dashboard.grafico_graduados_provincia(df_filtrado)

# # ========================= Tabla y descarga ========================
# dashboard.mostrar_tabla(df_filtrado)
# dashboard.descargar_csv(df_filtrado)
