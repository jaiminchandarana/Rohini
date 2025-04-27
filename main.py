from CityWeather import get_weather
from nlp import tokenize 
from GetCordinate import get_cord
from HeatWave import get_heatwave
from ColdWave import get_coldwave
from Lightning import get_lightning
from Monsoon import get_monsoon
from RainFall import get_rainfall
from soilMoisture import get_soilmoisture
from Windsolar import get_windsolar
import json

def get_data(query):
    words = tokenize(query)
    print(f"Tokenized query: {words}")

    for word in words:
        try:
            lat,lon = get_cord(word)
            return lat,lon
        except Exception as e:
            continue
    
    return None

def data():
    query = input("Enter query: ")
    lat,lon = get_data(query)
    weather_data = get_weather(lat,lon)
    heatwave_data = get_heatwave(lat,lon)
    coldwave_data = get_coldwave(lat,lon)
    lightning_data = get_lightning(lat,lon)
    monsoon_data = get_monsoon(lat,lon)
    rainfall_data = get_rainfall(lat,lon)
    soilmoisture_data = get_soilmoisture(lat,lon)
    windsolar_data = get_windsolar(lat,lon)
    merged_data = {
        "coldwave_forecast" : coldwave_data,
        "weather_forecast" : weather_data,
        "heatwave_forecast" : heatwave_data,
        "lightning_forecast" : lightning_data,
        "monsoon_forecast" : monsoon_data,
        "rainfall_forecase" : rainfall_data,
        "soilmoisture_forecast" : soilmoisture_data,
        "wind&solar_forecase" : windsolar_data
    }
    output_file = "merged_data.json"
    with open(output_file, "w") as file:
        json.dump(merged_data, file, indent=4)
        return query
    try:
        print(f"{weather_data} \n {heatwave_data} \n {coldwave_data} \n {lightning_data} \n {monsoon_data} \n {rainfall_data} \n {soilmoisture_data} \n {windsolar_data}")
        return query
    except:
        print("Couldn’t fetch weather data for any city in the query.")
        return query