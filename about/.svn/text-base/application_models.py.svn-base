
#from appengine_django.models import db.Model
from google.appengine.ext import db
import datetime
import appcode
from about.models import *
from entity.models import *

class StoredToken(db.Model):
        purpose = db.StringProperty(required=True,default="GoogleContacts")
        token_string = db.StringProperty(required=True)
        signup_reference = db.ReferenceProperty(Signup, collection_name='st_signup_collection')
        entity_reference = db.ReferenceProperty(Entity, collection_name='st_appoint_entity_reference')
        created = db.DateTimeProperty(auto_now_add=True)
        modified = db.DateTimeProperty(auto_now=True)
        active = db.BooleanProperty(default=True)
        is_shared = db.BooleanProperty(default=False)

	def __str__(self):
		return self.token_string