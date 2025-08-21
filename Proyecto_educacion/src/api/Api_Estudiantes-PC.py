from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional
app = FastAPI(title="API de predicion de estudiantes", description="API para predecir la probabilidad de aprobar")



# Crear la app
app = FastAPI(title="API Consultas Predicción Graduación")

# Cargar dataset una sola vez al iniciar la API
DATASET_CSV = r"C:\Users\kenda\OneDrive\CUC\Cuatri 4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Predicciones_Graduacion.csv"
try:
    df = pd.read_csv(DATASET_CSV, sep=';')
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {DATASET_CSV}")
    df = pd.DataFrame()
except Exception as e:
    print(f"Error al cargar el dataset: {e}")
    df = pd.DataFrame()


@app.get("/consultar")
def consultar(
    EDAD: Optional[int] = Query(None, description="Edad del estudiante"),
    CARRERA: Optional[str] = Query(None, description="Nombre de la carrera"),
    GRADO_ACADEMICO: Optional[str] = Query(None, description="Grado académico"),
):
    try:
        if df.empty:
            return JSONResponse(
                content={"error": "Dataset no disponible."},
                status_code=500
            )

        df_filtrado = df.copy()

        # Filtrar según parámetros proporcionados
        if EDAD is not None:
            df_filtrado = df_filtrado[df_filtrado['EDAD'] == EDAD]
        if CARRERA is not None:
            df_filtrado = df_filtrado[df_filtrado['CARRERA'].str.contains(CARRERA, case=False, na=False)]
        if GRADO_ACADEMICO is not None:
            df_filtrado = df_filtrado[df_filtrado['GRADO_ACADEMICO'].str.contains(GRADO_ACADEMICO, case=False, na=False)]

        # Verificar si hay resultados
        if df_filtrado.empty:
            return JSONResponse(
                content={"mensaje": "No se encontraron registros que coincidan con los filtros."},
                status_code=404
            )

        # Devolver resultados
        return JSONResponse(content=df_filtrado.to_dict(orient="records"))

    except Exception as e:
        return JSONResponse(
            content={"error": f"Ocurrió un error al procesar la consulta: {str(e)}"},
            status_code=500
        )
