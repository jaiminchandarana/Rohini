from CityWeather import get_weather_data 
from nlp import tokenize 

def get_data(query):
    words = tokenize(query)
    print(f"Tokenized query: {words}")

    for word in words:
        try:
            result = get_weather_data(word)
            print(f"Found weather data for '{word}': {result}")
            return result
        except Exception as e:
            continue
    
    return None

if __name__ == "__main__":
    query = input("Enter query: ")
    weather_data = get_data(query)
    if weather_data:
        print(f"Final result: {weather_data}")
    else:
        print("Couldn’t fetch weather data for any city in the query.")