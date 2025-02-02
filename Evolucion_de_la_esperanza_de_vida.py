import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

df = pd.read_csv("Life_exp_OECD.csv")

st.title("Evolución de la Esperanza de Vida")

###### filtros
# selección de países de interés
st.sidebar.header("Opciones de visualización")

countries = df['Country'].unique()
mex = np.where(countries == 'Mexico')[0] # index de México en el array
sel_countries = st.sidebar.multiselect(
    "Selecciona los países",
    options=countries,
    default=countries[mex]  # selecciona a México como país por defecto
)

# desagrupación por género
gender = st.sidebar.checkbox("Desagrupar por género")


# dataframes útiles para la visualización
df_sel_countries = df[df['Country'].isin(sel_countries)] #dataframe que contiene los datos solamente de los países seleccionados por el usuario


if gender:
    df_filtered = df_sel_countries[df_sel_countries['Gender'] != 'Total']  # excluir el total
else:
    df_filtered = df_sel_countries[df_sel_countries['Gender'] == 'Total']  # mostrar solo totales


# valores mínimo y máximo en las mediciones
min = min(df['Life_exp'])
max = max(df['Life_exp'])
# gráfico para cada país y su filtro de género
if not df_filtered.empty:
    ts_chart = alt.Chart(df_filtered).mark_line().encode(
        x=alt.X('Year:O', title='Año'),  # año de la medición
        y=alt.Y('Life_exp:Q', title='Esperanza de vida',  scale=alt.Scale(domain=[min, max])),  # medida de la esperanza de vida
        color=alt.Color('Country:N', legend=alt.Legend(title="País")),  # color para cada país
        strokeDash=alt.StrokeDash('Gender:N', legend=alt.Legend(title="Género"))   # línea discontinua para cada género
    ).properties(
        width=800,
        height=400,
        title="Evolución de la Esperanza de Vida"
    )
    st.altair_chart(ts_chart, use_container_width=True)
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")


# Acomodo de los botones de forma horizontal
col1, col_space, col2 = st.columns([1, 6, 1])  # Dos columnas de igual ancho

# Botón "Anterior" en la primera columna
with col1:
    st.page_link("Distribucion_de_la_esperanza_de_vida.py", label="Anterior", icon="⬅️")

