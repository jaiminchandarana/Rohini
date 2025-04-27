import requests

def get_weather(lat, lon):
    url = f"https://mosdac.gov.in/apiweather1/weather?lon={lon}&lat={lat}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)
            return weather_data
        else:
            print("Unable to fetch weather data")
    except Exception as e:
        print("Unable to fetch weather data")
