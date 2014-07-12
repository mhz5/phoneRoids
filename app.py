from flask import Flask, request, url_for, render_template, redirect
from flask.ext.login import LoginManager, current_user, login_user, logout_user 
from flask.ext import restful
 
from mongoengine import *
from models import * 

from venmo_auth import LoginRedirect, OAuthAuthorized

# from facebook_auth import FacebookAuthorized, FacebookLogin

import twilio.twiml
import json 
import brain		

connect("relay")
 
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key= "1234123512341"
api = restful.Api(app)

@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()
 
@app.route("/api/v1/text", methods=["GET", "POST"])
def index():
    """Respond to incoming calls with a simple text message."""
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

@app.route("/request")
def sampleRequest():
    # here we want to get the value of user (i.e. ?query=some-value)
    query = request.args.get('query')
    brain.processRequest(query)

class RegisterUser(restful.Resource):
    def post(self): 
        if User.objects(phone_number=request.form["phone"]): #checks if username is taken
            return redirect("/register.html")
        user= User(phone_number=request.form["phone"], password=request.form["password"])
        user.save()
        login_user(user)
        return redirect("/")

api.add_resource(RegisterUser, "/api/register")

class ValidateLogin(restful.Resource):
    def post(self):
        user= User.objects(phone_number=request.form["phone"], password=request.form["password"])
        if user:
            login_user(user.first(), remember=True)
            return redirect("/")
        error=json.dumps({"error": "Phone and password combination is not correct."})
        return redirect(url_for("serve_home", error=error))

api.add_resource(ValidateLogin, "/api/login")

#add venmo auth endpoints 
api.add_resource(LoginRedirect, '/api/auth/venmo/login')
api.add_resource(OAuthAuthorized, '/oauth-authorized')



if __name__ == "__main__":
    app.run(debug=True)