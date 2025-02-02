"""
compara la distribución de la esperanza de vida entre géneros o membresía a la OCDE .
Utiliza gráficas de caja y bigotes paralelas. Deja al usuario la posibilidad de seleccionar
qué desea comparar. Al igual que la página anterior, permite al usuario la posibilidad de 
seleccionar el año sobre el que se construirán las gráficas con radiobotones.
"""
import streamlit as st
import pandas as pd
import altair as alt


# función para mostrar un boxplot
def showBoxPlot(df): #stats1: año de interés; stats2: año anterior; year: año actual
    box_plot = alt.Chart(df).mark_boxplot().encode(
        y=alt.Y(f'Life_exp:Q', title=f'Esperanza de vida', scale=alt.Scale(zero=False))  # Eje Y numérico para el índice
    )
    st.altair_chart(box_plot, use_container_width=True) # dibujamos el gráfico

# función para mostrar dos boxplot
def showTwoBox(df1, df2, title1, title2):
    # rango mínimo y máximo de los datos
    min_value = min(df1['Life_exp'].min(), df2['Life_exp'].min())
    max_value = max(df1['Life_exp'].max(), df2['Life_exp'].max())
    
    # primer boxplot
    boxplot_1 = alt.Chart(df1).mark_boxplot().encode(
        y=alt.Y('Life_exp:Q', title='Esperanza de vida', scale=alt.Scale(domain=[min_value, max_value], zero=False)),
        color=alt.value('blue')  
    ).properties(
        width=300,  
        height=400,
        title=title1
    )
    
    # segundo boxplot
    boxplot_2 = alt.Chart(df2).mark_boxplot().encode(
        y=alt.Y('Life_exp:Q', title='Esperanza de vida', scale=alt.Scale(domain=[min_value, max_value], zero=False)),
        color=alt.value('red') 
    ).properties(
        width=300,  
        height=400,
        title=title2
    )
    
    # acomodar boxplots horizontalmente
    combined_chart = alt.hconcat(boxplot_1, boxplot_2)
    
    # mostrar el gráfico
    st.altair_chart(combined_chart, use_container_width=True)


# dataframe base
df = pd.read_csv("./Life_exp_OECD.csv", sep=",")

st.title("Distribución de la Esperanza de Vida")

## parámetros de filtrado, se contruyen las tres variables a usar: year, filter_oecd y filter_gender
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

st.write("Considere que para el año 2023 existen registros para menos países que los años previos.")
st.write(' ')
st.write(' ')


## datos filtrados por año
df_year = df[df['Year'] == year] # aseguramos que los registros no se repitan y solo se tome el año de interés


# grids si el usuario no selecciona ningún desagrupamiento
if not filter_oecd and not filter_gender:
    df_total = df_year[df_year['Gender'] == 'Total']
    st.write("##### Gráfico de cajas y bigotes para todos los países de la lista")
    showBoxPlot(df_total)

#grids si el usuario desagrupa por pertenencia a la OECD
elif filter_oecd and not filter_gender:
    df_total_OECD = df_year[(df_year['Gender'] == 'Total') & (df_year['OECD'] == True)]
    df_total_no_OECD = df_year[(df_year['Gender'] == 'Total') & (df_year['OECD'] == False)]
    showTwoBox(df_total_OECD, df_total_no_OECD, 'Países miembros de la OECD', 'Países restantes')

# grids si el usuario desagrupa solo por género
elif not filter_oecd and filter_gender:
    df_male = df_year[df_year['Gender'] == 'Male']
    df_female = df_year[df_year['Gender'] == 'Female']
    showTwoBox(df_male, df_female, 'Hombres de todos los países', 'Mujeres de todos los países')

elif filter_oecd and filter_gender:
    st.write(" ")
    st.markdown("<h3><center>Hombres</center></h3>", unsafe_allow_html=True)
    df_male_OECD = df_year[(df_year['Gender'] == 'Male') & (df_year['OECD'] == True)]
    df_male_no_OECD = df_year[(df_year['Gender'] == 'Male') & (df_year['OECD'] == False)]
    showTwoBox(df_male_OECD, df_male_no_OECD, 'Países miembros de la OECD', 'Países restantes')

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("<h3><center>Mujeres</center></h3>", unsafe_allow_html=True)
    df_fem_OECD = df_year[(df_year['Gender'] == 'Female') & (df_year['OECD'] == True)]
    df_fem_no_OECD = df_year[(df_year['Gender'] == 'Female') & (df_year['OECD'] == False)]
    showTwoBox(df_fem_OECD, df_fem_no_OECD, 'Países miembros de la OECD', 'Países restantes')

    # Acomodo de los botones de forma horizontal
col1, col_space, col2 = st.columns([1, 6, 1])  # Dos columnas de igual ancho

# Botón "Anterior" en la primera columna
with col1:
    st.page_link("Resumen_estadistico.py", label="Anterior", icon="⬅️")

# # Botón "Siguiente" en la segunda columna
with col2:
    st.page_link("Evolucion_de_la_esperanza_de_vida.py", label="Siguiente", icon="➡️")
