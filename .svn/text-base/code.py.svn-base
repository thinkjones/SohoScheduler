from google.appengine.dist import use_library
use_library('django', "1.0")

import os,sys
#Environment Setup
os.environ["DJANGO_SETTINGS_MODULE"] = "django_settings"

os.environ['ROOT_PATH'] = os.path.dirname(__file__)
sys.path.insert(0, 'appengine_utilities.zip')
sys.path.insert(0, 'atom.zip')
sys.path.insert(0, 'gdata.zip')

#Import Django Templates
from django.conf import settings
settings._target = None

import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

from google.appengine.ext.webapp import template
from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import about.views
import dashboard.views
import entity.views
import entity.wizards
import sohoadmin.views
import designer.views
import crm.wizards
import crm.views
import appointment.views

application = webapp.WSGIApplication([
                                        (r'/',about.views.LandingPage),
                                        (r'/application/switch/(.*)/',dashboard.views.GotoNewApplication),
                                        (r'/application/docpost/',entity.views.DocPostPage),
                                        (r'/application/formpost/',entity.views.FormPostPage),
                                        (r'/application/docdesignpost/',entity.views.DocDesignPost),
                                        (r'/application/jsonrequests/',entity.views.JsonRequests),
                                        (r'/application/(.*)/settings/',designer.views.DesignerPage),


                                        (r'/application/(.*)/crm/wizard/synchwithgoogle/jsonrequests/',crm.wizards.CRMWizardPage),
                                        (r'/application/(.*)/crm/',crm.views.CRMPage),
                                        (r'/application/(.*)/appointment/',appointment.views.AppointmentPage),


                                        (r'/application/(.*)/(.*)/(.*)/(.*)/',dashboard.views.ApplicationFormHandler4),
                                        (r'/application/(.*)/(.*)/(.*)/',dashboard.views.ApplicationFormHandler3),
                                        (r'/application/(.*)/(.*)/',dashboard.views.ApplicationFormHandler2),
                                        (r'/application/(.*)/',dashboard.views.DashboardPage),



                                        (r'/newuser/',dashboard.views.NewUserPage),
                                        (r'/newentitywizard/jsonrequests/',entity.wizards.JsonRequests),
                                        (r'/newentitywizard/(.*)/',entity.wizards.NewEntityWizard),
                                        (r'/newentitywizard/',entity.wizards.NewEntityWizard),
                                        
                                        (r'/sohoadmin/queue/(.*)/',sohoadmin.views.SohoAdminQueuePage),
                                        (r'/sohoadmin/(.*)/(.*)/',sohoadmin.views.SohoAdminPage),
                                        (r'/sohoadmin/(.*)/',sohoadmin.views.SohoAdminPage),
                                        (r'/sohoadmin/',sohoadmin.views.SohoAdminPage),

                                        (r'/about/contactus/',about.views.ContactUsPage),



                                      ],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()