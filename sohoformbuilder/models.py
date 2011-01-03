#from appengine_django.models import db.Model
from google.appengine.ext import db

class SohoFormBuilder(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    tags = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    form_design_dict = db.TextProperty()

    def __str__(self):
        return self.name
