import requests
def getTemp():
    r = requests.get('https://api.weather.gov/gridpoints/TOP/31,80/forecast').json()
    day_temp = r['properties']['periods'][0]
    return {
        'temperature': day_temp['temperature'],
        'wind_speed': day_temp['windSpeed'],
        'short_forecast': day_temp['shortForecast'],
        'icon': day_temp['icon']
    }
print(getTemp())