from flask.ext.login import current_user

from models import User, BrainState
import HackathonAPI.yelp as yelp_api
import Parser.parser as parser

#brain states. The most recent state should be saved to the database.
NULL_STATE = "null_state"
YELP_STATE_ONE = "yelp_1"
YELP_STATE_TWO = "yelp_2"


def processRequest(request):
	print request
	(app, argDict) = parser.parseRequest(request)
	state = YELP_STATE_ONE
	new_brain_state= BrainState(state=state)
	new_brain_state.save()
	current_user.brain_state=new_brain_state
	current_user.save()
	print yelp_api.main(location = argDict.get("location"), radius = argDict.get("distance", "50"), category = argDict.get("category", "restaurants"))



