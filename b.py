import requests
def getLocation(ip):
    r = requests.get('https://ipinfo.io/{ip}/json'.format(ip=ip)).json()
    return {
        'city': r['city'],
        'loc': r['loc']
    }
print(getLocation('65.63.255.255'))