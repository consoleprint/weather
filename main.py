from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

def get_temp(forecast_url):
    r = requests.get(forecast_url).json()
    day_temp = r['properties']['periods'][0]
    return {
        'temperature': day_temp['temperature'],
        'wind_speed': day_temp['windSpeed'],
        'short_forecast': day_temp['shortForecast'],
        'icon': day_temp['icon']
    }

def getLocation(ip):
    r = requests.get('https://ipinfo.io/{ip}/json'.format(ip=ip)).json()
    return {
        'city': r['city'],
        'loc': r['loc']
    }
def getGrid(loc):
    r = requests.get('https://api.weather.gov/points/{loc}'.format(loc=loc)).json()
    return r['properties']['forecast']

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    client_host = request.client.host
    client_host = '65.63.255.255' # TODO remove it
    location = getLocation(client_host)
    forecast_url = getGrid(location['loc'])
    temp = get_temp(forecast_url)
    pre_pos = '20'
    html_content = """
    <html>
        <head>
            <title>Weather</title>
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
              <h6>15:07</h6>
            </div>

            <div class="d-flex flex-column text-center mt-5 mb-4">
              <h6 class="display-4 mb-0 font-weight-bold" style="color: #1C2331;"> {temperature}°F </h6>
              <span class="small" style="color: #868B94">{short_forecast}</span>
            </div>

            <div class="d-flex align-items-center">
              <div class="flex-grow-1" style="font-size: 1rem;">
                <div><i class="fas fa-wind fa-fw" style="color: #868B94;"></i> <span class="ms-1"> {wind_speed}
                  </span></div>
                <div><i class="fas fa-tint fa-fw" style="color: #868B94;"></i> <span class="ms-1"> {pre_pos}% </span>
                </div>
                <div><i class="fas fa-sun fa-fw" style="color: #868B94;"></i> <span class="ms-1"> 0.2h </span>
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
    """.format(temperature=temp['temperature'], wind_speed=temp['wind_speed'],
                city=location['city'], pre_pos=pre_pos, icon=temp['icon'], short_forecast=temp['short_forecast'] )
    return HTMLResponse(content=html_content, status_code=200)

