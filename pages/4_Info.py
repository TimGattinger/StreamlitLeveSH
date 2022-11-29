import streamlit as st

st.title("Info")
st.sidebar.info('Diese App zeigt Pegelstände von Schleswig Holstein. Aktuell und historisch. Tim Gattinger 11/2022')
st.sidebar.success('Quelle http://www.umweltdaten.landsh.de')
st.sidebar.write("Pegel " +  st.session_state["my_input"] + " ausgewählt")

st.write("Diese Seite ist ein Hobbyprojekt von mir und eins meiner ersten Browser Apps. Ich hatte es mir zur Aufgabe gemacht, die Zeitreihe von den offiziellen Stellen (http://www.umweltdaten.landsh.de) automatisiert zu spiegeln und sie noch einmal auf eine andere Art darzustellen und auszuwerten.")
st.write("Die Karte zeigt den aktuellen Pegelstand qualitativ in vier Farben an (Grün, Gelb, Orange, Rot). Relativ zu den hier anhand der Zeitreihe selbst berechneten Statistiken wird die Markierung des Pegelstandorts beispielsweise Grün, wenn sie sich der Pegelstand aktuell unter dem MNW10 (mittlerer niedrigster Wert der Wasserstände der letzten 10 Jahre) befindet. Der Status des Pegels wird hingegen Rot, wenn der mittlere höchste Wert über 10 Jahre gemittelt überschritten wird. In dem Graphen der Zeitreihe ist der Bereich zwischen MNW10 und MHW10 grau gefärbt und der MW ist als schwarze gestrichelte Linie dargestellt. Das auf Grundlage der vorliegenden Daten statistisch berechnete hundertjährige Hochwasser erscheint als gestrichelte rote Linie im Graphen.")


col1, col2, col3 = st.columns(3)


with col1:

    st.write("MQ100:")#            Hundertjähriges Hochwasser")
    st.write("MNW10:")#              mittlerer niedrigster Wert der Wasserstände in einer Zeitspanne")
    st.write("MW10:")#               Mittelwert der Wasserstände in einer Zeitspanne")
    st.write("MHW10:")#              mittlerer höchster Wert der Wasserstände in einer Zeitspanne")

with col2:

    st.write("Hundertjähriges Hochwasser")
    st.write("mittlerer niedrigster Wert der Wasserstände in 10 Jahren")
    st.write("Mittelwert der Wasserstände in 10 Jahren")
    st.write("mittlerer höchster Wert der Wasserstände in 10 Jahren")
