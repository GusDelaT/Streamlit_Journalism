import streamlit as st

st.title("Formulario de Redacción para definir calidad de las noticias")

name = st.text_input("Agrega tu nombre en el siguiente espacio:")
job_title = st.text_input("Agrega tu puesto laboral en el siguiente espacio:")

if st.button("Adelante"):
    if name and job_title:
        st.success(f"Hola {name}, tu puesto es {job_title}.")
    else:
        st.warning("Por favor agrega tus datos para poder continuar")

git add JournalismMain.py
git commit -m "Updated file"
git push origin <main>