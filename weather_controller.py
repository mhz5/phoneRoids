import requests


# print requests.post("http://api.wunderground.com/api/323703917f969e14/forecast/q/CA/San_Francisco.json").json()["forecast"]
print requests.post("http://api.wunderground.com/api/323703917f969e14/forecast/q/CA/San_Francisco.json").json()["forecast"]["txt_forecast"]["forecastday"][0]["icon_url"]
print requests.post("http://api.wunderground.com/api/323703917f969e14/forecast/q/CA/San_Francisco.json").json()["forecast"]["txt_forecast"]["forecastday"][0]["fcttext"]
