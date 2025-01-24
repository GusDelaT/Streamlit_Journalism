import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import BytesIO
import PyPDF2

st.set_page_config(
    page_title="Formulario de Redacción",
    layout="wide"
)

# ---  Fetch Data para el drive en mi cuenta personal ---
def fetch_data(sheet_url: str):
    try:
        return pd.read_csv(sheet_url)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRSKqRqiv_7LHJsO3rvH8Cng9Nvr1hKmT143s3i9LUCTrZv0mCxU-3mDiS9bO4jhe3XbT-n9mgU78k_/pub?gid=0&single=true&output=csv"

# Fetch
df = fetch_data(sheet_url)

# --- De Data a CSV en la parte principal ---
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

# --- Layout ---
st.title("Formulario de Redacción")
st.caption("Recordá incluir tu nombre y puesto laboral previo a dar al botón de finalizar.")
st.text_input("Nombre")
st.text_input("Puesto Laboral")

# --- Filtros de sidebar ---
st.sidebar.header("Filtrar opciones")

# Chequeo de exito de subida
if not df.empty:
    # Visualizacion
    selected_column = st.sidebar.selectbox(
        "Selecciona un periódico",
        options=df.columns
    )

    # Seleccion multiple de variables
    if 'Name' in df.columns:
        excluded_names = st.sidebar.multiselect(
            "Filtrar periódicos",
            options=df['Name'].unique(),
            default=[]
        )
        filtered_df = df[~df['Name'].isin(excluded_names)]
    else:
        filtered_df = df

    # Sliders que puede que tenga que borrar
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        min_val, max_val = df[col].min(), df[col].max()
        selected_range = st.sidebar.slider(f"Seleccionar {col}", min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[0])]

    # --- Ambas paginas de navegacion cabal ---
    tab1, tab2 = st.tabs(["Overview", "Filtrados"])

    # Tab 1: Overview  
    with tab1:
        st.header("Overview")
        edited_df = st.data_editor(df, 
            num_rows="dynamic",  # Allow adding new rows
            column_config={
                "Name": st.column_config.Column(pinned=True),
        }
    )
    
    # Boton para guardar en el Drive
        if st.button("Finalizar"):
            edited_df.to_csv("updated_data.csv", index=False)
            upload_to_drive("updated_data.csv", drive_file_id)
            st.success("Cambios guardados y subidos a Google Drive exitosamente.")

    # Tab 2: Datos Filtrados para cosas mias
    with tab2:
        st.header("Filtered Data")
        st.dataframe(filtered_df)

        # Filtros
        csv_data = convert_df_to_csv(filtered_df)
        st.download_button(
            label="Download Filtered Data",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
        if not filtered_df.empty:
            chart_kwargs = {
                "data_frame": filtered_df,
                "x": 'Name' if 'Name' in df.columns else filtered_df.index,
                "y": selected_column,
                "title": f"{selected_column} by Name (Excluding Selected)",
                "labels": {"Name": "Player Name", selected_column: "Value"},
                "height": 600,
            }
        else:
            st.warning("No data available. Please check the Google Sheet URL or try again later.")

# --- Refrescar Datos ---
if st.button("Refrescar Datos"):
    df = fetch_data(sheet_url)
    st.write("Refrescado existosamente!")

# --- Subir archivo a Google Drive ---
def upload_to_drive(local_file_path, drive):
    # Authenticate Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)
    
    # Create and upload file to Google Drive
    file_drive = drive.CreateFile({'title': os.path.basename(local_file_path)})
    file_drive.Upload()

    # Provide confirmation
    st.success(f"File uploaded successfully: {file_drive['title']}")

# Sample usage with a PDF file
pdf_file_path = "sample.pdf"

# Open the PDF file
with open(pdf_file_path, "rb") as f:
    pdf_reader = PyPDF2.PdfReader(f)
    page = pdf_reader.pages[0]
    text = page.extract_text()
    print(text)