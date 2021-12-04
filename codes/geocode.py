import geocoder
from typing import List, Any

def get_place_datum(place:str) -> List[Any]:
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
    
    
print(get_place_data(['清水寺','清']) )