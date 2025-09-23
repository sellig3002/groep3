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
    y="Probability [-]",
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

st.subheader("Select variables:")
selected_features = []
for feat in all_features:
    if st.checkbox(feat, value=True, key=f"df2_{feat}"):
        selected_features.append(feat)

sub2 = df2[df2["Tolerance"] == tolerance]
sub2 = sub2[sub2["Features"].apply(lambda x: set(x.split(", ")) == set(selected_features))]

if sub2.empty:
    st.warning("No results for this combination of features and tolerance.")
else:
    fig = px.bar(
        sub2,
        x="Model",
        y="Probability [-]",
        error_y="Std",
        color="Model",
        title=f"Accuracy with tolerance: {tolerance}"
    )

    fig.update_traces(error_y=dict(color='white', thickness=2, width=8))
    fig.update_yaxes(range=[0, 1.05])

    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
In deze plot zijn alle mogelijke combinaties (hopelijk, code runnen duurde bijna 2 uur) te maken en de impact die elke variabele heeft op de totale nauwkeurigheid. Ook is weer een slider aanwezig die laat zien hoe accuraat de modellen zijn op basis van de tolerantie op de gok van de score. In de volgende plot
zullen deze opties gebruikt worden in combinatie met het verschil tussen de training data en de test data. Eventuele afwijkingen van de verwachting (dat de test data wat slechter zal zijn dan de training data) zullen hierna ook zo goed mogelijk verklaard worden.
""")


path3 = os.path.join("bestanden", "model_tolerance_results_all_features_prediction.csv")
df3 = pd.read_csv(path3)
df4 = df2.copy()

tolerance = st.slider("Select tolerance:", 0, 5, 0, key="3rd plot tolerance slider")
st.subheader("Select variables:")
selected_features_pred = []
for feat in all_features:
    if st.checkbox(feat, value=True, key=f"df3_{feat}"):
        selected_features_pred.append(feat)

sub3 = df3[df3["Tolerance"] == tolerance]
sub3 = sub3[sub3["Features"].apply(lambda x: set(x.split(", ")) == set(selected_features_pred))]
sub4 = df4[df4["Tolerance"] == tolerance]
sub4 = sub4[sub4["Features"].apply(lambda x: set(x.split(", ")) == set(selected_features_pred))]


if sub4.empty or sub3.empty:
    st.warning("No results for this combination of features and tolerance.")
else:
    sub4 = sub4.copy()
    sub4["Dataset"] = "Train (validation)"
    sub3 = sub3.copy()
    sub3["Dataset"] = "Test (prediction)"

    combined = pd.concat([sub4, sub3], ignore_index=True)

    fig = px.bar(
        combined,
        x="Model",
        y="Probability [-]",
        error_y="Std",
        color="Dataset",
        barmode="group",
        category_orders={"Dataset": ["Train (validation)", "Test (prediction)"]},
        color_discrete_map={
        "Train (validation)": "steelblue",
        "Test (prediction)": "orange"},
        title=f"Accuracy comparison (tolerance={tolerance})"
    )
    fig.update_traces(error_y=dict(color='white', thickness=2, width=8))
    fig.update_yaxes(range=[0, 1.05])

    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
Te zien in het figuur hierboven, de dataset waarop het model getrained is, is heel goed te voorspellen. De dataset die "voorspeld" moet worden is heel slecht te voorspellen. Dat kan diverse redenen hebben. De belangrijkste is dat de test data veel meer mediaan waardes heeft, omdat een significant gedeelte
van de data voor kwam als NaN waarde. Dit is te zien in de analyse, als beide datasets geladen zijn. Door te vergelijken hoeveel de training data en de test data aan NaN waardes hebben in de verschillende kolommen die overeen komen is al te zien dat de test data veel minder accuraat zal zijn op de werkelijkheid
dan de training data ooit zou kunnen voorspellen.

Een ander probleem kan de spreiding van de data in beide datasets zijn. De trainig dataset heeft een attendance tussen de 60 en 100%, terwijl die van de test data niet boven de 92% uit komt. De training data had ook perfecte scores, terwijl de test data dit niet heeft. De totale hoeveelheid uren die gestudeerd zijn
is ook verschillend bij de minima en maxima, namelijk 1 tegenover 0 en 33 tegenover 44. Dit zorgt ervoor dat de data niet perfect kan worden vergeleken met elkaar (waar meer gelet op had moeten worden, of de keuze moeten maken om één dataset te kiezen ipv twee) en resulteert ook in afwijkende nauwkeurigheden.
""")
