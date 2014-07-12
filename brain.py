from flask.ext.login import current_user

from models import User, BrainState
import HackathonAPI.yelp as yelp_api

#brain states. The most recent state should be saved to the database.
NULL_STATE = "null_state"
YELP_STATE_ONE = "yelp_state_one"
YELP_STATE_TWO = "yelp_state_two"


def processRequest(request):
	print request
	#yelp_api.main("","","")



