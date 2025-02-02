import streamlit as st

pg = st.navigation([st.Page("Introduccion.py"), st.Page("Tabla_de_datos.py"),
                    st.Page("Resumen_estadistico.py"), st.Page("Distribucion_de_la_esperanza_de_vida.py"),
                    st.Page("Evolucion_de_la_esperanza_de_vida.py")
                    ])
pg.run()

