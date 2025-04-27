import requests

def get_windsolar(lat, lon):
    url = "https://mosdac.gov.in/apienergy/solar"

    params = {
        "lat": lat,
        "lon": lon
    }
    response = requests.get(url, params=params)
    try:
        json_data = response.json()
        print(json_data) 
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")