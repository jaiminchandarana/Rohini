import requests
from pyproj import Transformer
from GetCordinate import get_cord

def get_soilmoisture(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)

    url = "https://mosdac.gov.in/geoserver_2/soil_wetness/wms"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.1.1",
        "REQUEST": "GetFeatureInfo",
        "FORMAT": "image/png",
        "TRANSPARENT": "true",
        "QUERY_LAYERS": "soil_wetness:soil_moisture",
        "LAYERS": "soil_wetness:soil_moisture",
        "STYLES": "",
        "INFO_FORMAT": "application/json",
        "X": 84,
        "Y": 51,
        "WIDTH": 256,
        "HEIGHT": 256,
        "SRS": "EPSG:4326",
        "BBOX": "78.75,11.25,90,22.5"
    }


    response = requests.get(url, params=params)
    try:
        json_data = response.json()
        print(json_data)
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")
        
if __name__ == "__main__":
    get_soilmoisture(22.5726459,88.3638953)