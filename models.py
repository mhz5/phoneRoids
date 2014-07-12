from mongoengine import *

class Address(Document):
	label = StringField(required=True, unique=True)
	location = StringField()

class AccessToken(Document):
	api = StringField(required=True)
	access_token = StringField(required=True)

class Query(Document):
	content = StringField()

class User(Document):
	phone_number = StringField(required=True, unique=True)
	password = StringField(required=True, max_length=50)
	addresses = ListField(ReferenceField(Address))
	queries = ListField(ReferenceField(Query))
	access_tokens = ListField(ReferenceField(AccessToken))

	def is_authenticated(self):
		return True
	def is_active(self):
		return True

	def is_anonymous(self):
		return False
		
	def get_id(self):
		return unicode(self.id)


