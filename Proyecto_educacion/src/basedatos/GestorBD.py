import pyodbc
import pandas as pd

class GestorBaseDatos:
    def __init__(self):
        """Configura los parámetros de conexión a SQL Server"""
        # Parámetros de conexión PC\\MSSQLSERVER01   DESKTOP-1TS3J5B\\SQLEXPRESS
        self.DB_CONFIG = {
            "driver": "ODBC Driver 17 for SQL Server",
            "server": "PC\\MSSQLSERVER01",
            "database": "Datos_Universidades",
            "trusted": "yes"
        }
        self.CONN_STR = (
            f"DRIVER={{{self.DB_CONFIG['driver']}}};"
            f"SERVER={self.DB_CONFIG['server']};"
            f"DATABASE={self.DB_CONFIG['database']};"
            f"Trusted_Connection={self.DB_CONFIG['trusted']};"
        )

    def obtener_tabla(self, nombre_tabla):
        """Devuelve la tabla completa como DataFrame"""
        query = f"SELECT * FROM {nombre_tabla}"
        with pyodbc.connect(self.CONN_STR) as conn:
            df = pd.read_sql(query, conn)
        return df

    def obtener_datos(self):
        """Trae las dos tablas guardadas en la base de datos"""
        df_matriculados = self.obtener_tabla("matriculados")
        df_graduados = self.obtener_tabla("graduados")
        return df_matriculados, df_graduados