import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

st.title("Findings")

df=pd.read_csv('data/StudentPerformanceFactors.csv')

tab1, tab2 = st.tabs(['Sterke correlaties', 'Zwakke correlaties'])

with tab1:
    st.write("""Uit de analyse van de dataset blijkt dat verschillende factoren invloed hebben op je eindcijfer. Maar twee factoren kwamen steeds 
             duidelijk terug: Hours_Studied en Attendance. Heel logisch als je erover nadenkt. Hoe meer tijd je aan school besteed, hoe hoger je eindcijfer.
             Hieronder wordt dit verband nog eens duidelijk weergegeven aan de hand van enkele plots:""")

    fig = px.scatter(df, x='Hours_Studied', y='Exam_Score', trendline='ols', trendline_color_override='red', hover_data=['Attendance'])
    st.plotly_chart(fig)

    X = df['Hours_Studied']           
    Y = df['Exam_Score']              
    X_const = sm.add_constant(X)      
    model = sm.OLS(Y, X_const).fit()  
    slope = model.params['Hours_Studied']
    st.write(f'Voor elk uur dat je langer studeert gaat je score met ongeveer **{round(slope, 2)} punten** omhoog')

    fig2 = px.scatter(df, x='Attendance', y='Exam_Score', trendline='ols', trendline_color_override='red', hover_data=['Hours_Studied'])
    st.plotly_chart(fig2)

    X = df['Attendance']           
    Y = df['Exam_Score']              
    X_const = sm.add_constant(X)      
    model = sm.OLS(Y, X_const).fit()  
    slope = model.params['Attendance']
    st.write(f'Voor elke procent meer die je aanwezig bent gaat je score met ongeveer **{round(slope, 2)} punten** omhoog')

    df_filtered = df[(df['Attendance'] <= 99) & (df['Hours_Studied'] <= 40)]
    fig3 = px.density_heatmap(
        df_filtered,
        x="Hours_Studied",
        y="Attendance",
        z="Exam_Score",
        histfunc="avg",
        nbinsx=15,
        nbinsy=15,
        color_continuous_scale="Viridis",
        labels={"Attendance":"Attendance (%)"},
        title="Gemiddelde Exam Score per Hours & Attendance (%)"
    )

    st.plotly_chart(fig3)

    st.markdown('---')
    st.write('''Wat we uit de dataset kunnen afleiden is vrij logisch: wie vaker naar school gaat en meer huiswerk maakt, behaalt hogere cijfers.
            Er zijn echter nog enkele verbeterpunten voor de dataset. Zo geeft de data een vrij eentonig beeld van studenten, aangezien bijna iedereen een voldoende 
            haalt. De laagste Exam_Score is namelijk 55, wat nog een voldoende is; dit probleem zien we ook terug in de aanvullende dataset. Hierdoor is het moeilijk 
            om factoren te identificeren die mogelijk een negatieve invloed hebben op de cijfers. Daarnaast is de tweede dataset nog niet volledig opgeschoond, 
            wat in de toekomst zeker verbeterd kan worden.''')

with tab2:
    st.write("""Naast het overduidelijke verband tussen, tijd aan school besteden en een hogercijfer, zijn er ook nog zwakkere verbanden. Zoals
             Parental Involvement, Access to Resources en Previous Scores. Deze verbanden zijn logisch te verklaren en ook waarom ze minder sterk zijn. Als je
             ouders meer aandacht aan je school besteden voel jij waarschijnlijk meer druk om beter te presteren. Als je meer toegang hebt tot hulpmiddelen die je helpen bij school
             kan het makkelijker zijn om te leren. Daarnaast zegt je vorige cijfer wellicht iets over een trend waar in je zit. Deze verbanden zijn hieronder in verschillende grafieken
             weergegeven:""")

    fig = px.scatter(df, x='Previous_Scores', y='Exam_Score', trendline='ols', trendline_color_override='red')
    st.plotly_chart(fig)

    X = df['Previous_Scores']           
    Y = df['Exam_Score']              
    X_const = sm.add_constant(X)      
    model = sm.OLS(Y, X_const).fit()  
    slope = model.params['Previous_Scores']
    st.write(f'Voor elke punt die je hoger scoorde op je vorige toets gaat je score met ongeveer **{round(slope, 2)} punten** omhoog')

    fig2 = px.box(df, x='Parental_Involvement', y='Exam_Score', color='Parental_Involvement')
    st.plotly_chart(fig2)

    fig3 = px.box(df, x='Access_to_Resources', y='Exam_Score', color='Access_to_Resources', category_orders={'Access_to_Resources': ["Low","Medium",'High']})
    st.plotly_chart(fig3)

    st.markdown('---')
    st.write('''Wat we uit de dataset kunnen afleiden is vrij logisch: wie vaker naar school gaat en meer huiswerk maakt, behaalt hogere cijfers.
            Er zijn echter nog enkele verbeterpunten voor de dataset. Zo geeft de data een vrij eentonig beeld van studenten, aangezien bijna iedereen een voldoende 
            haalt. De laagste Exam_Score is namelijk 55, wat nog een voldoende is; dit probleem zien we ook terug in de aanvullende dataset. Hierdoor is het moeilijk 
            om factoren te identificeren die mogelijk een negatieve invloed hebben op de cijfers. Daarnaast is de tweede dataset nog niet volledig opgeschoond, 
            wat in de toekomst zeker verbeterd kan worden.''')



