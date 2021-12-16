import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static
from skmob.utils.gislib import getDistance
from codes import get_place_data,str_list_to_numpy_array, route_selection , draw_bar , marker_decoration
from typing import List, Dict

st.set_page_config(
   page_title="Travel Planner",
)

st.title("Travel Planner")
st.write('<style>h1 {color: green;}</style>', unsafe_allow_html=True)

#st.markdown('行きたい場所を入力すると地図が出るアプリ')

#st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
#st.markdown('<i class="material-icons">face</i>', unsafe_allow_html=True)
#st.image('img/icons/sch.png')
#st.image('<i class="material-icons"> ":face:" </i>', unsafe_allow_html=True)
#password = st.text_input('パスワードを入力してください')

#st.sidebar.image('img/icons/flag.png')
st.markdown("""-----""")
#st.sidebar.markdown("""-----""")


raw_places = st.text_input('行きたい場所をスペース区切りで入力してください')
st.markdown('入力例: 京都駅　銀閣寺　金閣寺  仁和寺')

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
    df['場所の名前'] = places_list
    df['場所の種類'] = place_type
    df['緯度'] = lat
    df['経度'] = long
    df.index = range(1,len(lat) + 1)
    st.info('基本情報')
    st.dataframe(df)
    df.columns = ['place','place_type','lat','long']
    st.warning('Googleでの検索結果')
    for i,place_url in enumerate(zip(places_list,urls)):
        link = f'[{i+1} : {place_url[0]}]({place_url[1]})'
        st.markdown(link, unsafe_allow_html=True)
    st.markdown('---------')
    map_flag = st.checkbox('地図を出力')
    st.markdown('---------')



    if map_flag:
        st.success('地図')
        m = folium.Map(location=[lat.mean(),long.mean()], zoom_start=12) #locationとzoomは改良の余地あり
        for place_,type_,lat_,long_ in zip(places_list,place_type,lat,long):
            color_,icon_ = marker_decoration(type_)
            folium.Marker(
                location=[lat_, long_],
                popup=place_,
                icon=folium.Icon(color=color_, icon=icon_)
            ).add_to(m)
        folium_static(m)
        if len(lat) > 2:
            route_ = st.checkbox('最短経路を出力')
            #最適化
            selected_route:List[str] = route_selection(df) 
            if route_:
                st.error('最短経路')
                k = 0
                color = ['blue','red','green','purple','orange'] * 3
                calc_time:List[Dict] = []
                for i in df.index:
                    for j in df.index:
                        if k < len(selected_route) and [i,j] == selected_route[k]:
                            loc1 = [lat[i-1],long[i-1]]
                            loc2 = [lat[j-1], long[j-1]]
                            distance = getDistance(loc1,loc2) #m
                            calc_time.append({'path':f'{places_list[i-1]}-{places_list[j-1]}','time':round(distance / 20 * 60,1)}) #km / 20km / h 
                            locations= [loc1,loc2]
                            line = folium.PolyLine(locations=locations,color = color[k])
                            m.add_child(line)
                            k += 1
                folium_static(m)
                fig = draw_bar(calc_time)
                st.info('所用時間')
                st.plotly_chart(fig)
                st.markdown('所用時間は2点間の距離を時速20kmで進んだと仮定して算出')
                st.markdown("""-----""")

st.markdown("""-----""")
