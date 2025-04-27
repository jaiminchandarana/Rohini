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