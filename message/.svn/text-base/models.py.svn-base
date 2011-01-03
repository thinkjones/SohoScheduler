#from appengine_django.models import db.Model
from google.appengine.ext import db
from google.appengine.api import users
from appcode.sohodatamodels import *
import datetime
import time

#These are the messages to be shown
class Message(db.Model):
	message_mnemonic = db.StringProperty()
	message_title = db.StringProperty()
	message_description = db.TextProperty()
	message_class = db.StringProperty()
	message_href = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)
	tab_name = db.StringProperty()
	show_now = db.BooleanProperty(default=True)
	active = db.BooleanProperty(default=True)


# The user will only ever see the message if it is in this table.
# Messages are placed in this table via an admin routine, or service once
# Google releases that code.
# There is duplicate information in here because we can't use joins
class UserMessage(db.Model):
	owner = db.UserProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	message_title = db.StringProperty()
	message_description = db.TextProperty()
	message_class = db.StringProperty()
	message_href = db.StringProperty()
	tab_name = db.StringProperty()
	message_reference = db.ReferenceProperty(Message, collection_name ="col_message_reference")
	user_has_seen = db.BooleanProperty(default=False)
	user_read_date = db.DateTimeProperty(auto_now_add=True)