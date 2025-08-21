import pandas as pd
import os

class Limpieza:

    def Limpieza_matricula_actual(self):
        archivo_entrada = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\raw\BD_Matrícula_Sector_Estatal_2021_2024.xlsx"
        df = pd.read_excel(archivo_entrada, sheet_name="Archivo 2021-2024")

        # Seleccionar columnas importantes
        columnas_deseadas = [0, 2, 6, 7, 8, 16]
        df_filtrado = df.iloc[:, columnas_deseadas].copy()
        df_filtrado.dropna(inplace=True)

        # Renombrar columnas
        df_filtrado.columns = ["AÑO", "UNIVERSIDAD", "CARRERA", "GRADO_ACADEMICO", "NIVEL_ACADEMICO", "EDAD"]

        # Asegurar que EDAD sea numérica
        df_filtrado = df_filtrado[pd.to_numeric(df_filtrado["EDAD"], errors='coerce').notnull()]

        # Revisar valores únicos (para confirmar nombres)
        print("Universidades únicas:", df_filtrado["UNIVERSIDAD"].unique())
        print("Grados académicos únicos:", df_filtrado["GRADO_ACADEMICO"].unique())

        # Filtrar solo Universidad de Costa Rica
        df_ucr = df_filtrado[df_filtrado["UNIVERSIDAD"].str.strip() == "Universidad de Costa Rica"].copy()

        # Carpeta de salida
        carpeta_salida = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed"
        os.makedirs(carpeta_salida, exist_ok=True)

        # Guardar CSVs
        df_filtrado.to_csv(os.path.join(carpeta_salida, "Matriculados.csv"), index=False, sep=';', encoding="utf-8-sig")
        df_ucr.to_csv(os.path.join(carpeta_salida, "Matriculados_UCR.csv"), index=False, sep=';', encoding="utf-8-sig")

        print("✅ Archivos guardados: Matriculados.csv y Matriculados_UCR.csv")

    def Limpieza_matricula_historicos(self):
        archivo_entrada = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\raw\BD_Matrícula_Sector_Estatal_2016-2020.xlsx"
        df = pd.read_excel(archivo_entrada, sheet_name="Archivo 2016-2020")

        columnas_deseadas = [0, 2, 6, 7, 8, 16]
        df_filtrado = df.iloc[:, columnas_deseadas].copy()
        df_filtrado.dropna(inplace=True)

        # Renombrar columnas
        df_filtrado.columns = ["AÑO", "UNIVERSIDAD", "CARRERA", "GRADO_ACADEMICO", "NIVEL_ACADEMICO", "EDAD"]

        # Asegurar que EDAD sea numérica
        df_filtrado = df_filtrado[pd.to_numeric(df_filtrado["EDAD"], errors='coerce').notnull()]

        # Revisar valores únicos (para confirmar nombres)
        print("Universidades únicas:", df_filtrado["UNIVERSIDAD"].unique())
        print("Grados académicos únicos:", df_filtrado["GRADO_ACADEMICO"].unique())

        # Filtrar solo Universidad de Costa Rica
        df_ucr = df_filtrado[df_filtrado["UNIVERSIDAD"].str.strip() == "Universidad de Costa Rica"].copy()

        # Carpeta de salida
        carpeta_salida = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed"
        os.makedirs(carpeta_salida, exist_ok=True)

        df_filtrado.to_csv(os.path.join(carpeta_salida, "Matriculados_historicos.csv"), index=False, sep=';', encoding="utf-8-sig")
        df_ucr.to_csv(os.path.join(carpeta_salida, "Matriculados_UCR_historicos.csv"), index=False, sep=';', encoding="utf-8-sig")

        print("✅ Archivos guardados: Matriculados_historicos.csv y Matriculados_UCR_historicos.csv")

    def Limpieza_graduados(self):
        archivo_entrada = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\raw\BD_Diplomas_sector_estatal_y_privado_2021_2024.xlsx"
        df = pd.read_excel(archivo_entrada, sheet_name="Diplomas 2021-2023")

        columnas_deseadas = [0,1,2,3,4,6,7,8,15,16,17,18,19,20,21]
        df_filtrado = df.iloc[:, columnas_deseadas].copy()
        df_filtrado.dropna(inplace=True)

        df_ucr = df_filtrado[df_filtrado.iloc[:, 2] == "Universidad de Costa Rica"].copy()

        carpeta_salida = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed"
        os.makedirs(carpeta_salida, exist_ok=True)

        df_filtrado.to_csv(os.path.join(carpeta_salida, "Graduados.csv"), index=False, sep=';', encoding="utf-8-sig")
        df_ucr.to_csv(os.path.join(carpeta_salida, "Graduados_UCR.csv"), index=False, sep=';', encoding="utf-8-sig")

        print("✅ Archivos guardados: Graduados.csv y Graduados_UCR.csv")

    def Sin_Graduar(self):
        # Rutas de los archivos CSV
        archivo_graduados = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Graduados_UCR.csv"
        archivo_matriculados = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Matriculados_UCR_historicos.csv"
        archivo_salida = r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Solo_Matriculados_NoGraduados.csv"

        # Columnas a comparar excepto AÑO
        columnas_clave = ["UNIVERSIDAD", "CARRERA", "GRADO_ACADEMICO", "NIVEL_ACADEMICO", "EDAD"]

        # Leer los CSV
        df_graduados = pd.read_csv(archivo_graduados, sep=";")
        df_matriculados = pd.read_csv(archivo_matriculados, sep=";")

        # Función para obtener límite de años según grado
        def limite_anio(grado):
            if str(grado).strip().lower() == "bachiller":
                return 4
            elif str(grado).strip().lower() == "licenciatura":
                return 6
            else:
                return 0  # otros grados no se consideran iguales

        # Función para marcar filas que coinciden según las condiciones
        def es_graduado(row):
            coincidencias = df_graduados
            for col in columnas_clave:
                coincidencias = coincidencias[coincidencias[col] == row[col]]
            for _, r in coincidencias.iterrows():
                max_diferencia = limite_anio(row["GRADO_ACADEMICO"])
                if max_diferencia > 0 and abs(r["AÑO"] - row["AÑO"]) < max_diferencia:
                    return True
            return False

        # Filtrar solo los matriculados que NO están en graduados
        df_solo_matriculados = df_matriculados[~df_matriculados.apply(es_graduado, axis=1)]

        # Guardar el resultado
        df_solo_matriculados.to_csv(archivo_salida, index=False, sep=";")

        print(f"Proceso completado. Solo los matriculados no graduados se guardaron en '{archivo_salida}'.")


