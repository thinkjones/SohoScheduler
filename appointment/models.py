#from appengine_django.models import db.Model
from appcode.datehelper import *
from google.appengine.ext import db
from appcode.sohodatamodels import *
from crm.models import *
from designer.models import *
import datetime

class Appointment(db.Model):
    name = db.StringProperty(required=False)
    booking_date = db.DateProperty()
    booking_time = db.StringProperty(required=False)
    crm_reference = db.ReferenceProperty(CRM, required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    entity_reference = db.ReferenceProperty(Entity, collection_name='col_appoint_entity_reference')
    active = db.BooleanProperty(default=True)
    form_submission_ref = db.ReferenceProperty(FormSubmission, collection_name='col_appoint_form_submission_ref')
    date_from = db.DateProperty(required=False)
    time_from = db.TimeProperty(required=False)
    date_to = db.DateProperty(required=False)
    time_to = db.TimeProperty(required=False)



