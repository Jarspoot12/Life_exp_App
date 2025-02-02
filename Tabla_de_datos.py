import streamlit as st
import pandas as pd

###################################
# Tabla de datos
##################################
st.title("Tabla de datos")
st.write("Los datos que exploraremos están disponibles en la siguiente tabla:")

df = pd.read_csv("./Life_exp_OECD.csv", sep=",")
st.dataframe(df)




# Acomodo de los botones de forma horizontal
col1, col_space, col2 = st.columns([1, 6, 1])  # Dos columnas de igual ancho

# Botón "Anterior" en la primera columna
with col1:
    st.page_link("Introduccion.py", label="Anterior", icon="⬅️")

# # Botón "Siguiente" en la segunda columna
with col2:
    st.page_link("Resumen_estadistico.py", label="Siguiente", icon="➡️")
