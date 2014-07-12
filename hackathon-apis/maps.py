from gmaps import Geocoding
from gmaps import Directions
import pprint
import re

direct = Directions()
api = Geocoding()

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def getDirections(start, end):
	direct = Directions()
	response = direct.directions(start, end)
	pprint.pprint(response, indent=2)
	return response

response = getDirections("4790 Canberra Court, San Jose, CA", "820 E El Camino Real, Mountain View, CA")
instructionsList = response[0]['legs'][0]['steps']

output = ''
counter = 0
for insn in instructionsList:
	counter += 1
	cur_insn = remove_tags(insn['html_instructions'])
	cur_dist = insn['distance']['text']
	output += str(counter) + '. ' + cur_insn + " | " + cur_dist + ' --- '
	#print cur_insn + " | " + cur_dist








print
print '---- Output -----'
print output
print '-----------------'
