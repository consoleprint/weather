import requests
def getIp():
    ip_info = requests.get('https://ipinfo.io/72.229.28.185/json').json()
    return {
        'a':1
    }
print(getIp()['a'])

# lat_long = ip_info['loc'].split(',')
# print(lat_long[0])
# print(lat_long[1])
