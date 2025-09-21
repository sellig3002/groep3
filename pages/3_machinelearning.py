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
Door de tolerance aan te passen, is te zien dat het model behoorlijk goed in de buurt zit van de exacte waarde. Om een exacte waarde te geven tussen de 60 en 100 is behoorlijk moeilijk. Door 1 punt erboven of eronder te mogen zitten, zijn bijna alle modellen gelijk al ±50% correct.
De errorbars zijn aanwezig omdat met de modellen een willekeurig beginpunt gekozen kan worden. Dit beginpunt beïnvloedt hoe accuraat het model is aan het eind en door het model honderd keer een voorspelling te geven, kan een standaarddeviatie uit gehaald worden, die aan geeft in welke hoeveelheid het model
kan afwijken in nauwkeurigheid.
""")

path2 = os.path.join("bestanden", "model_tolerance_results_all_features.csv")
df2 = pd.read_csv(path2)

tolerance = st.slider("Select tolerance:", 0, 5, 0, key="2nd plot tolerance slider")
all_features = sorted(set(",".join(df2["Features"]).replace(" ", "").split(",")))

st.subheader("Select features:")
selected_features = []
for feat in all_features:
    if st.checkbox(feat, value=True):
        selected_features.append(feat)

sub2 = df2[df2["Tolerance"] == tolerance]
sub2 = sub2[sub2["Features"].apply(lambda x: set(x.split(", ")) == set(selected_features))]

if sub2.empty:
    st.warning("No results for this combination of features and tolerance.")
else:
    fig = px.bar(
        sub2,
        x="Model",
        y="Mean",
        error_y="Std",
        color="Model",
        title=f"Accuracy with tolerance: {tolerance}"
    )

    fig.update_traces(error_y=dict(color='white', thickness=2, width=8))
    fig.update_yaxes(range=[0, 1.05])

    st.plotly_chart(fig, use_container_width=True)
