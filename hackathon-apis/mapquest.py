#!/usr/bin/env python

# MapQuest API Turn-by-turn script
#
# Generates driving directions from a starting location
# to a series of destinations in a CSV, used to print
# maps for volunteers delivering food to the less-fortunate
#
# CSV format - place in a file named `list.csv`
# Name, Street, Zipcode, Phone, Count
#
# Generates two output folders:
#   maps/ : Printer-friendly HTML directions with turn-by-turn images
#   static/ : Images used in the maps
# 
# Requirements: Python 2.5+ and jinja2

import os, json
from urllib import urlopen, quote
from jinja2 import Template

API_KEY = 'YOUR_API_KEY' #Get one at http://developer.mapquest.com/, it's free
STARTING_ADDR = 'YOUR_STARTING_ADDR'
URL = 'http://www.mapquestapi.com/directions/v1/route?key=%s&from=%s&to=%s'

template = Template("""
<html>
  <h2>YOUR_TITLE_MESSAGE</h2>
  <p>{{ name }} - Family of {{ count }} - Phone: {{ phone }}</p>
  <p>Trip to <b>{{ full_addr }}</b></p>
  <p>{{ distance }} miles - about {{ time }} minutes</p>
  <h3>Starting from YOUR_STARTING_ADDR</h3>
  <table border='1'>
    <tbody>
      {% for step in steps %}
      <tr>
        <td>{{ step.text }}</td><td><img src="{{ step.img }}"/></td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <h3>Arrived at {{ full_addr }}</h3>
</html>""")

class Step(object):
    pass

def download_static_map(img_url, filename):
    file_path = os.path.join('static', filename)
    downloaded_image = file(file_path, "wb")

    image_on_web = urlopen(img_url)
    while True:
        buf = image_on_web.read(65536)
        if len(buf) == 0:
            break
        downloaded_image.write(buf)
    downloaded_image.close()
    image_on_web.close()

print "Reading list.csv..."
with open('list.csv') as fp:
    lines = fp.readlines()

lines = [l.strip() for l in lines]
items = [l.split(', ') for l in lines]

print "Starting..."
for item in items:
    addr = ' '.join(item[1:3])
    data = urlopen(URL % (API_KEY, quote(STARTING_ADDR), quote(addr))).read()
    directions = json.loads(data)
    print 'Fetching directions for:', item[0],
    distance = directions['route']['distance']
    time= float(directions['route']['time']) / 60
    
    maneuvers = directions['route']['legs'][0]['maneuvers']
    steps = []
    for leg in maneuvers:
        x = Step()
        x.text = '%s) %s' %(leg['index'] + 1, leg['narrative'])
        x.img = ""
        filename = item[0].lower().replace(' ', '-') + '-' + str(leg['index'])
        if 'mapUrl' in leg:
            x.img = os.path.join('../static', filename)
            download_static_map(leg['mapUrl'], filename + '.jpg')
        steps.append(x)
    full_addr = '%s, %s %s, %s' % (item[1], directions['route']['locations'][1]['adminArea5'], \
                                    directions['route']['locations'][1]['adminArea3'], item[2])

    out = template.render(name = item[0], count = item[4], full_addr = full_addr, phone = item[3], \
                          distance = round(distance, 2), time = round(time), steps = steps)

    with open(os.path.join('maps', filename + '.html'), 'w') as fp:
        fp.write(out)

print "Finished. Check the maps/ directory for the generated files"