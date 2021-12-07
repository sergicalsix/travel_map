import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static
from codes import get_place_data,str_list_to_numpy_array, route_selection
from typing import List

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
    raw_place_data = np.array(get_place_data(places_list))
    place_type,lat,long = raw_place_data[:,0], raw_place_data[:,1], raw_place_data[:,2]
    urls = [ f'https://www.google.com/search?q={place}' for place in places_list]
    try:
        lat,long = str_list_to_numpy_array(lat),str_list_to_numpy_array(long)
    except:
        st.markdown('検索できなかった場所があります')
    df = pd.DataFrame()
    df['place_name'] = places_list
    df['place_type'] = place_type
    df['lat'] = lat
    df['long'] = long
    df.index = range(1,len(lat) + 1)
    st.dataframe(df)
st.markdown('場所のリンクはこちら')
for i,place_url in enumerate(zip(places_list,urls)):
    link = f'[{i+1} : {place_url[0]}]({place_url[1]})'
    st.markdown(link, unsafe_allow_html=True)
st.markdown('---------')

map_flag = st.checkbox('地図を出力')

if map_flag:
    m = folium.Map(location=[lat[0],long[0]], zoom_start=12) #locationとzoomは改良の余地あり
    for place_,lat_,long_ in zip(places_list,lat,long):
        folium.Marker(
            location=[lat_, long_],
            popup=place_,
        ).add_to(m)
    folium_static(m)
    if len(lat) > 2:
        route_ = st.checkbox('提案ルートを出力')
        selected_route:List[str] = route_selection(df) #背後で動く
    if route_:
        k = 0
        #m = folium.Map(location=[lat[0],long[0]], zoom_start=12) #locationとzoomは改良の余地あり
        for i in df.index:
            for j in df.index:
                if k < len(selected_route) and [i,j] == selected_route[k]:
                    locations= [[lat[i-1],long[i-1]], [lat[j-1], long[j-1]]] 
                    line = folium.PolyLine(locations=locations)
                    m.add_child(line)
                    k += 1
                    
        folium_static(m)

st.markdown("""-----""")
