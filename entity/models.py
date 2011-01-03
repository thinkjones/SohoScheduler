#from appengine_django.models import db.Model
from google.appengine.api import users
from google.appengine.ext import db
from about.models import Signup

class Entity(db.Model):
    name = db.StringProperty(required=True)
    desc = db.TextProperty(required=True)
    signup_reference = db.ReferenceProperty(Signup, collection_name='entity_signup_collection')
    is_admin = db.BooleanProperty(default=False)
    is_collaborator = db.BooleanProperty(default=False)
    is_readonly = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    is_default = db.BooleanProperty(default=False)
    active = db.BooleanProperty(default=True)
    tags = db.StringProperty(required=True)
    entity_render_type = db.IntegerProperty(required=False,  default=1)
    derived_from_entity = db.SelfReferenceProperty(collection_name='col_derived_from_entity')
    is_high_quality_template = db.BooleanProperty(default=False)
    #frevvo_application_id = db.StringProperty(required=False)
    mnemonic = db.StringProperty(required=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class EntityRating(db.Model):
	entity_reference = db.ReferenceProperty(Entity)
	entity_rating = db.IntegerProperty(required=False,  default=1)

class EntityParams(db.Model):
    entity_reference = db.ReferenceProperty(Entity)
    param_name = db.StringProperty()
    param_value = db.StringProperty()

       
class AccessRightCode(db.Model):
    mnemonic = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    desc = db.TextProperty(required=True)

class SignupEntityAccess(db.Model):
    signup_user = db.UserProperty()
    signup_reference = db.ReferenceProperty(Signup, collection_name='sea_signup_collection')
    entity_reference = db.ReferenceProperty(Entity, collection_name='col_sea_entity_reference')
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    access_right_code = db.ReferenceProperty(AccessRightCode,required=True,collection_name='sea_access_right_code')
    active = db.BooleanProperty(default=False)

class InviteEntityAccess(db.Model):
    host_signup_reference = db.ReferenceProperty(Signup, collection_name='hsr_signup_collection')
    invite_email_address = db.EmailProperty(required=True)
    invite_signup_reference = db.ReferenceProperty(Signup, collection_name='isr_signup_collection')
    entity_reference = db.ReferenceProperty(Entity, collection_name='iea_entity_reference')
    invite_sent = db.DateTimeProperty(auto_now_add=True)
    invite_accepted = db.DateTimeProperty(auto_now_add=False)
    access_right_code = db.ReferenceProperty(AccessRightCode,required=True,collection_name='iea_access_right_code')
    active = db.BooleanProperty(default=False)
