import requests
from pyproj import Transformer

def get_monsoon(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)

    url = "https://mosdac.gov.in/geoserver_2/monsoon_24/wms"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetFeatureInfo",
        "FORMAT": "image/png",
        "TRANSPARENT": "true",
        "QUERY_LAYERS": "monsoon_24:CAM_Phase01_JJAS_RAIN",
        "LAYERS": "monsoon_24:CAM_Phase01_JJAS_RAIN",
        "STYLES": "",
        "INFO_FORMAT": "application/json",
        "I": 165,  
        "J": 210,
        "WIDTH": 256,
        "HEIGHT": 256,
        "CRS": "EPSG:3857",
        "BBOX": f"{x-5000},{y-5000},{x+5000},{y+5000}" 
    }

    response = requests.get(url, params=params)
    try:
        json_data = response.json()
        print(json_data)
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")
