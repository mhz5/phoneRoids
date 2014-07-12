from flask.ext.login import current_user

from models import User, BrainState
import HackathonAPI.yelp as yelp_api
import Parser.parser as parser
import venmo_controller as venmo_api
import HackathonAPI.maps as maps_api
import json

#brain states. The most recent state should be saved to the database.
NULL_STATE = "null_state"
YELP_STATE_ONE = "yelp_1"
YELP_STATE_TWO = "yelp_2"


def processRequest(request, phone_number):
	texting_user = User.objects(phone_number=str(phone_number)).first()
	if texting_user.brain_state is not None:
		old_state = texting_user.brain_state.state
		print "Old State: " + old_state
		argJson = texting_user.brain_state.args
		if argJson:
			argReload = json.loads(argJson)
	else:
		print "Brain state none"
		state = "None"
	
	(app, argDict, state) = parser.parseRequest(request, old_state)
	print 'state %s' % state
	argJson = json.dumps(argDict,  separators=(',',':'))
	
	new_brain_state = BrainState(state = state, args = argJson)

	new_brain_state.save()
	texting_user.brain_state = new_brain_state
	texting_user.save()
	print 'hits after texting'
	
	print argDict
	print app
	if app == "venmo":	
		response = venmo_api.make_payment(user = texting_user, phone = argDict.get("to")  , amount = argDict.get("pay"), note = argDict.get("for"))
	elif app == "maps":
		startLoc = argDict.get("from")
		endLoc = argDict.get("to")
		storedLoc = texting_user.get_address_by_label(endLoc)
		if storedLoc:
			endLoc = storedLoc
		response = map_api.query(startLoc = startLoc, endLoc = endLoc)
		
	elif app == "yelp":
		if old_state == "yelp_1" and argDict.get("choice"):
			index = argDict.get("choice") 
			response = yelp_api.verbose(location = argReload.get("location"), index = index , radius = argReload.get("distance", "50"), category = argReload.get("category", "restaurants"))
			pieces = response.split("|")
			texting_user.set_address(index, pieces[1])
		else:
			response = yelp_api.query(location = argDict.get("location"), radius = argDict.get("distance", "50"), category = argDict.get("category", "restaurants"))

	elif app == "error":
		response = argDict.get("error")
	print response
	return response




