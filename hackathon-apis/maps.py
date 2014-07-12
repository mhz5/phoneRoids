from gmaps import Geocoding
from gmaps import Directions
import pprint

direct = Directions()
api = Geocoding()


def getDirections(start, end):
	direct = Directions()
	response = direct.directions(start, end)
	pprint.pprint(response, indent=2)
	return response

response = getDirections("4790 Canberra Court, San Jose, CA", "Hollingsworth Drive, Mountain View, CA")

instructionsList = response[0]['legs'][0]['steps']

#for (insn in instructionsList):

