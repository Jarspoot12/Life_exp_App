import streamlit as st
import pandas as pd

## función para calcular las métricas
def stats(df):
    return {
        'mean': round(df['Life_exp'].mean(), 2),
        'std': round(df['Life_exp'].std(), 2),
        'min': df['Life_exp'].min(),
        'max': df['Life_exp'].max()
    }

# función para mostrar las métricas en tarjetas
def showStats(stats1, stats2, year): #stats1: año de interés; stats2: año anterior; year: año actual
    a, b = st.columns(2)
    c, d = st.columns(2)
    if year!=2015: # para todos los años, menos el 2015 porque no tiene año previo registrado
        a.metric(label="Promedio", value=stats1['mean'], delta=f"{(stats1['mean']-stats2['mean']).round(decimals=2)} que el año anterior", border=True)
        b.metric(label="Desviación estandar", value=stats1['std'], delta=f"{(stats1['std']-stats2['std']).round(decimals=2)} que el año anterior", border=True)
        c.metric(label="Valor mínimo", value=stats1['min'], delta=f"{(stats1['min']-stats2['min']).round(decimals=2)} que el año anterior", border=True)
        d.metric(label="Valor máximo", value=stats1['max'], delta=f"{(stats1['max']-stats2['max']).round(decimals=2)} que el año anterior", border=True)
    else:
        a.metric(label="Promedio", value=stats1['mean'], border=True)
        b.metric(label="Desviación estandar", value=stats1['std'], border=True)
        c.metric(label="Valor mínimo", value=stats1['min'], border=True)
        d.metric(label="Valor máximo", value=stats1['max'], border=True)




# dataframe base
df = pd.read_csv("./Life_exp_OECD.csv", sep=",")

st.title("Medidas estadísticas")

## parámtros de filtrado
with st.container(border=True): # almacenamos el filtrado dentro de un contenedor

    # selección del año
    year = st.radio('Seleccione el año', options=range(2015, 2024), index=8, horizontal=True)

    # selección de agrupamientos
    st.write("Seleccione los agrupamientos deseados")
    col1, col2, col3 = st.columns([5, 1, 5])
    with col1:
        filter_oecd = st.checkbox('Desagrupar por pertenencia a la OECD')
    with col3:
        filter_gender = st.checkbox('Desagrupar por género')


## datos filtrados por año
df_year = df[df['Year'] == year] # aseguramos que los registros no se repitan y solo se tome el año de interés
df_year_prev = df[df['Year'] == year-1] # usamos el año previo para métricas comparativas


# mostramos los grids generados a partir de los filtros

###### grid por defecto, cuando aún no se han realizado desagrumpamientos y se muestra la información total
if not filter_oecd and not filter_gender:
    # Sin desagrupar: mostrar todos los datos
    stats_total = stats(df_year[df_year['Gender'] == 'Total']) # estadísticas del año actual para el total de la población
    stats_prev_total = stats(df_year_prev[df_year_prev['Gender'] == 'Total']) # estadísticas del año anterior
    st.write("### Métricas para todos los países listados")
    # st.write(pd.DataFrame.from_dict(stats, orient='index', columns=['Valor']))
    # mostramos métricas (promedio, estd, min y max)
    a, b = st.columns(2)
    c, d = st.columns(2)
    showStats(stats_total, stats_prev_total, year)

###### grids deagrupando por miembros de la OECD (y no miembros)
elif filter_oecd and not filter_gender:
    # países miembros de la OECD
    stats_a_OECD = stats(df_year[(df_year['Gender'] == 'Total') & (df_year['OECD'] == True)]) # estadísticas del año actual
    stats_prev_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Total') & (df_year_prev['OECD'] == True)]) # estadísticas del año anterior
    st.write("### Métricas para miembros de la OECD")
    showStats(stats_a_OECD, stats_prev_OECD, year)

    # países no miembros de la OECD
    stats_a_not_OECD = stats(df_year[(df_year['Gender'] == 'Total') & (df_year['OECD'] == False)]) # estadísticas del año actual
    stats_prev_not_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Total') & (df_year_prev['OECD'] == False)]) # estadísticas del año anterior
    st.write("### Métricas para países restantes (no miembros)")
    showStats(stats_a_not_OECD, stats_prev_not_OECD, year)

# grids desagrupando por género
elif not filter_oecd and filter_gender:
    # agrupado por hombres de todos los países
    stats_a_male = stats(df_year[df_year['Gender'] == 'Male'])
    stats_prev_male = stats(df_year_prev[df_year_prev['Gender'] == 'Male'])
    st.write("### Métricas para hombres de todos los países")
    showStats(stats_a_male, stats_prev_male, year)

    # agrupado por mujeres de todos los países
    stats_a_fem = stats(df_year[df_year['Gender'] == 'Female'])
    stats_prev_fem =  stats(df_year_prev[df_year_prev['Gender'] == 'Female'])
    st.write("### Métricas para mujeres de todos los países")
    showStats(stats_a_fem, stats_prev_fem, year)

# grids desagrupando por género y pertenencia a la OECD
elif filter_oecd and filter_gender:
    st.write("")
    st.write("")
    # agrupado por hombres pertenecientes a la OECD
    st.markdown("<h3><center>Hombres</center></h3>", unsafe_allow_html=True)
    stats_a_male_OECD = stats(df_year[(df_year['Gender'] == 'Male') & (df_year['OECD'] == True)])
    stats_prev_male_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Male') & (df_year_prev['OECD'] == True)])
    st.write("### Métricas para países meimbros de la OECD")
    showStats(stats_a_male_OECD, stats_prev_male_OECD, year)

    # agrupado por hombres no miembros de la OECD
    stats_a_male_not_OECD = stats(df_year[(df_year['Gender'] == 'Male') & (df_year['OECD'] == False)])
    stats_prev_male_not_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Male') & (df_year_prev['OECD'] == False)])
    st.write("### Métricas para países restantes")
    showStats(stats_a_male_not_OECD, stats_prev_male_not_OECD, year)
    st.write("") #espacio en blanco

    # agrupado por mujeres pertenecientes a la OECD
    st.markdown("<h3><center>Mujeres</center></h3>", unsafe_allow_html=True)
    stats_a_fem_OECD = stats(df_year[(df_year['Gender'] == 'Female') & (df_year['OECD'] == True)])
    stats_prev_fem_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Female') & (df_year_prev['OECD'] == True)])
    st.write("### Métricas para países meimbros de la OECD")
    showStats(stats_a_fem_OECD, stats_prev_fem_OECD, year)

    # agrupado por mujeres no miembros de la OECD
    stats_a_fem_not_OECD = stats(df_year[(df_year['Gender'] == 'Female') & (df_year['OECD'] == False)])
    stats_prev_fem_not_OECD = stats(df_year_prev[(df_year_prev['Gender'] == 'Female') & (df_year_prev['OECD'] == False)])
    st.write("### Métricas para países restantes")
    showStats(stats_a_fem_not_OECD, stats_prev_fem_not_OECD, year)


# Acomodo de los botones de forma horizontal
col1, col_space, col2 = st.columns([1, 6, 1])  # Dos columnas de igual ancho

# Botón "Anterior" en la primera columna
with col1:
    st.page_link("Tabla_de_datos.py", label="Anterior", icon="⬅️")

# # Botón "Siguiente" en la segunda columna
with col2:
    st.page_link("Distribucion_de_la_esperanza_de_vida.py", label="Siguiente", icon="➡️")
