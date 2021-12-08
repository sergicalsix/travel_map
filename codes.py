import geocoder
import numpy as np 
import pandas as pd
import plotly.express as px
import pydeck as pdk #今回は使わない
import pulp
import time
from scipy.spatial import distance
from typing import List,Tuple , Dict, Any

def get_place_datum(place:str) -> List[str]:
    """
    input:  place:str
    output: [ type:str, lat:float , long:float ] 
    """
    assert type(str) != True
    ret = geocoder.osm(place, timeout=1.0)
    if ret.status == 'OK':
        datum:list = [ret.type]
        datum.extend(ret.latlng)
        return datum
    else:
        print(f'情報が取得できなかった場所:{place}')
        return [None, None, None]

def get_place_data(places:List[str]) -> List[Any]:
    """
    input:  places:places:List[str]
    output: [[ type:str, lat:float , long:float ], ...]
    """
    if not type(places) == list:
        try:
            places = list(places)
        except:
            raise ValueError("invaild input to codes/get_place_data")
    #OpenStreetmapのapiを叩く
    place_data = [None] * len(places)
    for i,place in enumerate(places):
        place_data[i] = get_place_datum(place)
        time.sleep(0.1)
    
    return place_data
    
def str_list_to_numpy_array(str_list:List[str]):
    """
    ['1.1','1.3'] -> array([1.1,1.3])
    """
    return np.array(list(map(float,str_list)))

def route_selection(df) -> List[str]:
    """
    pulpで経路最適化
    """
    df = df[['lat','long']]
    w = distance.pdist(df.values) 
    path_ = []
    for i in df.index:
        for j in df.index:
            if i < j:
                path_.append([i,j])
    path_len = len(path_)
    x = [ pulp.LpVariable(f'x{path_[i][0]}_{path_[i][1]}', cat='Binary') for i in range(path_len)]

    p = pulp.LpProblem('route_selection', pulp.LpMinimize)
    #式を追加
    p += pulp.lpDot(w, x)
    #条件を追加
    ##自己ループしない
    for i in range(path_len):
        p += x[i] <= 1
    ##ノード(地点)はエッジ(経路)を2本以上持たない
    edge_index = []
    for node in range(1,len(df) + 1):
        for i,p_ in enumerate(path_):
            if p_[0] == node or p_[1] == node:
                edge_index.append(i)
        print(edge_index)
        p+= pulp.lpSum([x[index] for index in edge_index]) == 2
        edge_index = []
    ##エッジの本数の規定 移動回数を規定できる
    #p+= pulp.lpSum(x) == len(df) - 1

    #実行
    p.solve()
    #選択されたルートを取得
    selected_route = []
    for path,route_ in zip(path_, list(map(pulp.value,x))):
        if route_ == 1.0:
            selected_route.append(path)
    return selected_route

#所要時間の棒グラフ(動的)を描画
def draw_bar(calc_time:List[Dict])-> object:
    """
    input: calc_time: [{'path':'a-b','time':20.3},...]
    """
    color = ['rgb(46, 137, 205)','rgb(114, 44, 121)','rgb(198, 47, 105)','rgb(58, 149, 136)','rgb(107, 127, 135)'] * 3
    df = pd.DataFrame(calc_time)
    df.columns = ['経路','時間(分)']
    df['color'] = color[:len(calc_time)]
    fig = px.bar(df, y='経路', x='時間(分)',color = '経路',orientation='h')

    return fig

def marker_decoration(type_:str)->Tuple[str]:
    """
    input: 'attraction'
    output: ('red','heart')
    """
    #https://glyphsearch.com/?library=glyphicons
    marker_map = {
        'attraction':('red','heart'),
        'station': ('green','road'),
        'bus_stop':('lightblue','road'),
        'administrative':('black', 'tent'),
        'place_of_worship':('blue','eye-open')}
    
    if type_ in marker_map.keys():
        return marker_map[type_]
    return ('lightblue','info-sign')


#今回が使用しない
def view_path(places_list,lat,long):
    df = pd.DataFrame()
    df['name'] = [f"{places_list[i]}-{places_list[i+1]}" for i in range(len(lat) - 1)]
    df['path'] = [[[lat[i],long[0]] ,[lat[i+1], long[i+1]]] for i in range(len(lat) - 1)]
    df['time'] = [i+1 for i in range(len(lat)  - 1)] 
    df['color'] = [(237, 28, 36) for i in range(len(lat)  - 1)]
    
    layer= pdk.Layer(
        type = "PathLayer",
        data=df,
        pickable=True,
        get_color="color",
        width_scale=20,
        width_min_pixels=2,
        get_path="path",
        get_width=5,
    )
    #3次元の地図
    view_state = pdk.ViewState(latitude=lat[0],longitude=long[0], zoom=10)
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r
    

