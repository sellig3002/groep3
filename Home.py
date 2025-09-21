import streamlit as st
import pandas as pd
import subprocess
import os


st.title("Student Performance Dashboard")
st.markdown("""
Welkom!  
Dit dashboard analyseert factoren die het examenresultaat van studenten beïnvloeden.  
Gebruik het menu links om naar **Analyse**, **Relaties**, **Machine Learning** of **Findings** te gaan.
""")

script_path = os.path.join(os.path.dirname(__file__), 'data_ophalen.py')
if st.button('Data inladen'):
    with st.spinner('Data verversen'):
        try:
            subprocess.run(['python','data_ophalen.py'], check=True)
        except Exception as e:
            st.error(f'Fout bij verversen: {e}')

try:
    df1 = pd.read_csv("data/StudentPerformanceFactors.csv")
    st.write("Dataset geladen:", df1.shape)
except Exception as e:
    st.error(f"Kon dataset niet laden: {e}")
    st.stop()


st.dataframe(df1.head())

st.markdown("""
De dataset die wordt gebruikt wordt met de kaggle api opgehaald. Meer informatie over de gebruikte dataset:
            https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
            """)

if st.button('Tweede dataset inladen'):
    df2 = pd.read_csv('data/student_performance_updated_1000.csv')

    df2_renamed = df2.rename(columns={
        "StudyHoursPerWeek": "Hours_Studied",
        "AttendanceRate": "Attendance",
        "PreviousGrade": "Previous_Scores",
        "FinalGrade": "Exam_Score",
        "ExtracurricularActivities": "Extracurricular_Activities",
        "ParentalSupport": "Parental_Involvement"
    })

    df2_aligned = df2_renamed[df1.columns.intersection(df2_renamed.columns)]

    combined = pd.concat([df1, df2_aligned], ignore_index=True, sort=False)
    combined['Extracurricular_Activities'] = combined['Extracurricular_Activities'].apply(
        lambda x: 'No' if (isinstance(x, (int,float)) and x == 0)
        else ('Yes' if isinstance(x,(int,float)) and x > 0 else x)
        )
    combined.to_csv("data/combined_students.csv", index=False)

    st.write('Gecombineerde dataset:', combined.shape)
    st.dataframe(combined.iloc[6600:6615])

st.markdown("""
Voor de aanvullende dataset is een vergelijkbare dataset gekozen. Voor verschillende kolommen geeft deze dataset meer data:
            ["Hours_Studied", "Attendance", "Previous_Scores", "Exam_Score", "Extracurricular_Activities", "Parental_Involvement"]
Voor meer informatie over de dataset: https://www.kaggle.com/datasets/haseebindata/student-performance-predictions""")
    
    