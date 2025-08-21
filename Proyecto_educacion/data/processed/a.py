import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report


def predecir_prob_graduacion(graduados_csv, no_graduados_csv, a_predecir_csv):
    """
    Entrena un modelo con graduados y no graduados,
    y predice la probabilidad de graduación para un nuevo dataset.

    Args:
        graduados_csv (str): Ruta al CSV de graduados.
        no_graduados_csv (str): Ruta al CSV de no graduados.
        a_predecir_csv (str): Ruta al CSV de personas a predecir.

    Returns:
        pd.DataFrame: Dataset de personas a predecir con columna 'PROB_GRADUACION'.
    """

    # === 1. Cargar datasets ===
    graduados = pd.read_csv(graduados_csv, sep=';')
    no_graduados = pd.read_csv(no_graduados_csv, sep=';')

    # Marcar target
    graduados['GRADUADO'] = 1
    no_graduados['GRADUADO'] = 0

    # Unir datasets para entrenamiento
    train_df = pd.concat([graduados, no_graduados], ignore_index=True)

    # === 2. Preparar features ===
    features = ['EDAD', 'UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']
    X = train_df[features].copy()
    y = train_df['GRADUADO']

    # Codificar variables categóricas
    le_dict = {}
    for col in ['UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']:
        le = LabelEncoder()
        X.loc[:, col] = le.fit_transform(X[col])
        le_dict[col] = le

    # === 3. Dividir y entrenar modelo ===
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluación
    y_pred = model.predict(X_test)
    print("Evaluación del modelo:\n", classification_report(y_test, y_pred))

    # === 4. Predecir para nuevos matriculados ===
    mat_new = pd.read_csv(a_predecir_csv, sep=';')
    X_new = mat_new[features].copy()

    for col in ['UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']:
        X_new.loc[:, col] = X_new[col].map(
            lambda x: le_dict[col].transform([x])[0] if x in le_dict[col].classes_ else -1)

    # Filtrar filas válidas
    X_new_valid = X_new[X_new.min(axis=1) >= 0]
    mat_new_valid = mat_new.loc[X_new_valid.index]

    # Predecir probabilidades
    mat_new_valid['PROB_GRADUACION'] = model.predict_proba(X_new_valid)[:, 1]

    return mat_new_valid[['EDAD', 'UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO', 'PROB_GRADUACION']]


# === Ejemplo de uso ===
resultado = predecir_prob_graduacion("Graduados.csv", "NoGraduados.csv", "Matriculados.csv")
print(resultado.head())
