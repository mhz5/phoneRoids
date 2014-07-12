import requests
import HackathonAPI.maps as maps_api

def get_weather(address): 
 return requests.post(("http://api.wunderground.com/api/323703917f969e14/forecast/q/%s/%s.json")% (map_api.getState(address),maps_api.getCity(address))).json()["forecast"]["txt_forecast"]["forecastday"][0]['fcttext']
