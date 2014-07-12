from flask import Flask, redirect, url_for, session, request
from flask_oauth import OAuth


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '1439095869700422'
FACEBOOK_APP_SECRET = '0983344c31d05351eec039a9486dbe62'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


class FacebookLogin(): 
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@facebook.authorized_handler
class FacebookAuthorized(restful.Resource): 
	def get(self):
	    if resp is None:
	        return 'Access denied: reason=%s error=%s' % (
	            request.args['error_reason'],
	            request.args['error_description']
	        )
	    session['oauth_token'] = (resp['access_token'], '')
	    me = facebook.get('/me')
	    return 'Logged in as id=%s name=%s redirect=%s' % \
	        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()