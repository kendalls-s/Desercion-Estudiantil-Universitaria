import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, pointbiserialr, f_oneway
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Cargar los datos
df = pd.read_csv(r"C:\Users\kenda\OneDrive\CUC\Cuatri_4\BD\Progra_2\Proyecto_final\Proyecto_educacion\data\processed\Graduados.csv", sep=';', encoding='utf-8-sig')

# Información básica del dataset
print("Dimensiones del dataset:", df.shape)
print("\nTipos de datos:")
print(df.dtypes)
print("\nValores únicos por columna:")
for col in df.columns:
    print(f"{col}: {df[col].nunique()}")


# Preparar datos para análisis
# Eliminar columnas con un único valor (no aportan información)
df = df.drop(['AÑO', 'SECTOR_UNIVERSITARIO', 'UNIVERSIDAD'], axis=1)

# Codificar variables categóricas para algunas correlaciones
label_encoders = {}
categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# 1. Correlación entre variables numéricas (solo EDAD)
print("="*50)
print("CORRELACIONES ENTRE VARIABLES NUMÉRICAS")
print("="*50)
# Solo tenemos una variable numérica (EDAD), por lo que no hay correlaciones numéricas que calcular
print("Solo existe una variable numérica (EDAD) en el dataset")

# 2. Correlaciones entre variables categóricas y numéricas
print("\n" + "="*60)
print("CORRELACIONES ENTRE VARIABLES CATEGÓRICAS Y NUMÉRICAS")
print("="*60)

# Para variables binarias usaremos point-biserial
binary_cols = [col for col in categorical_cols if df[col].nunique() == 2]
print("Correlaciones Point-Biserial (variables binarias vs EDAD):")
for col in binary_cols:
    correlation, p_value = pointbiserialr(df[col + '_encoded'], df['EDAD'])
    print(f"{col} vs EDAD: Correlación = {correlation:.4f}, p-value = {p_value:.4f}")

# Para variables categóricas con más de 2 categorías usaremos ANOVA
multi_cat_cols = [col for col in categorical_cols if df[col].nunique() > 2]
print("\nANOVA (variables categóricas múltiples vs EDAD):")
for col in multi_cat_cols:
    groups = [df[df[col] == category]['EDAD'] for category in df[col].unique()]
    f_stat, p_value = f_oneway(*groups)
    eta_squared = f_stat / (f_stat + (len(df) - len(groups)) / (len(groups) - 1))
    print(f"{col} vs EDAD: F = {f_stat:.4f}, p-value = {p_value:.4f}, Eta² = {eta_squared:.4f}")

# 3. Correlaciones entre variables categóricas
print("\n" + "="*50)
print("CORRELACIONES ENTRE VARIABLES CATEGÓRICAS")
print("="*50)

# Función para calcular V de Cramér
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

# Calcular matriz de correlación para variables categóricas
cat_corr_matrix = pd.DataFrame(index=categorical_cols, columns=categorical_cols)

for i, col1 in enumerate(categorical_cols):
    for j, col2 in enumerate(categorical_cols):
        if i <= j:  # Calcular solo la mitad para evitar duplicados
            if col1 == col2:
                cat_corr_matrix.loc[col1, col2] = 1.0
            else:
                v = cramers_v(df[col1], df[col2])
                cat_corr_matrix.loc[col1, col2] = v
                cat_corr_matrix.loc[col2, col1] = v

print("Matriz de correlación (V de Cramér) entre variables categóricas:")
print(cat_corr_matrix.astype(float).round(4))

# 4. Visualización de correlaciones
plt.figure(figsize=(12, 10))
sns.heatmap(cat_corr_matrix.astype(float), annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlación (V de Cramér) entre Variables Categóricas')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300)
plt.show()

# 5. Análisis de las correlaciones más fuertes
print("\n" + "="*60)
print("CORRELACIONES MÁS FUERTES ENTRE VARIABLES")
print("="*60)

# Encontrar las 10 correlaciones más fuertes (excluyendo la diagonal)
strong_correlations = []
for i, col1 in enumerate(categorical_cols):
    for j, col2 in enumerate(categorical_cols):
        if i < j:  # Solo la mitad superior, excluyendo la diagonal
            corr_value = cat_corr_matrix.loc[col1, col2]
            strong_correlations.append((col1, col2, corr_value))

# Ordenar por valor absoluto de correlación
strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)

print("Top 10 correlaciones más fuertes:")
for i, (col1, col2, corr) in enumerate(strong_correlations[:10]):
    print(f"{i+1}. {col1} - {col2}: {corr:.4f}")

# 6. Análisis de relación entre ubicaciones geográficas
print("\n" + "="*60)
print("ANÁLISIS DE CORRELACIONES GEOGRÁFICAS")
print("="*60)

geo_cols = ['PROVINCIA_GRADUADO', 'CANTON_GRADUADO', 'REGION_PLANIFICACION_GRADUADO',
            'ZONA_URBANO_RURAL_GRADUADO', 'GAM_ESTUDIANTE', 'GAM_SEDE']

for i, col1 in enumerate(geo_cols):
    for j, col2 in enumerate(geo_cols):
        if i < j:
            v = cramers_v(df[col1], df[col2])
            print(f"{col1} - {col2}: {v:.4f}")
