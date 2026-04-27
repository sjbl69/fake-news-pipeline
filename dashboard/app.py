import streamlit as st
import pandas as pd
import time
import os

# CONFIG
st.set_page_config(page_title="KPI Pipeline ETL", layout="wide")

st.title("Fake News Detection Pipeline - Monitoring Dashboard")

# LOAD DATA
@st.cache_data
def load_data():
    file_path = "data/processed/processed_news.csv"
    
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    return df

df = load_data()

# KPI CALCUL
if df.empty:
    st.error(" Aucune donnée trouvée. Lance d'abord ton pipeline.")
else:
    total_rows = len(df)

    valid_rows = df.dropna().shape[0]
    invalid_rows = total_rows - valid_rows

    validity_rate = (valid_rows / total_rows) * 100

    # Simulation temps (à remplacer par vrai log plus tard)
    execution_time = round(total_rows * 0.002, 2)  # simulation

    # Simulation coût
    cost_estimation = round(total_rows * 0.0001, 2)

    # KPI DISPLAY
    col1, col2, col3 = st.columns(3)

    col1.metric(" Données totales", total_rows)
    col2.metric(" % données valides", f"{validity_rate:.2f}%")
    col3.metric(" Temps estimé (s)", execution_time)

    st.markdown("---")

    col4, col5 = st.columns(2)

    col4.metric(" Données invalides", invalid_rows)
    col5.metric(" Coût estimé (€)", cost_estimation)

    st.markdown("---")

    # VISUALISATIONS
    st.subheader(" Répartition des données")

    chart_data = pd.DataFrame({
        "Type": ["Valides", "Invalides"],
        "Nombre": [valid_rows, invalid_rows]
    })

    st.bar_chart(chart_data.set_index("Type"))

    st.subheader(" Aperçu des données")
    st.dataframe(df.head(20))