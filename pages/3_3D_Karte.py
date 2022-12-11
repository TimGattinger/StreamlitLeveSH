import streamlit as st
import pandas as pd
from datetime import date
from itertools import cycle
import random
import time
import pydeck

st.sidebar.info('Diese App zeigt Pegelstände von Schleswig Holstein. Aktuell und historisch. Tim Gattinger 12/2022')
st.sidebar.success('Quelle http://www.umweltdaten.landsh.de')
st.sidebar.write("Pegel " +  st.session_state["my_input"] + " ausgewählt")

#bicycle_counts = pd.read_pickle("./3D_Pydeck_normalisedMQ100.pkl")
bicycle_counts = pd.read_pickle("3D_Pydeck_normalisedMQ100_2017_2022.pkl")
counts_df = pd.read_pickle("3D_Pydeck_BasicDataOBJ.pkl")


# don't modify the outputs from a cached streamlit function
counts_df = counts_df.copy()

# resample daily data to monthly means
bicycle_counts = bicycle_counts.resample("M").mean()
years_months_values = [(d.year, d.month) for d in bicycle_counts.index]
year, month = years_months_values[0]

# Setup presentation widgets
st.header("Visualisierung der Pegelstände 2020-2022 in Schleswig-Holstein")
date_value = st.empty()
month_slider = st.empty()
animations = {"Stop": None, "Langsam": 0.4, "Mittel": 0.2, "Schnell": 0.05}
animate = st.radio("", options=list(animations.keys()), index=2)

animation_speed = animations[animate]
deck_map = st.empty()


def render_slider(year, month):
    key = random.random() if animation_speed else None

    month_value = month_slider.slider(
        "",
        min_value=0,
        max_value=len(years_months_values),
        value=years_months_values.index((year, month)),
        format="",
        key=key,
    )
    year, month = years_months_values[month_value]
    d = date(year, month, 1)
    date_value.subheader(f"Datum: {d:%Y}-{d:%m}")
    return year, month


def render_map(year, month):
    mask = (bicycle_counts.index.year == year) & (bicycle_counts.index.month == month)
    month_counts = bicycle_counts[mask].transpose().reset_index()
    month_counts.rename(
        columns={
            month_counts.columns[0]: "ID",
            month_counts.columns[1]: "month_counts",
        },
        inplace=True,
    )

    counts_df["counts"] = counts_df.merge(
        month_counts, left_on="ID", right_on="ID"
    )["month_counts"]

    display_counts = counts_df[~pd.isna(counts_df["counts"])]
    display_counts = display_counts.round(decimals = 1)
    #st.write(display_counts.head())

    deck_map.pydeck_chart(
        pydeck.Deck(
            map_style="mapbox://styles/mapbox/light-v9",#'mapbox://styles/mapbox/outdoors-v12', #"mapbox://styles/mapbox/light-v9",
            initial_view_state=pydeck.ViewState(
                latitude=display_counts.lat.mean(),
                longitude=display_counts.lon.mean(),
                zoom=7.5,
                pitch=50,

            ), tooltip=tooltip,
            layers=[
                pydeck.Layer(
                    "ColumnLayer",
                    data=display_counts,
                    disk_resolution=12,
                    radius=900,
                    elevation_scale=150,
                    get_position="[lon, lat]",
                    get_color="[5, 25, 245]",#"[40, counts / 5000 * 255, 40, 150]",
                    get_elevation="[counts]",
                    pickable=True

                ),
            ],

        )
    )


#display_counts['Fcounts'] = display_counts['counts'].apply(lambda d: f'{round(d, 2):,}')
tooltip={
"html": "Station <b>{name}</b> ({ID}): <b>{counts}</b> % vom hundertjährigen Hochwasser MQ100",
"style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}


if animation_speed:
    for year, month in cycle(years_months_values):
        time.sleep(animation_speed)
        render_slider(year, month)
        render_map(year, month)
else:
    year, month = render_slider(year, month)
    render_map(year, month)
