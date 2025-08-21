# dashboard_graduados.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DashboardGraduados:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        sns.set(style="whitegrid")
        plt.rcParams["figure.facecolor"] = "white"

    # ========================
    # Filtros
    # ========================
    def filtrar_datos(self, carrera=None, regiones=None):
        df_filtered = self.df.copy()
        if carrera:
            df_filtered = df_filtered[df_filtered["CARRERA"] == carrera]
        if regiones:
            df_filtered = df_filtered[df_filtered["REGION_PLANIFICACION_GRADUADO"].isin(regiones)]
        return df_filtered

    # ========================
    # Métricas
    # ========================
    def mostrar_metricas(self, df):
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de graduados", len(df))
        col2.metric("Edad promedio", round(df["EDAD"].mean(), 1))
        col3.metric("Modalidad más común", df["NIVEL_ACADEMICO"].mode()[0] if not df["NIVEL_ACADEMICO"].mode().empty else "N/A")

    # ========================
    # Gráficos
    # ========================
    def grafico_distribucion_edad(self, df):
        st.subheader("Distribución por edad")
        fig, ax = plt.subplots()
        sns.histplot(df["EDAD"], bins=10, kde=True, ax=ax, color="#2c7fb8")
        st.pyplot(fig)

    def grafico_graduados_provincia(self, df):
        st.subheader("Graduados por provincia")
        provincia_count = df["PROVINCIA_GRADUADO"].value_counts()
        st.bar_chart(provincia_count)

    # ========================
    # Tabla y descarga
    # ========================
    def mostrar_tabla(self, df):
        st.subheader("Datos filtrados")
        st.dataframe(df)

    def descargar_csv(self, df):
        csv = df.to_csv(index=False)
        st.download_button("Descargar CSV", data=csv, file_name="graduados_filtrados.csv")
