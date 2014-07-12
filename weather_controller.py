import requests


print requests.post("http://api.wunderground.com/api/323703917f969e14/forecast/q/CA/San_Francisco.json").json()