import geocoder
import numpy as np 
import pandas as pd
import pydeck as pdk
from typing import List, Any

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
    place_data = [None] * len(places)
    for i,place in enumerate(places):
        place_data[i] = get_place_datum(place)
    
    return place_data
    
def str_list_to_numpy_array(str_list:List[str]):
    """
    ['1.1','1.3'] -> array([1.1,1.3])
    """
    return np.array(list(map(float,str_list)))

#使えるかわからない
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
    

