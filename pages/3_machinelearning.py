import pandas as pd
import streamlit as st
import plotly.express as px
import os

path = os.path.join("bestanden", "model_tolerance_results.csv")
df = pd.read_csv(path)

st.title("Machine Learning")

st.markdown("""
Om te zorgen dat de modellen kunnen werken op beide datasets, zullen de datasets eerst met elkaar vergeleken moeten worden. Deze datasets hebben namelijk niet dezelfde kolommen, omdat ze een andere oorsprong hebben.
De twee dataframes zijn handmatig aangepast om te zorgen dat ze dezelfde kolommen, met dezelfde namen, hebben. De resulterende kolommen staan hieronder:
""")

with st.expander("Show/Hide DataFrame Columns"):
    st.write(["Hours_Studied",
             "Attendance",
             "Parental_Involvement",
             "Previous_Scores",
             "Gender",
             "Exam_Score"])

st.markdown("""
Alle kolommen komen overeen met elkaar en kunne benut worden door de modellen om een voorspelling te maken. Hieronder staat een barplot waarin alle variabelen worden gebruikt. Belangrijk om te weten is dat niet alle variabelen nuttig hoeven te zijn voor een voorspelling. Later kan dit ook zelf bekeken worden waarin alle variabelen gebruikt kunnen worden.
""")

tolerance = st.slider("Select tolerance:", 0, 5, 0)

sub = df[df["Tolerance"] == tolerance]

fig = px.bar(
    sub,
    x="Model",
    y="Mean",
    error_y="Std",
    color="Model",
    title=f"Accuracy with {tolerance} points of leeway of tolerance")

fig.update_traces(error_y=dict(color='white', thickness=2, width=8))
fig.update_yaxes(range=[0, 1.05])

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
In het figuur hierboven zijn verschillende modellen te zien die gefit zijn op de grote dataset. 
""")
