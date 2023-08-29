import requests
r = requests.get('https://api.weather.gov/gridpoints/TOP/31,80/forecast').json()

time = r['properties']['updated']
temp = r['properties']['periods'][0]['temperature']
wind_speed = r['properties']['periods'][0]['windSpeed']
short_forecast = r['properties']['periods'][0]['shortForecast']
icon = r['properties']['periods'][0]['icon']
print(time)
print(temp)
print(wind_speed)
print(short_forecast)
print(icon)