from typing import Union
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()
def getIpInfo(ip):
    return requests.get('https://ipinfo.io/{ip}/json'.format(ip=ip)).json()

def getTemp(loc):
    grid = requests.get('https://api.weather.gov/points/{loc}'.format(loc=loc)).json()
    r = requests.get(grid['properties']['forecast']).json()
    return {
        'time': datetime.fromisoformat(r['properties']['updated']).strftime("%H:%M"),
        'temp': r['properties']['periods'][0]['temperature'],
        'wind_speed': r['properties']['periods'][0]['windSpeed'],
        'short_forecast': r['properties']['periods'][0]['shortForecast'],
        'chance_of_rain': r['properties']['periods'][0]['probabilityOfPrecipitation']['value'],
        'icon': r['properties']['periods'][0]['icon']
    }

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    client_host = request.client.host
    print(client_host)
    ip_info = getIpInfo('72.229.28.185')
    r = getTemp(ip_info['loc'])
    return """
        <html>
            <head>
                <title>Some HTML in here</title>
                <!-- Font Awesome -->
<link
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
  rel="stylesheet"
/>
<!-- Google Fonts -->
<link
  href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
  rel="stylesheet"
/>
<!-- MDB -->
<link
  href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.1/mdb.min.css"
  rel="stylesheet"
/>

                <script
  type="text/javascript"
  src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.1/mdb.min.js"
></script>
            </head>
            <body>
                <section class="vh-100" style="background-color: #4B515D;">
  <div class="container py-5 h-100">

    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-md-8 col-lg-6 col-xl-4">

        <div class="card" style="color: #4B515D; border-radius: 35px;">
          <div class="card-body p-4">

            <div class="d-flex">
              <h6 class="flex-grow-1">{city}</h6>
              <h6>{time}</h6>
            </div>

            <div class="d-flex flex-column text-center mt-5 mb-4">
              <h6 class="display-4 mb-0 font-weight-bold" style="color: #1C2331;"> {temp}°F </h6>
              <span class="small" style="color: #868B94">{short_forecast}</span>
            </div>

            <div class="d-flex align-items-center">
              <div class="flex-grow-1" style="font-size: 1rem;">
                <div><i class="fas fa-wind fa-fw" style="color: #868B94;"></i> <span class="ms-1"> {wind_speed}
                  </span></div>
                <div><i class="fas fa-tint fa-fw" style="color: #868B94;"></i> <span class="ms-1"> {chance_of_rain}% </span>
                </div>
              </div>
              <div>
                <img src="{icon}"
                  width="100px">
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

  </div>
</section>
            </body>
        </html>
        """.format(wind_speed=r['wind_speed'], temp=r['temp'], short_forecast=r['short_forecast'], 
                   icon=r['icon'], time=r['time'], chance_of_rain=r['chance_of_rain'], city=ip_info['city'])

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}