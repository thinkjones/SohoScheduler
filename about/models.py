#from appengine_django.models import db.Model
from google.appengine.ext import db
import datetime

#Stage
#0 = Registered with company
#1 = Just Registered no company assigned

class Signup(db.Model):
    signup_user = db.UserProperty()
    signup_stage = db.IntegerProperty(default=1)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    application_version = db.FloatProperty(default=0.6)


class SignupExtendedProfile(db.Model):
    signup_reference = db.ReferenceProperty(Signup,collection_name='col_sea_signup_ref')
    param_type = db.StringProperty(required=True)
    param_value = db.StringProperty(required=False)
    param_date = db.DateTimeProperty(required=False)

    initial_date_value = datetime.datetime(1970, 1, 1)

    param_types = {
                                    "last_logged_in":{'param_value':None, 'param_date':initial_date_value},
                                    "activity_last_ran":{'param_value':None, 'param_date':initial_date_value},
                                    "messages_last_processed":{'param_value':None, 'param_date':initial_date_value},
                                    "has_used_designer":{'param_value':'No', 'param_date':initial_date_value},
                    }

class ContactUs(db.Model):
    signup_user = db.UserProperty()
    signup_ref = db.ReferenceProperty(Signup, collection_name='col_contact_us_signup_ref')
    created = db.DateTimeProperty(auto_now_add=True)
    http_referer = db.StringProperty(required=False)
    inquiry_type = db.StringProperty(required=False)
    inquiry_details = db.TextProperty(required=False)
