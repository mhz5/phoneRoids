from mongoengine import *

class BrainState(Document):
	state = StringField()

class Address(Document):
	label = StringField(required=True, unique=True)
	location = StringField()

class UserAccount(Document):
	api = StringField(required=True)
	access_token = StringField(required=True)
	username = StringField()

class Query(Document):
	content = StringField()

class User(Document):
	phone_number = StringField(required=True, unique=True)
	password = StringField(required=True, max_length=50)
	addresses = ListField(ReferenceField(Address))
	default_address = ReferenceField(Address)
	queries = ListField(ReferenceField(Query))
	user_accounts = ListField(ReferenceField(UserAccount))
	brain_state = ReferenceField(BrainState)

	def is_authenticated(self):
		return True
	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def set_address(self, label, location):
		address_already_added = False
		for address in Address.objects(label=label):
			if address in self.addresses:
				address.location = location
				address.save()
				address_already_added = True
		if not address_already_added:
			new_address = Address(label=label, location=location)
			new_address.save()
			self.addresses.append(new_address)
			self.save()

	def get_address_by_label(self, label):
		for address in self.addresses:
			if address.label == label:
				return address
		return None 

	def get_id(self):
		return unicode(self.id)


