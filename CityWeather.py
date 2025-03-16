import requests

def get_cord(word):
    city = word

    headers = {
        "User-Agent": "YourAppName/1.0 (jdchandarana3@gmail.com)"
    }

    url = f"https://nominatim.openstreetmap.org/search?city={city}&country=India&format=json"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                print(f"{city}: Latitude = {lat}, Longitude = {lon}")
                return lat,lon
            else:
                print(f"No data found for given {city}")
        else:
            print(f"Error fetching data for {city}")
    except Exception as e:
        print(f"Error fetching data for {city}")

def get_weather(lat, lon):
    url = f"https://mosdac.gov.in/apiweather1/weather?lon={lon}&lat={lat}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print("Weather Data:")
            print(weather_data)
            return weather_data
        else:
            print("Unable to fetch weather data")
    except Exception as e:
        print("Unable to fetch weather data")

def get_weather_data(word):
    latitude,longitude = get_cord(word)
    data = get_weather(latitude, longitude)
    return data