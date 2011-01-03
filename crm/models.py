#from appengine_django.models import db.Model
from google.appengine.api import users
from google.appengine.ext import db
from about.models import Signup
from entity.models import Entity
from designer.models import FormSubmission
from about.application_models import *


class CRM(db.Model):
    name = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    entity_reference = db.ReferenceProperty(Entity, collection_name='col_crm_entity_reference')
    active = db.BooleanProperty(default=True)
    form_submission_ref = db.ReferenceProperty(FormSubmission, collection_name='col_crm_form_submission_ref')
    external_system_id = db.StringProperty(required=False)
    stored_token_ref = db.ReferenceProperty(StoredToken, collection_name='col_crm_stored_token_ref')

    def __str__(self):
        return self.name
