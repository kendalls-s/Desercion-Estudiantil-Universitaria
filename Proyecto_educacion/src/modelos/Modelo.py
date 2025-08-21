import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

class Prediccion:
    def __init__(self):
        pass

    def predecir_prob_graduacion(self, graduados_csv, no_graduados_csv, a_predecir_csv, salida_csv):
        # === 1. Verificar archivos existentes ===
        for archivo in [graduados_csv, no_graduados_csv, a_predecir_csv]:
            if not os.path.isfile(archivo):
                raise FileNotFoundError(f"No se encontró el archivo: {archivo}")

        # === 2. Cargar datasets y eliminar duplicados ===
        graduados = pd.read_csv(graduados_csv, sep=';').drop_duplicates()
        no_graduados = pd.read_csv(no_graduados_csv, sep=';').drop_duplicates()

        # Marcar target
        graduados['GRADUADO'] = 1
        no_graduados['GRADUADO'] = 0

        # Unir datasets para entrenamiento
        train_df = pd.concat([graduados, no_graduados], ignore_index=True)

        # === 3. Preparar features ===
        features = ['EDAD', 'UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']
        X = train_df[features].copy()
        y = train_df['GRADUADO']

        # Codificar variables categóricas
        le_dict = {}
        for col in ['UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            le_dict[col] = le

        # === 4. Dividir y entrenar modelo ===
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluación
        y_pred = model.predict(X_test)
        print("Evaluación del modelo:\n", classification_report(y_test, y_pred))

        # === 5. Predecir para nuevos matriculados ===
        mat_new = pd.read_csv(a_predecir_csv, sep=';').drop_duplicates()

        X_new = mat_new[features].copy()
        for col in ['UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO']:
            # Asignar -1 a los valores desconocidos
            X_new[col] = X_new[col].apply(lambda x: le_dict[col].transform([x])[0]
                                          if x in le_dict[col].classes_ else -1)

        # Filtrar filas válidas (solo las que no tengan -1)
        valid_idx = (X_new >= 0).all(axis=1)
        X_new_valid = X_new.loc[valid_idx]
        mat_new_valid = mat_new.loc[valid_idx].copy()  # <--- usar copy() para evitar warning

        # Predecir probabilidades
        mat_new_valid.loc[:, 'PROB_GRADUACION'] = model.predict_proba(X_new_valid)[:, 1]

        # === 6. Crear carpeta de salida si no existe ===
        os.makedirs(os.path.dirname(salida_csv), exist_ok=True)

        # Guardar en CSV sin duplicados
        mat_new_valid[['EDAD', 'UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO', 'PROB_GRADUACION']]\
            .drop_duplicates()\
            .to_csv(salida_csv, index=False, sep=';')

        print(f"Predicciones guardadas en: {salida_csv}")
        return mat_new_valid[['EDAD', 'UNIVERSIDAD', 'CARRERA', 'GRADO_ACADEMICO', 'PROB_GRADUACION']]
