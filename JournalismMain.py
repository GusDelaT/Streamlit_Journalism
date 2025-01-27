import streamlit as st
import pandas as pd
import os
import base64
from io import StringIO

# Streamlit setup
st.set_page_config(
    page_title="Formulario de Redacción",
    layout="wide"
)

# Fetch data from a CSV URL
def fetch_data(sheet_url: str):
    try:
        return pd.read_csv(sheet_url)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRSKqRqiv_7LHJsO3rvH8Cng9Nvr1hKmT143s3i9LUCTrZv0mCxU-3mDiS9bO4jhe3XbT-n9mgU78k_/pub?gid=0&single=true&output=csv"

# Fetch data
df = fetch_data(sheet_url)

# Convert DataFrame to CSV for download
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

st.title("Formulario de Redacción")
st.caption("Recordá incluir tu nombre y puesto laboral previo a dar al botón de finalizar.")
nombre = st.text_input("Nombre")
puesto_laboral = st.text_input("Puesto Laboral")
st.sidebar.header("Filtrar opciones")

# Filter data and display
if not df.empty:
    selected_column = st.sidebar.selectbox(
        "Selecciona un periódico",
        options=df.columns
    )

    if 'Name' in df.columns:
        excluded_names = st.sidebar.multiselect(
            "Filtrar periódicos",
            options=df['Name'].unique(),
            default=[]
        )
        filtered_df = df[~df['Name'].isin(excluded_names)]
    else:
        filtered_df = df

    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        min_val, max_val = df[col].min(), df[col].max()
        selected_range = st.sidebar.slider(f"Seleccionar {col}", min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]

if st.button("Refrescar Datos"):
    df = fetch_data(sheet_url)
    st.write("Refrescado exitosamente!")

# Tabs for content
st.title("Tus Datos + 15 Observaciones")
tab1, tab2 = st.tabs(["Overview", "Filtrados"])

# Tab 1: Overview
with tab1:
    st.header("Overview")
    col1, col2 = st.columns([1.5, 1.5]) 

    with col1:
        edited_df = st.data_editor(df,
            num_rows="dynamic",  
            column_config={
                "Name": st.column_config.Column(pinned=True),
            }
        )

        if st.button("Finalizar"):
            if nombre and puesto_laboral:
                file_name = f"{nombre}_{puesto_laboral}.csv"
                edited_df.to_csv(file_name, index=False)
                
                # Provide a download link for the user
                csv_data = convert_df_to_csv(edited_df)
                st.download_button(
                    label="Download CSV File",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv"
                )
                
                st.success("Cambios guardados y archivo CSV listo para descargar.")
            else:
                st.error("Por favor ingrese tanto el nombre como el puesto laboral.")

# Tab 2: Filtered Data
with tab2:
    st.header("Filtered Data")
    st.dataframe(filtered_df)

    csv_data = convert_df_to_csv(filtered_df)
    st.download_button(
        label="Download Filtered Data",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )


    with col2:
        st.subheader("PDF Viewer")
        pdf_links = {
            "Periódico 1": "18tZvzD8Iv3w0U7iRfN_K9AH3jcwkVyYn",
    "Periódico 2": "19Dfm62cx2DozMX04mH5UDjfCkXYcTa6b",
    "Periódico 3": "1UbNMpX1tgpPDrLLKhoPjuO3Sktf9OPdI",
    "Periódico 4": "1igQK6jP34Y7-vaAaQ4KCtjsb45rxSkBC",
    "Periódico 5": "1SrOM1FwAoZfNeWEh9BJLCfbHhi9Fi-Zd",
    "Periódico 6": "1hSx0HSXfJSwxZonPsggyumXJWwTtxQ-2",
    "Periódico 7": "1VjTbJSbEGg_iT_IF88rJ_X5Aku-o0IOk",
    "Periódico 8": "17a1kwFuGdl12LxB8q0X30wceciK1Kb_6",
    "Periódico 9": "1KIRMS8up_xlmxGAGj3TaT1u9747qXaOc",
    "Periódico 10": "1IaDnFBfMS9JT4ZeVQ0u5W8Ar2i9RPMnn",
    "Periódico 11": "19VB1SnYROs1GMmKQECVskpu1iMbK7ejL",
    "Periódico 12": "1Gs0xc6WqZCSpk6Gqk4qafOO6n4vmyROX",
    "Periódico 13": "15i_uplyIGD7swONxaBkNB6X4cjYlj8Vj",
    "Periódico 14": "1gnFNR5ySN_5EEFKq2C6ytlyzx7JUyIeW",
    "Periódico 15": "1msU35-Pv3SpiFr2GPRJwutTXWRQHpmTL"
        }

        selected_pdf = st.selectbox("Select a PDF to view:", list(pdf_links.keys()), key="pdf_select")
        if selected_pdf:
            file_id = pdf_links[selected_pdf]
            pdf_url = f"https://drive.google.com/file/d/{file_id}/preview"
            st.markdown(f'<iframe src="{pdf_url}" width="90%" height="800"></iframe>', unsafe_allow_html=True)
            st.success(f"Displaying: {selected_pdf}")

# Tab 2: Filtros de Data
with tab2:
    st.header("Filtered Data")
    st.dataframe(filtered_df)

    csv_data = convert_df_to_csv(filtered_df)
    st.download_button(
        label="Download Filtered Data",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )