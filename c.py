import requests
def getGrid(loc):
    r = requests.get('https://api.weather.gov/points/{loc}'.format(loc=loc)).json()
    return r['properties']['forecast']
print(getGrid('39.7456,-97.0892'))