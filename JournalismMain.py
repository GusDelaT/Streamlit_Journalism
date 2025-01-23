import streamlit as st
import pandas as pd
import os

if 'page' not in st.session_state:
    st.session_state.page = 'form'  

def go_to_image_page():
    st.session_state.page = 'image'  

def go_to_form_page():
    st.session_state.page = 'form'  


if st.session_state.page == 'form':
    st.title("Formulario de Redacción para definir calidad de las noticias")

name = st.text_input("Agrega tu nombre en el siguiente espacio:")
job_title = st.text_input("Agrega tu puesto laboral en el siguiente espacio:")

csv_file = 'user_data.xlsx'
if st.button("Adelante"):
    if name and job_title:
        new_data = pd.DataFrame([[name, job_title]], columns=["Nombre", "Puesto de Trabajo"])
        
        if os.path.exists(csv_file):
            existing_data = pd.read_csv(csv_file)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data
        
        updated_data.to_csv(csv_file, index=False, mode='a', header=not os.path.exists(csv_file))

        st.success(f"Datos guardados correctamente!")
        go_to_image_page()

elif st.session_state.page == 'image':
    st.title("Welcome to the Image Page!")
    st.image("01.jpg", caption="Your Uploaded Image", use_container_width=True)
    
    if st.button("Go Back"):
        go_to_form_page()
