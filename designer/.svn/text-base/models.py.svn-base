#from appengine_django.models import db.Model
from google.appengine.ext import db
from google.appengine.api import users
from appcode.baseserver import *

from django.core import serializers
from entity.models import *
from sohoformbuilder.models import *

import re

"""
	Class to handle entity's forms. These are instances of templates
"""
class FormDesign(db.Model):
    formType = db.IntegerProperty() #this can be ReservationCalendar or Customer
    xhtmlCode = db.TextProperty() #the xhtml/xml code to be used on rendering
    formatCode = db.TextProperty() #the format code - css for example
    behaviorCode = db.TextProperty() # the behavior code - js for example
    fieldsJSON = db.TextProperty() #json with fields
    entity_reference = db.ReferenceProperty(Entity, collection_name='col_fd_entity_reference') #the entity that uses this form
    is_default = db.BooleanProperty()
    creator = db.UserProperty() #the creator of this template
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    sohoformbuilder_reference = db.ReferenceProperty(SohoFormBuilder, collection_name='col_fd_sohoformbuilder_reference')
    active = db.BooleanProperty(default=True)

    def __str__(self):
        return self.formType

    def fieldsDict(self):
        #return json.loads( self.fieldsJSON )
        #GCJ Use Django Serialization deserialization
        data = serializers.deserialize('json', self.fieldsJSON)
        return data

    def isFieldRequired(self, fieldName):
        return self.fieldsDict[fieldName]['required']


class FormDesignField(db.Model):
    field_name = db.StringProperty(required=True)
    field_display_name = db.StringProperty(required=True)
    control_id = db.StringProperty()
    control_type = db.StringProperty()
    display_type = db.StringProperty()
    formdesign_reference = db.ReferenceProperty(FormDesign, collection_name='col_fdf_formdesign_reference') #the entity that uses this form
    is_active = db.BooleanProperty()

    def __str__(self):
        return self.field_name
    
    
#TODO: this may be an Expando object, we haven't used it in order to as independent as possible from GAE    
class FormSubmission(db.Model):
    entity_ref = db.ReferenceProperty(Entity, collection_name='col_fs_entity_ref') #reference to ReservationCalendar or Customer
    formType = db.IntegerProperty()
    pkid = db.IntegerProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    submitted = db.DateTimeProperty(required=False)
    signup_reference = db.ReferenceProperty(Signup,collection_name='col_fs_signup_ref')
    form_submitted = db.BooleanProperty(default=False)
    formdesign_reference = db.ReferenceProperty(FormDesign, required=False, collection_name='col_fs_formdesign_reference') #the entity that uses this form


class FlexFieldValue(db.Model):
    form_submission_ref = db.ReferenceProperty(FormSubmission, collection_name='col_form_submission') #reference to ReservationCalendar or Customer
    entity_ref = db.ReferenceProperty(Entity, collection_name='col_ffv_entity_ref') #reference to ReservationCalendar or Customer
    form_design_field_ref = db.ReferenceProperty(FormDesignField, collection_name='col_form_design_field_ref')
    formType = db.IntegerProperty()
    field_name = db.StringProperty(multiline=False)
    display_name = db.StringProperty(multiline=False)
    display_type = db.StringProperty()
    value_string = db.StringProperty(required=False)
    value_text = db.TextProperty(required=False)
    value_bool = db.BooleanProperty(required=False)
    value_int = db.IntegerProperty(required=False)
    value_dec = db.FloatProperty(required=False)
    value_date = db.DateProperty(required=False)
    value_time = db.TimeProperty(required=False)
    value_datetime = db.DateTimeProperty(required=False)
    sub_field_type = db.StringProperty(required=False)


class FlexFieldValueTest(db.Model):
    ffkey = db.StringProperty(required=False)
    ffval = db.StringProperty(required=False)