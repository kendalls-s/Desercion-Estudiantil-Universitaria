from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional
import os

app = FastAPI(title="API Consultas Predicción Graduación")

# Determinar ruta del CSV relativa al script
# __file__ apunta a este script (main.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed"))
DATASET_CSV = os.path.join(BASE_DIR, "Predicciones_Graduacion.csv")

print("Buscando CSV en:", DATASET_CSV)

# Cargar dataset una sola vez al iniciar la API
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

    if df_filtrado.empty:
        return JSONResponse(
            content={"mensaje": "No se encontraron registros que coincidan con los filtros."},
            status_code=404
        )

    return JSONResponse(content=df_filtrado.to_dict(orient="records"))
