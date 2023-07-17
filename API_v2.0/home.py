# import streamlit as st
# import time
# from streamlit_option_menu import option_menu
# from streamlit_extras.switch_page_button import switch_page
# import pandas as pd
# from PIL import Image


# #Logo de la empresa
# def inicio():
#     st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         nombre = st.text_input("Nombre").capitalize()
#     with col2:
#         apellido = st.text_input("Apellido").capitalize()
#     with col3:
#         edad = st.text_input("Edad")
#     with col4:
#         email = st.text_input("Correo Electronico")
#     if nombre == "" or apellido == "" or edad == "" or email == "":
#         st.text("Todos los campos son obligatorios")
#     else:
#         st.header(f"Hola {nombre} {apellido} 👋 . Bienvenido a la pagina de la consultora KEGV INC, aqui encontraras informacion valiosa para saber todo sobre sismos, su historia, daños, graficos y mas.")
#         st.header("Por favor selecciona una de las opciones mas abajo descritas")
#         password = "123456"
#         seleccion = st.selectbox("¿Quien eres?", ("", "Empresa", "Usuario")  )
        
        
#         if seleccion == "":
#             pass
#         elif seleccion == "Usuario":
#             with st.spinner(f"Redirigiendo a {seleccion}..."):
#                 time.sleep(3)
#                 switch_page("usuario")
#         elif  seleccion == "Empresa":
#             empresa = st.text_input("Por favor digita la contraseña", type="password")
#             if empresa == "":
#                 pass
#             elif empresa == password:
#                     with st.spinner(f"Redirigiendo a {seleccion}..."):
#                         time.sleep(3)
#                         switch_page("empresa")
#             else:
#                 st.info("Contraseña incorrecta")
        
#     return nombre, apellido

# inicio()
                
            








    







# # if seleccion == "":
# #     pass
# # elif seleccion == "Empresa":
# #     with st.spinner("Espere"):
# #         time.sleep(3)
# #     if empresa == password:
# #         switch_page("prueba")
# #     else:
# #         st.info("Contraseña Errada")
