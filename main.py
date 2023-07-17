# Importar las bibliotecas necesarias
import uvicorn
import os
import streamlit as st
from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
#import db_dtypes
from PIL import Image
import time
import streamlit_extras
#from streamlit_extras.switch_page_button import switch_page
#from streamlit_extras.metric_cards import style_metric_cards
from streamlit_option_menu import option_menu
from streamlit import *
#import plost
#import plotly.express as px
#import seaborn as sns
import pydeck as pdk
#import numpy as np
##### Librerias Francisco - Modelo
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from ETLEnvironment_class import ETLEnvironment
import pandas as pd
import googlemaps
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
import math
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\miche\OneDrive\Escritorio\KNN\prueba_bigquery\project-sismos-1a1e2a643257.json"

st.set_page_config("INICIO", layout="wide", initial_sidebar_state="expanded")

# Crear una función para ejecutar las consultas en BigQuery y obtener un DataFrame
def run_query(query):
    # client = bigquery.Client()
    # query_job = client.query(query)
    # results = query_job.result().to_dataframe()
    # return results
    path_root = ETLEnvironment().root_project_path
    json_credentials = "project-sismos-2a770c4ff889.json"
    first_scope = "https://www.googleapis.com/auth/cloud-platform"
    credentials = service_account.Credentials.from_service_account_file(path_root + json_credentials, scopes=[first_scope],)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    return results

# Crear la aplicación Streamlit
def main():
    st.header("Bienvenido al consultor de KEGV INC")
    st.write("Este consultor tiene por finalidad ayudar a las personas a entender un poco mejor la informacion sobre los sismos")
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        pais = st.selectbox("Selecciona el pais a consultar", options=["","CHILE", "JAPON", "USA"])
        anio = ""
    with col1:
        if pais == "CHILE":
            anio = st.selectbox("Selecciona el año a consultar", options=["",2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023],index=0)
            with col2:
                imagen = Image.open(r"C:\Users\miche\OneDrive\Escritorio\KNN\prueba_bigquery\bandera chile.jpg")
                st.image(imagen, "Bandera de Chile", width=560)
                if anio != "":
                    with col1:
                        with st.spinner(f"Recolectando informacion de {pais} para el año {anio}..."):
                            time.sleep(3)
        elif pais == "JAPON":
            anio = st.selectbox("Selecciona el año a consultar", options=["",2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023],index=0)
            with col2:
                imagen = Image.open(r"C:\Users\miche\OneDrive\Escritorio\KNN\prueba_bigquery\bandera japon.jpg")
                st.image(imagen, "Bandera de Japon", width=560)
                if anio != "":
                    with col1:
                        with st.spinner(f"Recolectando informacion de {pais} para el año {anio}..."):
                            time.sleep(3)
        elif pais == "USA":
            anio = st.selectbox("Selecciona el año a consultar", options=["",2018,2019,2020,2021,2022,2023], index=0)
            with col2:
                imagen = Image.open(r"C:\Users\miche\OneDrive\Escritorio\KNN\prueba_bigquery\bandera usa.jpg")
                st.image(imagen, "Bandera de Estados Unidos", width=560)
                if anio != "":
                    with col1:
                        with st.spinner(f"Recolectando informacion de {pais} para el año {anio}..."):
                            time.sleep(3)

    #Activadores
    mostrar_button = False
    mostrar_graficos = False
    mostrar_metricas = False
    #Cambiamos el nombre
    if pais == "CHILE":
        pais = "CL"
    elif pais == "JAPON":
        pais = "JP"
    elif pais == "USA":
        pais = "US"

    # Definir una consulta de ejemplo
    if pais == "":
        pass
    elif pais =="" or anio == "":
        pass
    elif pais != "" and anio != "":
        global df
        query = f"SELECT * FROM `sismos_db.sismos` WHERE ID_Pais = '{pais}' and extract(year from Fecha_del_sismo) = {anio} ;"
        df = run_query(query)
        mostrar_button = True
        #Dataframe
        if df.empty:
            pass
        elif not df.empty:
            st.write("A continuacion podras observar una tabla donde esta toda la informacion y caracteristicas de los sismos. Desde su fecha de ocurrencia hasta el pais donde ocurrio.")
            st.write("Esta es toda la informacion que pudimos encontrar en nuestros registros.")
            st.write(f"Contamos con `{len(df)}` registros para el año `{anio}`")
            st.dataframe(df, width=1000)
            st.write("Informacion Importante: ")
            st.write("1. Mmmm :thinking_face: viendo estos datos, sabemos que tal vez no entiendas que pueden significar")
            st.write("2. A veces nosotros tampoco pero shhh :zipper_mouth_face:")
            st.write("3. Abajo hay un boton ... Presionalo y dale vida a los datos. Te ayudara a entender mejor")
    
            #Indices para obtener solo los registros que tengan el pais y año correspondiente.
            lista_indices = []
            for indice, elemento in enumerate(df["Fecha_del_sismo"]):
                if df["ID_Pais"][indice]== pais and df["Fecha_del_sismo"][indice].year == anio:
                    lista_indices.append(indice)

            #Lugares para obtener de Estados Unidos
            lugares_us = []
            for indice, elemento in enumerate(df.loc[lista_indices, "Lugar_del_Epicentro"]):
                inicio_usa = str(df["Lugar_del_Epicentro"][indice]).find(",")+1 
                fin_usa = len(df["Lugar_del_Epicentro"][indice])+10
                lugar_usa = str(df["Lugar_del_Epicentro"][indice])[inicio_usa:fin_usa]
                lugares_us.append(lugar_usa)

            #Lugares para obtener de Chile
            lugares_Ch = []
            for indice in lista_indices:
                inicio_CL = str(df["Lugar_del_Epicentro"][indice]).find("de")+2 
                fin_CL = len(str(df["Lugar_del_Epicentro"][indice]))
                lugar_CL = str(df["Lugar_del_Epicentro"][indice])[inicio_CL:fin_CL]
                lugares_Ch.append(lugar_CL)


        #Transformamos a Dataframe y contamos los valores para graficar.
        lugares_cl = pd.DataFrame(lugares_Ch, columns=["Lugar"])
        lugares_usa = pd.DataFrame(lugares_us, columns=["Lugar"])

        #Contamos los valores
        lugares_cl["Lugar"].value_counts()
        lugares_usa["Lugar"].value_counts()


        mg_min = df.loc[lista_indices, "Magnitud"].min()
        mg_max = df.loc[lista_indices, "Magnitud"].max()
        q_sismos = len(df.loc[lista_indices, "Magnitud"])
        lugares_unicos = df.loc[lista_indices, "Lugar_del_Epicentro"]
        lugar_mas_sismos = lugares_unicos.value_counts()[0:5].sort_values(ascending=True)
        mostrar_metricas = True

        col10,col20 = st.columns([0.58, 0.42])
        with col10:
            if mostrar_metricas == True:
                button = st.button("DALE VIDA A LOS DATOS :sunglasses:")
                if button:
                    with st.spinner("Extrayendo..."):
                        time.sleep(2)
                    with st.spinner("Transformando..."):
                        time.sleep(2)
                    with st.spinner("Cargando..."):
                        time.sleep(2)
                    with st.spinner("Dando vida a los Datos :sunglasses:..."):
                        time.sleep(2)
                    st.markdown("# Metricas")
                    st.write("En este apartado podras observar informacion reducida y relevante en cuanto a los sismos. Queremos que sea lo mas facil de interpretar y que puedas tener una vision general de los sismos, lugares mas sismologicos, magnitudes, entre otra informacion que consideramos `importante`. ")
                    st.write("En caso de tener dudas sobre alguna de nuestras metricas al lado de cada `titulo` podras encontrar un :grey_question: el cual contiene informacion de ayuda para entenderla mejor.")
                    

                    mostrar_graficos = True
                    if pais == "JP":
                        mostrar_graficos = True
                        col1, col2, col3 = st.columns(3)
                        col1.metric("`MAGNITUD MINIMA`", f"{mg_min} M", help=f"Esta metrica nos muestra la Magnitud minima de un sismos para el año {anio}")
                        col2.metric("`MAGNITUD MAXIMA`", f"{mg_max} M", help=f"Esta metrica nos muestra la Magnitud maxima de un sismo para el año {anio}", delta_color="off")
                        col3.metric("`SISMOS POR AÑO`", f"{q_sismos}", help=f"Esta metrica nos muestra la cantidad de sismos para el año {anio}")
                        col4, col5, col6= st.columns(3)
                        col4.metric("`LUGAR MAS SISMOLOGICO`", lugar_mas_sismos.index[4], help=f"Esta metrica nos muestra el lugar mas sismologico para el año {anio}")
                        col5.metric("`SISMOS EN EPICENTRO`", lugar_mas_sismos[4], help=f"Esta metrica nos muestra la cantidad de sismos que ocurrieron en {lugar_mas_sismos.index[4]} para el año {anio}")
                        col6.metric("`PORCENTAJE`",f"{lugar_mas_sismos[4]/q_sismos:.2%}", help=f"Esta metrica nos muestra el porcentaje que representa la cantidad de sismos ocurridos en {lugar_mas_sismos.index[4]} en comparacio con el total" )
                        style_metric_cards(background_color="gray", border_color="black", border_left_color="cyan")
                        st.markdown(" ### Graficos")
                        col7, col8 = st.columns(2)
                        with col7:
                            fig_bar = plt.figure(figsize=(3,3))
                            plt.barh(y=lugar_mas_sismos.index, width=lugar_mas_sismos.values)
                            plt.title(f"Top 5 Epicentros mas Sismicos en {pais}")
                            plt.xlabel("Frecuencia")
                            plt.ylabel("Lugares mas sismologicos")
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig_bar)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de barras horizontal el cual nos estan indicando el top 5 lugares o epicentros que fueron mas afectados en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por la cantidad de veces que los lugares presentaron un sismo.")
                            st.write(f"Donde el eje Y esta representado por los nombres de los lugares que mas presentaron sismos.")
                        col7, col8 = st.columns(2)
                        with col7:
                            enero = 0
                            febrero=0
                            marzo=0
                            abril =0
                            mayo =0
                            junio=0
                            julio=0
                            agosto=0
                            septiembre=0
                            octubre=0
                            noviembre=0
                            diciembre=0

                            for indice, elemento in enumerate(df["Fecha_del_sismo"]):
                                if df["Fecha_del_sismo"][indice].year == anio:
                                    if df["Fecha_del_sismo"][indice].month == 1:
                                        enero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 2:
                                        febrero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 3:
                                        marzo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 4:
                                        abril +=1
                                    elif df["Fecha_del_sismo"][indice].month == 5:
                                        mayo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 6:
                                        junio +=1
                                    elif df["Fecha_del_sismo"][indice].month == 7:
                                        julio +=1
                                    elif df["Fecha_del_sismo"][indice].month ==8:
                                        agosto +=1
                                    elif df["Fecha_del_sismo"][indice].month == 9:
                                        septiembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 10:
                                        octubre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 11:
                                        noviembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 12:
                                        diciembre +=1
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}
                                                        
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}                                
                            df_meses = pd.DataFrame(meses, index=range(1))
                            fig = plt.figure()
                            plt.plot(df_meses.columns, df_meses.values[0], marker="o", ls="--", markerfacecolor = "white", color="green")
                            plt.xticks(rotation=90)
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de lineas el cual nos esta mostrando la evolucion de los sismos a traves de los meses en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por los nombres de los meses del año.")
                            st.write(f"Donde el eje Y esta representado por la frecuencia o acumulacion de las veces que ocurrio un sismo en el mes.")

                        col7, col8 = st.columns([0.9,0.1])
                        with col7:
                            df_map = df[["Longitud", "Latitud"]]
                            df_map = df_map.rename(columns={"Longitud":"lon", "Latitud": "lat"})
                            st.markdown("# Mapa :sunglasses:")          
                            st.pydeck_chart(pdk.Deck(
                                #map_style="mapbox://styles/mapbox/streets-v11",
                                map_style=None,
                                initial_view_state=pdk.ViewState(
                                    latitude=36.204824,
                                    longitude=138.252924,
                                    zoom=7,
                                    pitch=50,
                                ),
                                layers=[
                                    pdk.Layer(
                                    'HexagonLayer',
                                    data=df_map,
                                    get_position='[lon, lat]',
                                    elevation_range=[0, 1000],
                                    pickable=True,
                                    extruded=True,
                                    get_radius=5,
                                    radius=-10
                                    ),
                                    pdk.Layer(
                                        'ScatterplotLayer',
                                        data=df_map,
                                        auto_highlight=True,
                                        elevation_range=[0, 1000],
                                        get_position='[lon, lat]',
                                        get_color='[255,255,0, 0]',
                                        get_radius=250,
                                        border_radius=100,
                                        border_color_radius="black"
                                    
                    ),
                ],
            ))


                    elif pais == "CL":
                        col1, col2, col3 = st.columns(3)
                        col1.metric("`MAGNITUD MINIMA`", f"{mg_min} M", help=f"Esta metrica nos muestra la Magnitud minima de un sismos para el año {anio}")
                        col2.metric("`MAGNITUD MAXIMA`", f"{mg_max} M", help=f"Esta metrica nos muestra la Magnitud maxima de un sismo para el año {anio}", delta_color="off")
                        col3.metric("`SISMOS POR AÑO`", f"{q_sismos}", help=f"Esta metrica nos muestra la cantidad de sismos para el año {anio}")
                        col4, col5, col6= st.columns(3)
                        col4.metric("`LUGAR MAS SISMOLOGICO`", lugar_mas_sismos.index[4], help=f"Esta metrica nos muestra el lugar mas sismologico para el año {anio}")
                        col5.metric("`SISMOS EN EPICENTRO`", lugar_mas_sismos[4], help=f"Esta metrica nos muestra la cantidad de sismos que ocurrieron en {lugar_mas_sismos.index[4]} para el año {anio}")
                        col6.metric("`PORCENTAJE`",f"{lugar_mas_sismos[4]/q_sismos:.2%}", help=f"Esta metrica nos muestra el porcentaje que representa la cantidad de sismos ocurridos en {lugar_mas_sismos.index[4]} en comparacio con el total" )
                        style_metric_cards(background_color="gray", border_color="black", border_left_color="cyan")

                        #Empezamos a graficar.
                        st.markdown("# Graficos")
                        col7, col8 = st.columns(2)
                        with col7:
                            fig_bar = plt.figure(figsize=(3,3))
                            plt.barh(y=lugar_mas_sismos.index, width=lugar_mas_sismos.values)
                            plt.title(f"Top 5 Epicentros mas Sismicos en {pais}")
                            plt.xlabel("Frecuencia")
                            plt.ylabel("Lugares mas sismologicos")
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig_bar)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de barras horizontal el cual nos estan indicando el top 5 lugares o epicentros que fueron mas afectados en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por la cantidad de veces que los lugares presentaron un sismo.")
                            st.write(f"Donde el eje Y esta representado por los nombres de los lugares que mas presentaron sismos.")
                        
                        col7, col8 = st.columns(2)
                        with col7:
                            enero = 0
                            febrero=0
                            marzo=0
                            abril =0
                            mayo =0
                            junio=0
                            julio=0
                            agosto=0
                            septiembre=0
                            octubre=0
                            noviembre=0
                            diciembre=0

                            for indice, elemento in enumerate(df["Fecha_del_sismo"]):
                                if df["Fecha_del_sismo"][indice].year == anio:
                                    if df["Fecha_del_sismo"][indice].month == 1:
                                        enero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 2:
                                        febrero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 3:
                                        marzo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 4:
                                        abril +=1
                                    elif df["Fecha_del_sismo"][indice].month == 5:
                                        mayo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 6:
                                        junio +=1
                                    elif df["Fecha_del_sismo"][indice].month == 7:
                                        julio +=1
                                    elif df["Fecha_del_sismo"][indice].month ==8:
                                        agosto +=1
                                    elif df["Fecha_del_sismo"][indice].month == 9:
                                        septiembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 10:
                                        octubre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 11:
                                        noviembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 12:
                                        diciembre +=1
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}
                                                        
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}                                
                            df_meses = pd.DataFrame(meses, index=range(1))
                            fig = plt.figure()
                            plt.plot(df_meses.columns, df_meses.values[0], marker="o", ls="--", markerfacecolor = "white", color="green")
                            plt.xticks(rotation=90)
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig)                    
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de lineas el cual nos esta mostrando la evolucion de los sismos a traves de los meses en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por los nombres de los meses del año.")
                            st.write(f"Donde el eje Y esta representado por la frecuencia o acumulacion de las veces que ocurrio un sismo en el mes.")

                        col7, col8 = st.columns(2)
                        with col7:
                            fig_bar = plt.figure(figsize=(3,3))
                            plt.bar(x=lugares_cl["Lugar"].value_counts().index[0:5], height=lugares_cl["Lugar"].value_counts().values[0:5])
                            plt.title(f"Top 5 Lugares mas Sismicos en {pais}")
                            plt.xlabel("Frecuencia")
                            plt.ylabel("Lugares mas sismologicos")
                            plt.xticks(rotation=90)
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig_bar)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de barras horizontal el cual nos estan indicando el top 5 lugares o epicentros que fueron mas afectados en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por la cantidad de veces que los lugares presentaron un sismo.")
                            st.write(f"Donde el eje Y esta representado por los nombres de los lugares que mas presentaron sismos.")

                        col7, col8 = st.columns([0.9,0.1])
                        with col7:
                            df_map = df[["Longitud", "Latitud"]]
                            df_map = df_map.rename(columns={"Longitud":"lon", "Latitud": "lat"})
                            st.markdown("# Mapa :sunglasses:")          
                            st.pydeck_chart(pdk.Deck(
                                #map_style="mapbox://styles/mapbox/streets-v11",
                                map_style=None,
                                initial_view_state=pdk.ViewState(
                                    latitude=-33.45694,
                                    longitude=-70.64827,
                                    zoom=8,
                                    pitch=50,
                                ),
                                layers=[
                                    pdk.Layer(
                                    'HexagonLayer',
                                    data=df_map,
                                    get_position='[lon, lat]',
                                    elevation_range=[0, 1000],
                                    pickable=True,
                                    extruded=True,
                                    get_radius=5,
                                    radius=-10
                                    ),
                                    pdk.Layer(
                                        'ScatterplotLayer',
                                        data=df_map,
                                        auto_highlight=True,
                                        elevation_range=[0, 1000],
                                        get_position='[lon, lat]',
                                        get_color='[255,255,255, 255]',
                                        get_radius=250
                                    
                    ),
                ],
            ))

                    elif pais == "US":
                        col1, col2, col3 = st.columns(3)
                        col1.metric("`MAGNITUD MINIMA`", f"{mg_min} M", help=f"Esta metrica nos muestra la Magnitud minima de un sismos para el año {anio}")
                        col2.metric("`MAGNITUD MAXIMA`", f"{mg_max} M", help=f"Esta metrica nos muestra la Magnitud maxima de un sismo para el año {anio}", delta_color="off")
                        col3.metric("`SISMOS POR AÑO`", f"{q_sismos}", help=f"Esta metrica nos muestra la cantidad de sismos para el año {anio}")
                        col4, col5, col6= st.columns(3)
                        col4.metric("`LUGAR MAS SISMOLOGICO`", lugar_mas_sismos.index[4], help=f"Esta metrica nos muestra el lugar mas sismologico para el año {anio}")
                        col5.metric("`SISMOS EN EPICENTRO`", lugar_mas_sismos[4], help=f"Esta metrica nos muestra la cantidad de sismos que ocurrieron en {lugar_mas_sismos.index[4]} para el año {anio}")
                        col6.metric("`PORCENTAJE`",f"{lugar_mas_sismos[4]/q_sismos:.2%}", help=f"Esta metrica nos muestra el porcentaje que representa la cantidad de sismos ocurridos en {lugar_mas_sismos.index[4]} en comparacio con el total" )
                        style_metric_cards(background_color="gray", border_color="black", border_left_color="cyan")
                        st.markdown("# Graficos")
                        col7, col8 = st.columns(2)
                        with col7:
                            fig_bar = plt.figure(figsize=(3,3))
                            plt.barh(y=lugar_mas_sismos.index, width=lugar_mas_sismos.values)
                            plt.title(f"Top 5 Epicentros mas Sismicos en {pais}")
                            plt.xlabel("Frecuencia")
                            plt.ylabel("Lugares mas sismologicos")
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig_bar)
                        with col7:
                            enero = 0
                            febrero=0
                            marzo=0
                            abril =0
                            mayo =0
                            junio=0
                            julio=0
                            agosto=0
                            septiembre=0
                            octubre=0
                            noviembre=0
                            diciembre=0

                            for indice, elemento in enumerate(df["Fecha_del_sismo"]):
                                if df["Fecha_del_sismo"][indice].year == anio:
                                    if df["Fecha_del_sismo"][indice].month == 1:
                                        enero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 2:
                                        febrero +=1
                                    elif df["Fecha_del_sismo"][indice].month == 3:
                                        marzo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 4:
                                        abril +=1
                                    elif df["Fecha_del_sismo"][indice].month == 5:
                                        mayo +=1
                                    elif df["Fecha_del_sismo"][indice].month == 6:
                                        junio +=1
                                    elif df["Fecha_del_sismo"][indice].month == 7:
                                        julio +=1
                                    elif df["Fecha_del_sismo"][indice].month ==8:
                                        agosto +=1
                                    elif df["Fecha_del_sismo"][indice].month == 9:
                                        septiembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 10:
                                        octubre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 11:
                                        noviembre +=1
                                    elif df["Fecha_del_sismo"][indice].month == 12:
                                        diciembre +=1
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}
                                                        
                            meses = {"Enero": enero, "Febrero": febrero, "Marzo":marzo, "Abril":abril, "Mayo":mayo, "Junio":junio, "Julio":julio, "Agosto":agosto, "Septiembre":septiembre, "Octubre":octubre, "Noviembre":noviembre, "Diciembre":diciembre}                                
                            df_meses = pd.DataFrame(meses, index=range(1))
                            fig = plt.figure()
                            plt.plot(df_meses.columns, df_meses.values[0], marker="o", ls="--", markerfacecolor = "white", color="green")
                            plt.xticks(rotation=90)
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de lineas el cual nos esta mostrando la evolucion de los sismos a traves de los meses en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por los nombres de los meses del año.")
                            st.write(f"Donde el eje Y esta representado por la frecuencia o acumulacion de las veces que ocurrio un sismo en el mes.")

                        col7, col8 = st.columns(2)
                        with col7:
                            fig_bar = plt.figure(figsize=(3,3))
                            plt.bar(x=lugares_usa["Lugar"].value_counts().index[0:5], height=lugares_usa["Lugar"].value_counts().values[0:5])
                            plt.title(f"Top 5 Ciudades mas Sismicos en {pais}")
                            plt.xlabel("Frecuencia")
                            plt.ylabel("Lugares mas sismologicos")
                            plt.xticks(rotation=90)
                            plt.grid(visible=True, ls = "--", alpha=0.5)
                            st.pyplot(fig_bar)
                        with col8:
                            st.markdown("# Interpretacion:")
                            st.write(f"Al lado izquierdo encontramos un grafico de barras horizontal el cual nos estan indicando el top 5 lugares o epicentros que fueron mas afectados en {pais} para el año {anio}")
                            st.write(f"Donde el eje X esta representado por la cantidad de veces que los lugares presentaron un sismo.")
                            st.write(f"Donde el eje Y esta representado por los nombres de los lugares que mas presentaron sismos.")
                        
                        col7, col8 = st.columns([0.9,0.1])
                        with col7:
                            df_map = df[["Longitud", "Latitud"]]
                            df_map = df_map.rename(columns={"Longitud":"lon", "Latitud": "lat"})
                            st.markdown("# Mapa :sunglasses:")          
                            st.pydeck_chart(pdk.Deck(
                                #map_style="mapbox://styles/mapbox/streets-v11",
                                map_style=None,
                                initial_view_state=pdk.ViewState(
                                    latitude=37.09024,
                                    longitude=-95.712891,
                                    zoom=7,
                                    pitch=50,
                                ),
                                layers=[
                                    pdk.Layer(
                                    'HexagonLayer',
                                    data=df_map,
                                    get_position='[lon, lat]',
                                    elevation_range=[0, 1000],
                                    pickable=True,
                                    extruded=True,
                                    get_radius=5,
                                    radius=-10
                                    ),
                                    pdk.Layer(
                                        'ScatterplotLayer',
                                        data=df_map,
                                        auto_highlight=True,
                                        elevation_range=[0, 1000],
                                        get_position='[lon, lat]',
                                        get_color='[255,255,255, 255]',
                                        get_radius=250
                    ),
                ],
            ))




selected = option_menu(
            menu_title=None,
            options=["Inicio", "Nosotros", "Historia", "Comunidad", "Proceso", "Modelos", "Contacto" ],
            icons=["house", "book" ,"list-task","list-task","list-task","list-task","envelope"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
    styles={
        "container": {"padding": "0!important"}
    }
)

if selected == "Inicio":
    st.header("Bienvenido a la pagina principal de KEGV INC")
if selected == "Nosotros":
    st.title("`Nosotros`")
    st.subheader("Somos una consultora con 3 años de experiencia en el mundo de los datos. Somos data-driven, todas nuestras acciones estan basadas y fundamentadas en datos")

    st.subheader("Contamos con un equipo multidisciplinario, donde cada uno posee grandes habilidades tecnicas y personales")

    st.title("`Mision`")
    st.subheader("Nuestra mision es ayudar a las organizaciones a aprovechar al máximo el poder de sus datos. Nos comprometemos a brindar soluciones innovadoras y estratégicas que impulsen la toma de decisiones basada en datos, fomenten la eficiencia operativa y generen un impacto positivo en el rendimiento y el crecimiento de nuestros clientes.")

    st.title("`Vision`")
    st.subheader("La visión como consultora de datos es convertirnos en líderes reconocidos a nivel mundial en el campo de la ciencia de datos y análisis de datos. Nos esforzamos por ser la consultora de referencia para las organizaciones que buscan maximizar el valor de sus datos y utilizarlos como un activo estratégico para la toma de decisiones.",)

    st.title("`Nuestro Equipo`")
    col1, col2, col3, col4 = st.columns(4)
    with col1:  
        st.subheader("`Data Analyst`: Macarena Gonzalez")
    with col2:
        st.subheader("`Data Scientist`: Francisco Krapovickas")
    with col3:
        st.subheader("`Data Engineer`: Fernando Embrioni")
    with col4:
        st.subheader("`Data Engineer`: Michel Villot")

if selected == "Historia":
    container = st.container()
    imagen = Image.open(r"C:\Users\miche\OneDrive\Escritorio\Streamlit\sismo.jpg")
    col1, col2= st.columns(2)
    with col1:
        st.subheader("`¿Que es un sismo?`")
        st.subheader("Un terremoto​, también llamado sismo, seísmo, ​ temblor de tierra o movimiento telúrico, es la sacudida brusca y pasajera de la corteza terrestre. Los más comunes se producen por actividad de fallas geológicas.")
        st.subheader("`Causas`")
        st.subheader("Aunque la interacción entre Placas Tectónicas es la principal causa de los sismos no es la única. Cualquier proceso que pueda lograr grandes concentraciones de energía en las rocas puede generar sismos cuyo tamaño dependerá, entre otros factores, de qué tan grande sea la zona de concentración del esfuerzo.")
        st.subheader("Las causas más generales se pueden enumeran según su orden de importancia en:")
    with col2:
        st.image(imagen, "Imagen referencial de un Sismo", width=700)


    st.subheader("`Tectónica`: son los sismos que se originan por el desplazamiento de las placas tectónicas que conforman la corteza, afectan grandes extensiones y es la causa que más genera sismos.")
    st.subheader("`Volcánica`: es poco frecuente; cuando la erupción es violenta genera grandes sacudidas que afectan sobre todo a los lugares cercanos, pero a pesar de ello su campo de acción es reducido en comparación con los de origen tectónico.")
    st.subheader("`Hundimiento`: cuando al interior de la corteza se ha producido la acción erosiva de las aguas subterráneas, va dejando un vacío, el cual termina por ceder ante el peso de la parte superior. Es esta caída que genera vibraciones conocidas como sismos. Su ocurrencia es poco frecuente y de poca extensión.")
    st.subheader("`Deslizamientos`: el propio peso de las montañas es una fuerza enorme que tiende a aplanarlas y que puede producir sismos al ocasionar deslizamientos a lo largo de fallas, pero generalmente no son de gran magnitud.")
    st.subheader("`Explosiones Atómicas`: realizadas por el ser humano y que al parecer tienen una relación con los movimientos sísmicos.")

apikey = os.environ.get('apikey')
                            
def main_1(latitud, longitud, distancia_km):
    # Título de la aplicación

    def get_google_cloud_client():
        '''
        Esta función devuelve un cliente de Google Cloud listo para ser utilizado en el proyecto sismos
        '''

        # Preparo el path y scope para recuperar las credenciales
        path_root = ETLEnvironment().root_project_path
        json_credentials = "project-sismos-2a770c4ff889.json"
        first_scope = "https://www.googleapis.com/auth/cloud-platform"
        credentials = service_account.Credentials.from_service_account_file(path_root + json_credentials, scopes=[first_scope],)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)

        return client

    client = get_google_cloud_client()

    st.title('Resultados')

    lista = []

    # Ejecutar la consulta en BigQuery
    query = f'''
        SELECT * FROM `sismos_db.sismos`
        WHERE ST_DWITHIN(ST_GeogPoint(Longitud, Latitud), ST_GeogPoint({longitud}, {latitud}), {distancia_km} * 1000)
    '''
    job = client.query(query)
    # Mostrar los resultados en Streamlit
    for row in job.result():
        lista.append(row)

    fechas = []
    horas = []
    latitudes = []
    longitudes = []
    profundidades = []
    magnitudes = []
    tipo_magnitudes = []
    epicentros = []
    id_paises = []
    for fila in lista:
        fechas.append(fila[0])
        horas.append(fila[1])
        latitudes.append(fila[2])
        longitudes.append(fila[3])
        profundidades.append(fila[4])
        magnitudes.append(fila[5])
        tipo_magnitudes.append(fila[6])
        epicentros.append(fila[7])
        id_paises.append(fila[8])

    data = {
        'Fecha_del_sismo': fechas,
        'Hora_del_sismo': horas,
        'Latitud': latitudes,
        'Longitud': longitudes,
        'Profundidad_Km': profundidades,
        'Magnitud': magnitudes,
        'Tipo_Magnitud': tipo_magnitudes,
        'Lugar_del_Epicentro': epicentros,
        'ID_Pais': id_paises
    }

    df = pd.DataFrame(data)

    ProfundidadPromedio = df["Profundidad_Km"].mean()
    ProfundidadPromedio = round(ProfundidadPromedio, 2)
    ProfundidadMaxima = df["Profundidad_Km"].max()
    ProfundidadMinima = df["Profundidad_Km"].min()
    MagnitudPromedio = df["Magnitud"].mean()
    MagnitudPromedio = round(MagnitudPromedio, 2)
    MagnitudMaxima = df["Magnitud"].max()
    MagnitudMinima = df["Magnitud"].min()
    Cantidad = len(df)
    
    df["Magnitud"] = df["Magnitud"].astype(float)
    countm55 = df[df["Magnitud"] > 5]["Magnitud"].count()
    countm65 = df[df["Magnitud"] > 6.5]["Magnitud"].count()
    count = len(df)
    probm55 = (countm55 / count).round(8)
    probm65 = (countm65 / count).round(8)


    if len(df) == 0:
        st.write("No contamos con registros de sismos en tu área, recuerda que esta API sólo es funcional en Chile, Japón y EEUU.")
    else:
        df['Fecha_del_sismo'] = pd.to_datetime(df['Fecha_del_sismo'])

        # Calcular la cantidad de sismos por día
        sismos_por_dia = df.groupby(df['Fecha_del_sismo'].dt.date).size().reset_index(name='Cantidad de Sismos')

        if len(sismos_por_dia) <= 1:
           st.write("El área es demasiado chica, no hay suficientes datos para ajustar el modelo.")
        else:
            fecha_actual = datetime.now().date()

            sismos_por_dia = sismos_por_dia[sismos_por_dia['Fecha_del_sismo']>fecha_actual-timedelta(days=365)]
            
            model = ARIMA(sismos_por_dia['Cantidad de Sismos'], order=(3, 0, 0))
            model_fit = model.fit()


            # Obtener los últimos tres meses previos a la fecha actual
            fecha_tres_meses_atras = fecha_actual - timedelta(days=90)
            ultimos_tres_meses = sismos_por_dia[(sismos_por_dia['Fecha_del_sismo'] >= fecha_tres_meses_atras)]

            # Generar las fechas para la predicción de los próximos tres meses desde la fecha actual
            fecha_tres_meses_adelante = fecha_actual + timedelta(days=90)
            fechas_prediccion = pd.date_range(start=fecha_actual, end=fecha_tres_meses_adelante, freq='D')
            prediccion = model_fit.predict(start=len(ultimos_tres_meses), end=len(ultimos_tres_meses) + len(fechas_prediccion) - 1)

            # Crear una lista con las fechas de los últimos tres meses y las fechas de predicción
            fechas = list(ultimos_tres_meses['Fecha_del_sismo']) + list(fechas_prediccion)

            # Crear una lista con la cantidad de sismos de los últimos tres meses y las predicciones
            cantidad_sismos = list(ultimos_tres_meses['Cantidad de Sismos']) + list(prediccion)

            # Crear el DataFrame con los datos de los últimos tres meses y las predicciones
            datos_grafico = pd.DataFrame({'Fecha': fechas, 'Cantidad de Sismos': cantidad_sismos})

            # Configurar la aplicación de Streamlit
            st.write('Gráfico de actividad sísmica de los últimos 3 meses y predicción de actividad para los próximos 3 meses:')
            st.line_chart(datos_grafico.set_index('Fecha'))
            
            sismos_predichos = datos_grafico.iloc[-len(fechas_prediccion):]['Cantidad de Sismos'].sum().astype(int)
            prob1 = (probm55*sismos_predichos).round(5)
            prob2 = (probm65*sismos_predichos).round(5)
            st.write(f'Según nuestros pronósticos, en tu área se registrarán una cantidad de {sismos_predichos} sismos en los próximos 3 meses, y la probabilidad de que ocurra un sismo dañino es de:')
            col1,col2 = st.columns(2)
            with col1:
                st.markdown(f'**Moderadamente dañino(Mg5 o superior):**')
                st.markdown(f'<p style="font-size:34px">{prob1}%</p>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'**Muy dañino(Mg6.5 o superior):**')
                st.markdown(f'<p style="font-size:34px">{prob2}%</p>', unsafe_allow_html=True)
            st.markdown("<h2 style='font-size:13px;'>(Esta estimación se hace en base al registro histórico de sismos ocurridos en el área desde el año 2000 a la actualidad, se tiene en cuenta la cantidad de sismos de magnitud superior a la dicha ocurrieron en el lugar y no cerciora eventos futuros)</h2>", unsafe_allow_html=True)
            st.write("")


            st.write("El siguiente mapa muestra los sismos de magnitud mayor a 5 registrados en tu área desde el año 2000:")
            zoom_adjustment = 3.4  # Ajuste personalizado (puedes experimentar con diferentes valores)
            zoom_start = int(15 - zoom_adjustment * math.log10(distancia_km))

            # Crear un mapa centrado en una ubicación específica
            mapa = folium.Map(location=[latitud, longitud], zoom_start=zoom_start)

            # Obtener los puntos que cumplen la condición
            puntos = df[df["Magnitud"] > 5]

            # Agregar marcadores al mapa
            for _, punto in puntos.iterrows():
                folium.Marker(location=[punto['Latitud'], punto['Longitud']]).add_to(mapa)

            folium.Circle(
                location=[latitud, longitud],
                radius=distancia_km * 1000,  # Convertir el radio a metros
                color='blue',
                fill=False,
            ).add_to(mapa)

            st.write("Mapa de sismos")
            folium_static(mapa)

            st.write("Los valores promedio, mínimo y máximo de profundidad y magnitud de los sismos en tu área son los siguientes:")

            data = {
                'Profundidad': [ProfundidadPromedio, ProfundidadMinima, ProfundidadMaxima],
                'Magnitud': [MagnitudPromedio, MagnitudMinima, MagnitudMaxima]
            }
            df2 = pd.DataFrame(data, index=['Promedio', 'Mínimo', 'Máximo'])
            st.table(df2)

            st.write(f'Contamos con registros de un total de {Cantidad} sismos en tu área:')

            return st.dataframe(df)


def opcion1():
    # Agregar contenido a la aplicación

    st.write('Ingresa latitud, longitud y radio del área de la que quieres conocer la actividad sismica.')


    col1, col2, col3 = st.columns(3)

    with col1:
        latitud = st.text_input('Latitud')
    with col2:
        longitud = st.text_input('Longitud')
    with col3:
        distancia_km = st.text_input('Radio del área (km)')
    
    if st.button('Ejecutar consulta'):
        # Llamar a la función para ejecutar la consulta 
        try:
            latitud = float(latitud)
            longitud = float(longitud)
            distancia_km = float(distancia_km)
            main_1(latitud, longitud, distancia_km)
        except (ValueError, UnboundLocalError):
            st.write("Los parámetros ingresados son incorrectos o el área es demasiado chica.")


def opcion2():
    gmaps = googlemaps.Client(key=apikey)

    st.write('Ingresa el nombre del lugar, seguido del país(Chile, Japón o EEUU) y radio del área de la que quieres conocer la actividad sismica.')

    col1, col2 = st.columns(2)

    with col1:
        lugar = st.text_input("Nombre del lugar:")
    with col2:
        distancia_km = st.text_input('Radio del área (km)')
    if lugar:
        # Realizar la solicitud de geocodificación inversa
        resultados = gmaps.geocode(lugar)

        if resultados:
            # Obtener las coordenadas del primer resultado
            coordenadas = resultados[0]['geometry']['location']
            latitud = coordenadas['lat']
            longitud = coordenadas['lng']

            st.write(f"Las coordenadas del lugar '{lugar}' son:")
            st.write(f"Latitud: {latitud}")
            st.write(f"Longitud: {longitud}")
    else:
        st.write("No se encontraron resultados para el lugar ingresado.")

    if st.button('Ejecutar consulta'):
        # Llamar a la función para ejecutar la consulta 
        try:
            latitud = float(latitud)
            longitud = float(longitud)
            distancia_km = float(distancia_km)
            main(latitud, longitud, distancia_km)
        except (ValueError, UnboundLocalError):
            st.write("Los parámetros ingresados son incorrectos o el área es demasiado chica.")

def main2():
    st.write("Seleccione en el menú de la izquierda la opción que desea utilizar")

    # Opciones del menú
    opciones = ["", "Con Coordenadas", "Con Google Maps"]
    seleccion = st.selectbox("Selecciona un método para obtener los datos", opciones)

    # Lógica de las opciones seleccionadas
    if seleccion == "Con Coordenadas":
        opcion1()
    elif seleccion == "Con Google Maps":
        opcion2()

if selected == "Comunidad":
    main()
if selected =="Modelos":
    main2()

main()

