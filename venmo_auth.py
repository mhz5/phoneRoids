from flask import Flask, redirect, session, request, url_for, render_template
from flask.ext import restful
from flask import g
from flask.ext.login import current_user
from urllib import urlencode
from venmo_secrets import CLIENT_ID, CLIENT_SECRET, APP_SECRET
from models import UserAccount

 
import requests
 
app = Flask(__name__)
api = restful.Api(app)
 
app.secret_key= APP_SECRET

app.config["REMEMBER_COOKIE_DOMAIN"] = ".localhost:5000"

class OAuthAuthorized(restful.Resource):
    def get(self):
        """
        You can use request.args to get URL arguments from a url. Another name for URL arguments
        is a query string.
        What is a URL argument? It"s some data that is appended to the end of a url after a "?"
        that can give extra context or information.
      
        """
        AUTHORIZATION_CODE = request.args.get("code")
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code" : AUTHORIZATION_CODE
            }
        url = "https://api.venmo.com/v1/oauth/access_token"
        response = requests.post(url, data)
        response_dict = response.json()
        access_token = response_dict.get("access_token")
        user = response_dict.get("user")
        print(user["id"])
        user_account = UserAccount(user=user["id"], access_token=access_token, api="venmo")
        user_account.save()
        for current_user_account in current_user.user_accounts:
            if current_user_account.api == "venmo":
                return redirect("/apps")
        current_user.user_accounts.append(user_account)
        current_user.save()
        session["venmo_token"] = access_token
        return redirect("/apps")
  
class LoginRedirect(restful.Resource):
    def get(self):
        data = {
            "client_id": CLIENT_ID, 
            "scope" : "access_friends make_payments", 
            "response_type" : "code"}
        return redirect("https://api.venmo.com/v1/oauth/authorize?%s" % urlencode(data))
  
