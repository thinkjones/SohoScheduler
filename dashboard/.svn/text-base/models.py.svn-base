#from appengine_django.models import db.Model
from google.appengine.ext import db
from google.appengine.api import users
from appcode.sohodatamodels import *
import appcode
import appcode.baseserver
import datetime
import time

#These are the messages to be shown
class Dashboard(db.Model):
    signup_reference = db.ReferenceProperty(Signup, collection_name='dashboard_signup_Collection')
    last_refreshed = db.DateTimeProperty(auto_now_add=True)
    refresh_activity_type = db.IntegerProperty(default=0)
    requires_refresh = db.BooleanProperty(default=True)


class DashboardRecentActivity(db.Model):
    signup_reference = db.ReferenceProperty(Signup, required=False, collection_name='dashboard_recent_activity_signup_Collection')
    signup_user = db.UserProperty()
    user_email = db.EmailProperty(required=False)
    application_zone = db.StringProperty(required=False)
    action_name = db.StringProperty(required=False)
    action_url = db.StringProperty(required=False)
    entity_id = db.StringProperty(required=False)
    param_1 = db.StringProperty(required=False)
    param_2 = db.StringProperty(required=False)
    param_3 = db.StringProperty(required=False)
    activity_date = db.DateTimeProperty(auto_now_add=True)
    activity_text = db.StringProperty()
    show_to_user = db.BooleanProperty(default=False)
    stats_processed = db.BooleanProperty(default=False)
    

class DashboardRecentActivitySummary(db.Model):
    signup_reference = db.ReferenceProperty(Signup, collection_name='dashboard_recent_activity_summary_signup_Collection')
    application_zone = db.StringProperty(required=False)
    action_name = db.StringProperty(required=False)
    total_count = db.IntegerProperty(default=0)
