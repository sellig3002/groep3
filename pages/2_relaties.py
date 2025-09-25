import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os


sidebarknop = st.sidebar.checkbox('Gebruik uitgebreide dataset')

st.title('Relaties')

student_data_main = pd.read_csv("data/StudentPerformanceFactors.csv")

if sidebarknop:
    bestand = 'data/combined_students.csv'
    if os.path.exists(bestand):
        student_data = pd.read_csv(bestand)
    else:
        st.warning(
            'Uitgebreide dataset bestaat nog niet, genereer deze op de hoofdpagina'
        )
else:
    student_data = student_data_main

tab1, tab2 = st.tabs(['Highlights van de data','Vergelijk met Exam_Score'])

with tab1:
    numeric_student_data = student_data.select_dtypes(include = 'number')
    correlation_matrix = numeric_student_data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlation_matrix, annot = True, cmap = 'plasma')
    st.pyplot(fig)

    fig1 = px.scatter(
        student_data,
        x = 'Hours_Studied',
        y = 'Exam_Score',
        color = 'Gender',
        opacity = 0.4,
        color_discrete_map = {
            'Male': 'green',
            'Female': 'red'
        },
        size_max = 10,
        labels = {
            'Hours_Studied': 'Aantal gestudeerde uren',
            'Exam_Score': 'Examenscore'
        },
        title = 'Verband tussen examenscore en het aantal gestudeerde uren'
    )
    st.plotly_chart(fig1) 

    fig2 = px.scatter(
        student_data,
        x = 'Attendance',
        y = 'Exam_Score',
        color = 'Teacher_Quality',
        color_discrete_map = {
            'Low': 'red',
            'Medium': 'yellow',
            'High': 'green'
        },
        opacity = 0.4,
        size_max = 10,
        labels = {
            'Attendance': 'Aanwezigheid van student in uren',
            'Exam_Score': 'Examenscore'
        },
        title = 'Verband tussen examenscore en het aantal bezochte lesuren',
        category_orders = {
            'Teacher_Quality': ['High', 'Medium', 'Low']
        }
    )
    st.plotly_chart(fig2)

    fig3 = px.scatter(
        student_data,
        x = 'Sleep_Hours',
        y = 'Exam_Score',
        color = 'Extracurricular_Activities',
        size_max = 10,
        opacity = 0.6,
        labels = {
            'Sleep_Hours': 'Slaapuren van student',
            'Exam_Score': 'Examenscore op schaal van 0 tot 100'
        },
        title = 'Verband tussen examenscore en het aantal geslaapte uren',
        category_orders={
            'Extracurricular_Activities': ['Yes', 'No']
        }
    )
    st.plotly_chart(fig3)

    color_map = {
        'Public': 'rgb(24, 60, 80)',
        'Private': 'rgb(200, 40, 90)'
    }

    plot_type = st.radio("Kies type plot:", ["Scatterplot", "Histogram"])

    if plot_type == "Scatterplot":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=student_data['Attendance'],
            y=student_data['Hours_Studied'],
            mode='markers',
            marker=dict(
                color=student_data['School_Type'].map(color_map),
                size=10,
                opacity=0.6
            ),
            name='Scatterplot'
        ))
        fig.update_layout(
            title="Verband tussen aanwezigheid en aantal gestudeerde uren (Scatterplot)",
            xaxis_title="Aanwezigheid van student in uren",
            yaxis_title="Aantal gestudeerde uren"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:  # Histogram
        fig = go.Figure()
        for school_type, color in color_map.items():
            fig.add_trace(go.Histogram(
                x=student_data.loc[student_data['School_Type'] == school_type, 'Hours_Studied'],
                name=school_type,
                marker_color=color,
                opacity=0.75
            ))
        fig.update_layout(
            title="Verdeling van aantal gestudeerde uren per schoolsoort (Histogram)",
            xaxis_title="Aantal gestudeerde uren",
            yaxis_title="Aantal studenten",
            barmode="overlay"
        )
        st.plotly_chart(fig, use_container_width=True)


    fig5 = px.box(student_data, x = 'Parental_Involvement', y = 'Exam_Score', color = 'Gender')

    fig5.update_layout(
        xaxis_title ='Hulp van ouders',
        yaxis_title ='Examenscore op schaal van 0 tot en met 100',
        title = 'Spreiding van examenscores per ouderinvloedrijke klasse',
    )
    st.plotly_chart(fig5)

    fig6 = px.box(student_data, x = 'Motivation_Level', y = 'Exam_Score', color = 'Gender',
                color_discrete_map={
            'Male': 'rgb(54, 162, 235)',       
            'Female': 'rgb(255, 99, 132)'       
        })

    fig6.update_layout(
        xaxis_title ='Motavatieklasse',
        yaxis_title ='Examenscore op schaal van 0 tot en met 100',
        title = 'Spreiding van examenscores per motivatieklasse',
        
    )
    st.plotly_chart(fig6)

with tab2:
    st.write('Vergelijk hier de veschillende kolommen met de Exam_Score kolom.')
    st.write('***Numeriek***')
    numerieke_kol = student_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    numerieke_kol = [kol for kol in numerieke_kol if kol != 'Exam_Score']

    kolom_keuze = st.selectbox("Kies een numerieke kolom voor de plot:", options=numerieke_kol)

    if kolom_keuze:
        g = sns.jointplot(
            data=student_data,
            x=kolom_keuze,
            y='Exam_Score',
            kind='scatter',
            marginal_kws={'bins':20, 'fill':True}
        )

        st.pyplot(g.fig)  
        plt.close(g.fig)  

    st.write(' ')
    st.write('***Categorisch***')

    categorical_kol = student_data.select_dtypes(include=['object']).columns.tolist()

    kolom_keuze = st.selectbox("Kies een categorische kolom voor de boxplot:", options=categorical_kol)

    if kolom_keuze:
        plt.figure(figsize=(8,5))
        sns.boxplot(data=student_data, x=kolom_keuze, y='Exam_Score')
        plt.title(f'Exam scores vs {kolom_keuze}')
        
        st.pyplot(plt.gcf())
        plt.close()
