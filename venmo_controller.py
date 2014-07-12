import requests
from models import * 

def make_payment(user, phone, amount, note):
	for user_account in user.user_accounts:
		if user_account.api=="venmo":
			data = {
			"access_token": user_account.access_token, 
			"phone": phone,
			"note" : note, 
			"amount" : amount
			}
			requests.post('https://api.venmo.com/v1/payments', data=data)	
