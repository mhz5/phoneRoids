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
	state = texting_user.brain_state.state
	print texting_user.brain_state.args
	(app, argDict, state) = parser.parseRequest(request)
	print 'state %s' % state
	argJson = json.dumps(argDict,  separators=(',',':'))
	argReload = json.loads(argJson)
	print argJson
	print argReload
	new_brain_state = BrainState(state = state, args = argJson)
	new_brain_state.save()
	
	print 'hits after texting'
	# texting_user.brain_state = new_brain_state
	# texting_user.save()
	print argDict
	print app
	if app == "venmo":
		response = venmo_api.make_payment(user = texting_user, phone = argDict.get("to")  , amount = argDict.get("pay"), note = argDict.get("for"))
	elif app == "maps":
		response = maps_api.query(startLoc = argDict.get("from"), endLoc = argDict.get("to"))
	elif app == "yelp":
		response = yelp_api.query(location = argDict.get("location"), radius = argDict.get("distance", "50"), category = argDict.get("category", "restaurants"))
	elif app == "error":
		response = argDict.get("error")
	print response
	return response



