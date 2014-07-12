from gmaps import Geocoding
from gmaps import Directions
import pprint
import re

direct = Directions()

TAG_RE = re.compile(r'<[^>]+>')
startLoc = '4790 Canberra Court, San Jose, CA'
endLoc = '820 E El Camino Real, Mountain View, CA'
token = '\n'

def remove_tags(text):
    return TAG_RE.sub('', text)

def getDirections(start, end):
	direct = Directions()
	response = direct.directions(start, end)
	#pprint.pprint(response, indent=2)
	return response

def getDistance(start, end):
	response = getDirections(start, end)
	return str(response[0]['legs'][0]['distance']['text'])

def main(startLoc, endLoc):
	response = getDirections(startLoc, endLoc)
	instructionsList = response[0]['legs'][0]['steps']

	output = 'Directions to ' + endLoc + token
	counter = 0


	for insn in instructionsList:
		counter += 1
		cur_insn = remove_tags(insn['html_instructions'])
		cur_dist = insn['distance']['text']
		output += str(counter) + '. ' + cur_insn + " | " + cur_dist + token
		#print cur_insn + " | " + cur_dist

	print
	print '---- Output -----'
	print output
	print '-----------------'

#main(startLoc, endLoc)