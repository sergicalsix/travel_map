import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
from geocode import get_place_data,str_list_to_numpy_array

st.set_page_config(
   page_title="Travel Planer",
)

st.title("Travel Planer")
st.write('<style>h1 {color: red;}</style>', unsafe_allow_html=True)

#st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
#st.markdown('<i class="material-icons">face</i>', unsafe_allow_html=True)
#st.image('img/icons/sch.png')
#st.image('<i class="material-icons"> ":face:" </i>', unsafe_allow_html=True)
#password = st.text_input('パスワードを入力してください')

#st.sidebar.image('img/icons/flag.png')

st.markdown("""-----""")
#st.sidebar.markdown("""-----""")


raw_places = st.text_input('行きたい場所をスペース区切りで入力してください')
places_list = raw_places.split()
if raw_places:
    for p in places_list:
        st.markdown(f'{p}')

    raw_place_data = np.array(get_place_data(places_list))
    place_type,lat,long = raw_place_data[:,0], raw_place_data[:,1], raw_place_data[:,2]
    lat,long = str_list_to_numpy_array(lat),str_list_to_numpy_array(long)
    df = pd.DataFrame()
    df['place_type'] = place_type
    df['lat'] = lat
    df['lon'] = long
st.markdown('---------')
go = st.checkbox('地図を出力')

if go:
    st.map(df)
st.markdown("""-----""")
