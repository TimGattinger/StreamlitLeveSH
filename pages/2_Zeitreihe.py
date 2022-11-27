import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from streamlit_folium import st_folium
import folium
import csv

st.title("Zeitreihe")
st.sidebar.info('Diese App zeigt Pegelstände von Schleswig Holstein und deren statistische Auswertung. Aktuell und als Zeitreihe. Tim Gattinger 09/2022')
st.sidebar.success('Quelle http://www.umweltdaten.landsh.de')
st.sidebar.write("Pegel " +  st.session_state["my_input"] + " ausgewählt")

try:



    Ort = st.session_state["my_input"]
    query = f"name=='{Ort}'"

    df = pd.read_pickle("PegelMetadatenStats.pkl")
    df_f = df.query(query)
    #st.write(df_f)
    t_ID = df_f['ID'].values[0]
    ### anedern wenn online als app/Github
    t = r"C:\Users\User\_pegel_Atom\Pegelab1900\\" + str(t_ID) + ".pkl"
    Pegeltitle = "Pegel " + str(Ort) + ", ID: " + str(t_ID)
    df = pd.read_pickle(t)

    oldest = df['date'].min()
    old = str(oldest)
    old = old[0:4]

    ####TimeSlider Start Time selector
    from datetime import date

    current_year = date.today().year
    slider = st.slider('Wähle ein Start Jahr ', min_value=int(old), value=2012 ,max_value=current_year, step=1)#

    startS = str(slider) + "-1-1"
    endS = str(current_year) + "-12-31"

    mask = (df['date'] > startS) & (df['date'] <= endS)
    df = df.loc[mask]

    tab1, tab2, tab3 = st.tabs(["Graph", "Histogramm", "Statistiken"])


    with tab1:
    #st.dataframe(df.head())
    # Create figure
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=list(df.date), y=list(df.level), line_shape='spline'))
            #go.Scatter(df, x='date', y='level', line_shape='spline'))

        fig.add_hline(y=df_f['MW10'].values[0], line_color='black', line_dash='dash', annotation_text="MW10")
        fig.add_hline(y=df_f['MQ100'].values[0], line_color='red', line_dash='dash', annotation_text="Hundertjähriges Hochwasser (MQ100)")
        fig.add_hrect(y0=df_f['MNW10'].values[0], y1=df_f['MHW10'].values[0], line_width=0, fillcolor="black", opacity=0.2)

        # Set title

        fig.update_layout(
            title_text=Pegeltitle
        )

        # Add range slider
        fig.update_layout(width=900,height=600,
            xaxis=dict(title='Datum',

                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),

                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        level = [df['level']]

        group_labels = ['Pegelstände [cm PN]'] # name of the dataset

        fig2 = ff.create_distplot(level, group_labels)
        fig2.update_layout(
            title_text=Pegeltitle
        )

        st.plotly_chart(fig2, use_container_width=True)

    with tab3:



        fig = px.box(df, x ='year', y ='level', title="Pegelstände gruppiert nach Jahr von " + str(slider) + " bis " + str(current_year),

        labels={
                     "year": "Jahr",
                     "level": "Pegelstand"

                 }
        )
        st.plotly_chart(fig, use_container_width=True)

        fig = px.box(df, x ='month', y ='level', title="Pegelstände gruppiert nach Monat von " + str(slider) + " bis " + str(current_year),
        labels={
                     "month": "Monat",
                     "level": "Pegelstand"

                 }
        )
        st.plotly_chart(fig, use_container_width=True)
        st.table(df.describe())

except:
    st.write("Bitte wählen Sie einen Pegel auf der Hauptseite")
