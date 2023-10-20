import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE


# Función de limpieza
def limpieza_barkeno(df):
        import pandas as pd
        digitos_validos = list(map(str, range(11)))

        df = df[df['pax_reserva'].astype(str).str.strip().isin(digitos_validos)]
 
        df['año_reserva'] = df['dia_reserva'].str.slice(0, 4)
        df['mes_reserva'] = df['dia_reserva'].str.slice(5, 7)
        df['dia_r'] = df['dia_reserva'].str.slice(8, 10)

        df['año_visita'] = df['dia_visita'].str.slice(0, 4)
        df['mes_visita'] = df['dia_visita'].str.slice(5, 7)
        df['dia_v'] = df['dia_visita'].str.slice(8, 10)

        df['dia_reserva'] = pd.to_datetime(df['dia_reserva'], format='%Y%m%d %H:%M:%S')
        df['dia_visita'] = pd.to_datetime(df['dia_visita'], format='%Y%m%d %H:%M:%S')

        # Transformación a formato fecha 

        df['dia_reserva'] = pd.to_datetime(df['dia_reserva'], format='%Y/%m/%d')
        df['dia_visita'] = pd.to_datetime(df['dia_visita'], format='%Y/%m/%d')

        # Dia de la semana y diferencia de dias.

        df['dia_reserva'] = pd.to_datetime(df['dia_reserva'])
        df['dia_visita'] = pd.to_datetime(df['dia_visita'])

        df['nombre_dia_reserva'] = df['dia_reserva'].dt.strftime('%A')
        df['nombre_dia_visita'] = df['dia_visita'].dt.strftime('%A')

        df['diferencia_dias'] = (df['dia_visita'] - df['dia_reserva']).dt.days

    # Categorización diferencias de dias. 
        bins = [0, 7, 14, 30, 60, 180, 365, float('inf')]
        labels = ['Menos de una semana', 'Una semana o más', 'Menos de un mes', '1-2 meses', '3-6 meses', '6-12 meses', 'Más de un año']
        df['categorias_dias'] = pd.cut(df['diferencia_dias'], bins=bins, labels=labels, right=False)


        mapeo_id_origen_reserva = {
    1: 'Barkeno Tours',
    2: 'GuruWalk',
    3: 'Yoorney',
    4: 'FreeTours',
    5: 'Civitatis',
    6: 'ReservaFreeTours',
    7: 'Be Local',
    8: 'Vipealo',
    9: 'Walkative',
    10: 'Buen Dia Tours',
    11: 'PuntoTours',
    12: 'By Foot',
    13: 'My Top Tour',
    14: 'Arkeo Tour',
    15: 'Atrápalo',
    16: 'Viabam'
}

        mapeo_id_idioma_visita = {
    1: 'Castellano',
    2: 'Inglés',
    3: 'Francés',
    4: 'Italiano'
}

        mapeo_id_visita = {
    1: 'Gótico',
    2: 'Modernismo',
    3: 'Raval',
    6: 'Born',
    7: 'Ciutadella',
    8: 'Maó',
    9: 'Tarragona'
}

        df['id_origen_reserva'] = df['id_origen_reserva'].replace(mapeo_id_origen_reserva)
        df['id_idioma_visita'] = df['id_idioma_visita'].replace(mapeo_id_idioma_visita)
        df['id_visita'] = df['id_visita'].replace(mapeo_id_visita)
        df['id_idioma_visita'] = df['id_idioma_visita'].replace(0, 'Castellano')
        df['id_visita'] = df['id_visita'].replace(0, 'Gótico')

        df['id_idioma_visita'] = df['id_idioma_visita'].replace(0, 'Castellano')
        df['hora_visita'] = df['hora_visita'].replace('10:04', '10:00')
        ocurrencias_hora = df['hora_visita'].value_counts()

        df['hora_visita'] = df['hora_visita'].replace('10:04', '10:00')
        ocurrencias_hora = df['hora_visita'].value_counts()

        valores_con_suficientes_ocurrencias = ocurrencias_hora[ocurrencias_hora >= 30].index

        df_filtrado = df[df['hora_visita'].isin(valores_con_suficientes_ocurrencias)]
    
        return df


# Cargar y limpiar los datos
df = pd.read_csv("tu_archivo.csv")
df_modelo = limpieza_barkeno(df)
y2 = df_modelo['realitzat']
X2 = df_modelo.drop(['realitzat'], axis=1)

# Dividir los datos en conjuntos de entrenamiento y prueba
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

# Entrenar el modelo Random Forest con Grid Search y SMOTE
smote = SMOTE(random_state=42)
X_resampled_smote, y_resampled_smote = smote.fit_resample(X2_train, y2_train)

param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None]
}

rf_SMOTE = RandomForestClassifier(random_state=42)
grid_search_rf_SMOTE = GridSearchCV(rf_SMOTE, param_grid_rf, cv=5)
grid_search_rf_SMOTE.fit(X_resampled_smote, y_resampled_smote)
best_rf_SMOTE = grid_search_rf_SMOTE.best_estimator_

# Predecir la probabilidad de que la reserva se realice o no
best_rf_SMOTE.fit(X2_train, y2_train)
probs = best_rf_SMOTE.predict_proba(X2_test)
prob_realizada2 = probs[:, 1]
X2_test['probabilidad_realizada'] = prob_realizada2

# Crear una página web con Streamlit
st.title("Predicción de Reservas de Hotel")

# Añadir una sección para cargar datos
st.header("Cargar Datos")

uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)
    
    # Aplicar la función de limpieza a los datos cargados
    df_modelo = limpieza_barkeno(data)
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_test = df_modelo.drop(['realitzat'], axis=1)
    prob_realizada = best_rf_SMOTE.predict_proba(X_test)[:, 1]
    
    df_modelo['probabilidad_realizada'] = prob_realizada
    st.dataframe(df_modelo)
else:
    st.error("El conjunto de datos no es correcto")


