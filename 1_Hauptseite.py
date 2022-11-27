import streamlit as  st
st.set_page_config(layout='wide',
        page_title="Pegel SH",
        page_icon="xy"
)
import pandas as pd
from streamlit_folium import st_folium
import folium

st.header("Pegelstände in Schleswig-Holstein")
st.sidebar.info('Diese App zeigt Pegelstände von Schleswig-Holstein und deren statistische Auswertung. Aktuell und historisch. Tim Gattinger 09/2022')
st.sidebar.success('Quelle http://www.umweltdaten.landsh.de')
df = pd.read_pickle("PegelMetadatenStats.pkl")


my_input = st.selectbox("Wähle einen Ort in Schleswig-Holstein", df.name, index=9)

st.session_state["my_input"] = my_input
st.session_state["df"] = df

query = f"name=='{my_input}'"
df_f = df.query(query)

t_ID = df_f['ID'].values[0]
PegelA = round(df_f['PegelA'].values[0], 0)
LatW = df_f['LatW'].values[0]
LonW = df_f['LonW'].values[0]
PegelT = df_f['PegelT'].values[0]
MNW = round(df_f['MNW10'].values[0], 1)
MW = round(df_f['MW10'].values[0], 1)
MHW = round(df_f['MHW10'].values[0], 1)
MQ100 = round(df_f['MQ100'].values[0], 1)

col1, col2, col3 = st.columns(3)
st.sidebar.write("Pegel " + str(my_input) + " ausgewählt")


mapx = folium.Map(location=[df.LatW.mean(), df.LonW.mean()],   zoom_start=7, control_scale=False, tiles='OpenStreetMap',
                 width='5')#, crs='EPSG4326')

folium.CircleMarker(location=[LatW,	LonW],
              radius=10, color='black', fill_color='white'
              ).add_to(mapx)

df.apply(lambda row:folium.CircleMarker(location=[row["LatW"],
                                                  row["LonW"]], fill="black",
                                                    popup="Pegel " + row["name"],
                                                    tooltip="Pegel " + row["name"],
                                                    radius=2, color=row["warnSteps"]).add_to(mapx),
                                                    axis=1, )

with col1:
    st_data = st_folium(mapx)


with col2:
    st.subheader("Pegel ")
    st.write("ID:")
    st.write("Aktueller Stand:")
    st.write(" ")
    #st.write(" ")
    #st.write('\n')
    #st.write('\n')
    st.markdown('##')
    st.markdown('##')
    #st.markdown("***")
    st.write("MNW10: ")
    st.write("MW10")
    st.write("MHW10")
    st.write("MQ100")

with col3:
    st.subheader(str(my_input))
    st.write(t_ID)
    st.write(str(PegelA) + " [cm PN]")
    st.write(PegelT)
    st.markdown('##')
    #st.write(" ")
    #st.markdown("***")
    st.write(str(MNW) + " [cm PN]")
    st.write(str(MW) + " [cm PN]")
    st.write(str(MHW) + " [cm PN]")
    st.write(str(MQ100) + " [cm PN]")
