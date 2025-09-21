import streamlit as st
import plotly.express as px
import pandas as pd
import os


sidebarknop = st.sidebar.checkbox('Gebruik uitgebreide dataset')

st.title('Analyse')
maindf = "data/StudentPerformanceFactors.csv"
if os.path.exists(maindf):
    df1 = pd.read_csv(maindf)
else:
    st.warning('Nog geen dataset opgehaald, ga terug naar de hoofdpagina')

if sidebarknop:
    bestand = 'data/combined_students.csv'
    if os.path.exists(bestand):
        df = pd.read_csv(bestand)
    else:
        st.warning(
            'Uitgebreide dataset bestaat nog niet, genereer deze op de hoofdpagina'
        )
else:
    df = df1

tab1, tab2 = st.tabs(["Algemene analyse", "Verdelingen per categorie"])
with tab1:
    st.subheader('Algemene analyse')
    st.write('Aantal rijen en kolommen:', df.shape)
    st.write('Kolommen en types:')
    st.dataframe(df.dtypes)
    st.write('Missing values per kolom:')
    st.dataframe(df.isna().sum())
    

with tab2:
    st.subheader('Verdelingen per categorie')
    numeriek_kolom = df.select_dtypes(include=['float64','int64']).columns
    for kolom in numeriek_kolom:
        fig = px.histogram(df, x=kolom, nbins=15, title=f'Verdeling {kolom}')
        st.plotly_chart(fig)
        with st.expander(f'Statistieken voor {kolom}'):
            st.write(df[kolom].describe())

    categorische_kolom = df.select_dtypes(include=['object']).columns
    for kolom in categorische_kolom:
        fig = px.bar(df, x=kolom, title=f'Verdeling {kolom}')
        st.plotly_chart(fig)
        with st.expander(f'Statistieken voor {kolom}'):
            st.write("Aantal unieke waarden:", df[kolom].nunique())
            st.write("Frequenties:")
            st.write(df[kolom].value_counts().head(10))

