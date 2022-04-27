import requests

city_name = "imola"
api_key = "3826404e59d836a2e70391671feabcd1"

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    print(response['weather'][0]['description'])
    print(response['weather'][0]['main'])
    print(response['main']['temp'] - 273.15)
    print(response['main']['humidity'])
    print(response['wind'])

weather = get_weather(api_key, city_name)
