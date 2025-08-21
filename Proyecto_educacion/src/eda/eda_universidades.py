import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, pointbiserialr, f_oneway
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class EDAUniversidades:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        # Estilo sobrio y profesional
        sns.set(style="whitegrid", palette="deep")
        plt.rcParams["figure.facecolor"] = "white"
        plt.rcParams["axes.facecolor"] = "#f5f5f5"
        plt.rcParams["axes.edgecolor"] = "#333333"
        plt.rcParams["axes.labelcolor"] = "#333333"
        plt.rcParams["text.color"] = "#333333"
        plt.rcParams["axes.titleweight"] = "bold"

    def _check_column(self, col_name):
        if col_name not in self.df.columns:
            print(f"⚠ Columna '{col_name}' no encontrada en el DataFrame.")
            return False
        return True

    # ---------- Métodos de EDA original ----------
    def resumen_general(self):
        print("===== Resumen General =====")
        print(self.df.info())
        print("\nDescripción estadística:")
        print(self.df.describe(include='all'))
        print("\nValores nulos:")
        print(self.df.isnull().sum())

    def diplomas_por_anio(self):
        if not self._check_column('AÑO'):
            return
        conteo = self.df['AÑO'].value_counts().sort_index()
        print("\n===== Diplomas por Año =====")
        print(conteo)

        plt.plot(conteo.index, conteo.values, marker="o", color="#2825be", linewidth=2, label="Tendencia")
        plt.fill_between(conteo.index, conteo.values, color="#8a89e6", alpha=0.3)
        plt.title("Diplomas por Año (Evolución)")
        plt.xlabel("Año")
        plt.ylabel("Cantidad de Diplomas")
        plt.legend()
        plt.show()

    def diplomas_por_sector(self):
        if not self._check_column('SECTOR_UNIVERSITARIO'):
            return
        conteo = self.df['SECTOR_UNIVERSITARIO'].value_counts()
        print("\n===== Diplomas por Sector Universitario =====")
        print(conteo)
        sns.barplot(x=conteo.index, y=conteo.values, color="#146916")
        plt.title("Diplomas por Sector Universitario")
        plt.xlabel("Sector")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=30)
        plt.show()

    def diplomas_por_universidad(self, top_n=10):
        if not self._check_column('UNIVERSIDAD'):
            return
        conteo = self.df['UNIVERSIDAD'].value_counts().nlargest(top_n).sort_values(ascending=True)
        print(f"\n===== Top {top_n} Universidades =====")
        print(conteo)
        sns.barplot(x=conteo.values, y=conteo.index, color="#5f5e13")
        plt.title(f"Top {top_n} Universidades con más Diplomas")
        plt.xlabel("Cantidad de Diplomas")
        plt.ylabel("Universidad")
        plt.show()

    def grados_academicos(self):
        if not self._check_column('GRADO_ACADEMICO'):
            return
        conteo = self.df['GRADO_ACADEMICO'].value_counts()
        print("\n===== Grados Académicos =====")
        print(conteo)
        sns.histplot(self.df['GRADO_ACADEMICO'], discrete=True, color="#981e28")
        plt.title("Distribución de Grados Académicos")
        plt.xlabel("Grado Académico")
        plt.ylabel("Frecuencia")
        plt.xticks(rotation=30)
        plt.show()

    def carreras_mas_frecuentes(self, top_n=10):
        if not self._check_column('CARRERA'):
            return
        conteo = self.df['CARRERA'].value_counts().nlargest(top_n).sort_values(ascending=False)
        print(f"\n===== Top {top_n} Carreras =====")
        print(conteo)

        plt.fill_between(range(len(conteo.index)), conteo.values, color="#167265", alpha=0.5)
        plt.plot(range(len(conteo.index)), conteo.values, marker="o", color="#0a3d34", linewidth=2)
        plt.title(f"Top {top_n} Carreras con más Diplomas")
        plt.xlabel("Carrera")
        plt.ylabel("Cantidad")
        plt.xticks(range(len(conteo.index)), conteo.index, rotation=30)
        plt.show()

    def sedes_conare(self, top_n=10):
        if not self._check_column('SEDE_CONARE'):
            return
        conteo = self.df['SEDE_CONARE'].value_counts().nlargest(top_n)
        print(f"\n===== Top {top_n} Sedes CONARE =====")
        print(conteo)

        plt.plot(conteo.index, conteo.values, marker="o", linestyle="-", color="#5c25be")
        plt.title(f"Top {top_n} Sedes CONARE con más Diplomas")
        plt.xlabel("Sede")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=30)
        plt.show()

    # ---------- NUEVOS MÉTODOS DE CORRELACIÓN ----------
    def preparar_datos_correlacion(self):
        """Prepara datos para análisis de correlación: elimina columnas irrelevantes y codifica variables categóricas."""
        self.df_corr = self.df.copy()
        # Eliminar columnas con un único valor
        for col in ['AÑO', 'SECTOR_UNIVERSITARIO', 'UNIVERSIDAD']:
            if col in self.df_corr.columns:
                self.df_corr = self.df_corr.drop(col, axis=1)

        # Codificar variables categóricas
        self.label_encoders = {}
        self.categorical_cols = self.df_corr.select_dtypes(include=['object']).columns
        for col in self.categorical_cols:
            le = LabelEncoder()
            self.df_corr[col + '_encoded'] = le.fit_transform(self.df_corr[col].astype(str))
            self.label_encoders[col] = le
        print("Preparación de datos finalizada.")

    def correlaciones_numericas(self):
        """Correlaciones entre variables numéricas."""
        numeric_cols = self.df_corr.select_dtypes(include=['int64', 'float64']).columns
        print("="*50)
        print("CORRELACIONES ENTRE VARIABLES NUMÉRICAS")
        print("="*50)
        print(self.df_corr[numeric_cols].corr())

    def correlaciones_categoricas_numericas(self):
        """Correlaciones entre variables categóricas y numéricas (Point-Biserial y ANOVA)."""
        print("\n" + "="*60)
        print("CORRELACIONES ENTRE VARIABLES CATEGÓRICAS Y NUMÉRICAS")
        print("="*60)
        if 'EDAD' not in self.df_corr.columns:
            print("No existe la variable EDAD para correlaciones.")
            return

        # Point-biserial para binarias
        binary_cols = [col for col in self.categorical_cols if self.df_corr[col].nunique() == 2]
        print("Correlaciones Point-Biserial (variables binarias vs EDAD):")
        for col in binary_cols:
            correlation, p_value = pointbiserialr(self.df_corr[col + '_encoded'], self.df_corr['EDAD'])
            print(f"{col} vs EDAD: Correlación = {correlation:.4f}, p-value = {p_value:.4f}")

        # ANOVA para variables categóricas con más de 2 categorías
        multi_cat_cols = [col for col in self.categorical_cols if self.df_corr[col].nunique() > 2]
        print("\nANOVA (variables categóricas múltiples vs EDAD):")
        for col in multi_cat_cols:
            groups = [self.df_corr[self.df_corr[col] == category]['EDAD'] for category in self.df_corr[col].unique()]
            f_stat, p_value = f_oneway(*groups)
            eta_squared = f_stat / (f_stat + (len(self.df_corr) - len(groups)) / (len(groups) - 1))
            print(f"{col} vs EDAD: F = {f_stat:.4f}, p-value = {p_value:.4f}, Eta² = {eta_squared:.4f}")

    def correlaciones_categoricas(self):
        """Correlaciones entre variables categóricas usando V de Cramér."""
        print("\n" + "="*50)
        print("CORRELACIONES ENTRE VARIABLES CATEGÓRICAS")
        print("="*50)

        def cramers_v(x, y):
            confusion_matrix = pd.crosstab(x, y)
            chi2 = chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2 / n
            r, k = confusion_matrix.shape
            phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
            rcorr = r - ((r-1)**2)/(n-1)
            kcorr = k - ((k-1)**2)/(n-1)
            return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

        cat_corr_matrix = pd.DataFrame(index=self.categorical_cols, columns=self.categorical_cols)
        for i, col1 in enumerate(self.categorical_cols):
            for j, col2 in enumerate(self.categorical_cols):
                if i <= j:
                    if col1 == col2:
                        cat_corr_matrix.loc[col1, col2] = 1.0
                    else:
                        v = cramers_v(self.df_corr[col1], self.df_corr[col2])
                        cat_corr_matrix.loc[col1, col2] = v
                        cat_corr_matrix.loc[col2, col1] = v

        print("Matriz de correlación (V de Cramér) entre variables categóricas:")
        print(cat_corr_matrix.astype(float).round(4))

        # Heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(cat_corr_matrix.astype(float), annot=True, cmap='coolwarm', center=0)
        plt.title('Matriz de Correlación (V de Cramér) entre Variables Categóricas')
        plt.tight_layout()
        plt.show()

    def top_correlaciones(self, top_n=10):
        """Imprime las top N correlaciones más fuertes entre variables categóricas."""
        strong_correlations = []
        for i, col1 in enumerate(self.categorical_cols):
            for j, col2 in enumerate(self.categorical_cols):
                if i < j:
                    corr_value = cramers_v(self.df_corr[col1], self.df_corr[col2])
                    strong_correlations.append((col1, col2, corr_value))

        strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
        print(f"Top {top_n} correlaciones más fuertes:")
        for i, (col1, col2, corr) in enumerate(strong_correlations[:top_n]):
            print(f"{i+1}. {col1} - {col2}: {corr:.4f}")
