from flask import Flask, request, url_for, render_template, redirect, g
from flask.ext.login import LoginManager, current_user, login_user, logout_user 
from flask.ext import restful
 
from mongoengine import *
from models import * 

from venmo_auth import LoginRedirect, OAuthAuthorized

# from facebook_auth import FacebookAuthorized, FacebookLogin

import twilio.twiml
import json 		
import os

 
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key= "1234123512341"
api = restful.Api(app)

#for heroku
if 'PORT' in os.environ: 
    print os.environ
    import re
    from mongoengine import connect

    regex = re.compile(r'^mongodb\:\/\/(?P<username>[_\w]+):(?P<password>[\w]+)@(?P<host>[\.\w]+):(?P<port>\d+)/(?P<database>[_\w]+)$')

    # grab the MONGOLAB_URI
    mongolab_url = os.environ['MONGOLAB_URI']

    # get our match
    match = regex.search(mongolab_url)
    data = match.groupdict()

    # now connect
    connect(data['database'], host=data['host'], port=int(data['port']), username=data['username'], password=data['password'])

else:
    # not heroku (dev env)
    # connect to mongo
    connect('relay')

    # log to stderr
    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    log.addHandler(file_handler)
    app.logger.addHandler(file_handler)

@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()
 
@app.route("/api/text", methods=["GET", "POST"])
def index():
    """Respond to incoming calls with a simple text message."""
    body_response = request.values.get('Body')
    resp = twilio.twiml.Response()
    resp.message("Hello World")
    return str(resp)

@app.route("/")
def serve_home():
    if not current_user.is_authenticated():
        return render_template("login.html")
    else:
    	print current_user.user_accounts
        return render_template("index.html", user=current_user)

# Testing apps.html
@app.route("/apps")
def serve_apps():
    return render_template("apps.html")

@app.route("/register")
def serve_register(): 
	return render_template("register.html")

@app.route("/login")
def serve_login(): 
	return render_template("login.html")

@app.route("/logout")
def serve_logout(): 
    logout_user()
    return render_template("login.html")

class RegisterUser(restful.Resource):
    def post(self): 
        if User.objects(phone_number=request.form["phone"]): #checks if username is taken
            return redirect("/register")
        user= User(phone_number=request.form["phone"], password=request.form["password"])
        user.save()
        login_user(user)
        return redirect("/")

api.add_resource(RegisterUser, "/api/register")

class ValidateLogin(restful.Resource):
    def post(self):
        user= User.objects(phone_number=request.form["phone"], password=request.form["password"])
        g.user = current_user
        if user:
            login_user(user.first(), remember=True)
            return redirect("/apps")
        error=json.dumps({"error": "Phone and password combination is not correct."})
        return redirect(url_for("serve_home", error=error))

api.add_resource(ValidateLogin, "/api/login")

#add venmo auth endpoints 
api.add_resource(LoginRedirect, '/api/auth/venmo/login')
api.add_resource(OAuthAuthorized, '/oauth-authorized')



if __name__ == "__main__":
    app.run(debug=True)