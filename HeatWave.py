import requests
from pyproj import Transformer
from GetCordinate import get_cord

def get_heatwave(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)

    url = "https://mosdac.gov.in/geoserver_2/heat_popup/wms"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.1.1",
        "REQUEST": "GetFeatureInfo",
        "FORMAT": "image/png",
        "TRANSPARENT": "true",
        "QUERY_LAYERS": "heat_popup:FCST48_TMAX",
        "LAYERS": "heat_popup:FCST48_TMAX",
        "STYLES": "",
        "INFO_FORMAT": "application/json",
        "X": 128,  
        "Y": 128,  
        "WIDTH": 256,
        "HEIGHT": 256,
        "SRS": "EPSG:3857",
        "BBOX": f"{x-5000},{y-5000},{x+5000},{y+5000}"  
    }

    response = requests.get(url, params=params)
    try:
        json_data = response.json()
        print(json_data)
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")