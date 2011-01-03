from google.appengine.dist import use_library
use_library('django', "1.0")

import os,sys
import logging

#Standard Imports
from google.appengine.ext import webapp
from appcode.dataserver import *
from appengine_utilities.sessions import Session
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse


import appcode.sohosecurity as sohosecurity
import about.helpers
import message.helpers
import entity.helpers

import appcode.sohosecurity

class SohoResponseSession():
    def __init__(self):
        self.session = Session()

    def __getitem__(self, keyname):
        try:
            session_val_test = self.session[keyname]
        except KeyError:
            session_val_test = None
        return session_val_test

    def __setitem__(self, keyname, value):
        bolRet = True
        try:
            self.session[keyname] = value
        except KeyError:
            bolRet = False
        return bolRet

    def get(self, keyname, default = None):
        """
        Returns either the value for the keyname or a default value
        passed.

        Args:
            keyname: keyname to look up
            default: (optional) value to return on keyname miss

        Returns value of keyname, or default, or None
        """
        try:
            return self.__getitem__(keyname)
        except KeyError:
            if default is not None:
                return default
            return None

class SohoResponse(webapp.RequestHandler):
    def __init__(self, template=None):
        #Main Response Parameters
        self.template = template
        self.session = SohoResponseSession()
        self.params = {}

        #User
        self.user = users.GetCurrentUser()
        self.access_rights = None
        self.signup_user = None 
        self.is_admin = None 
        self.signed_up = False
        if self.user:
            self.signed_up = True

        #Data
        self.company_id = 0
        self.entity_id = 0
        self.companys = None
        self.company = None
        self.entity = None
        self.entity_render_type  = 0
        self.customer_id = 0
        self.customers = None
        self.customer = None
        self.mainmessages = None
        self.application_version = 0.6
        self.logged_in_required = True
        self.header_text = 'Soho Scheduler'
        self.sub_header_text = 'Pioneering small business simplicity.'
        self.mode = 'Manage Individual Company'
        self.EntityCount = 0
        self.is_design_mode = False
        self.is_admin_screen = False
        self.tabSelected = None
        self.entity_access_rights = False
        self.access_rights = None


        #Display
        self.sign_out = users.CreateLogoutURL('/')
        self.sign_in = None

    def respond(self):
        #Refresh Session Variable If Required
        self.setupSession()

        self.sign_in = users.CreateLoginURL('/')

        if not self.template.endswith('.html'):
            self.template += '.html'

        #1. Check that user is logged in if not then you cannot  access this resource
        if self.logged_in_required:
            if self.IsRegularUser() == False:
                return self.redirect('/')

        self.application_version = 0.8
        EntityHasAccess = False

        #1. Check we have access to a company
        if int(self.entity_id) > 0:
            self.entity_access_rights = appcode.sohosecurity.SohoSecurityHelper(self.session).getEntityAccessRights(self.entity_id)
            EntityHasAccess = self.entity_access_rights['View']
            if EntityHasAccess == False and users.IsCurrentUserAdmin():
                EntityHasAccess = True
            if EntityHasAccess:
                self.EntityCount = 1
            else:
                return self.redirect('/')
        else:
            self.EntityCount = entity.helpers.HelperSignupEntityAccess().GetMyEntityCount()

        #3. If we get to here then we can process
        self.params = {}

        self.access_rights = self.session['access_rights']

        #3.1. Setup headertext
        if self.entity:
            self.header_text = self.entity.name
            self.sub_header_text = 'powered by soho scheduler'

        message_has_been_shown = self.session.get('message_has_been_shown',True)
        if message_has_been_shown==False:
            self.session['message_has_been_shown'] = True
        else:
            self.session['temp_message_title'] = ""
            self.session['temp_message_body'] = ""

        #3.2 Check if in design mode
        self.is_design_mode = False
        self.entity_render_type = appcode.sohosecurity.SohoSecurityHelper(self.session).getEntityRenderType(self.entity_id)

        if self.entity_render_type == "2":
            self.is_design_mode = True

        self.entity_id = int(self.entity_id)

        for key in dir(self):
            if '__' not in key:
                value = getattr(self, key)
                self.params[key] = value

        django_http_response = render_to_response(self.template, self.params)
        self.response.out.write(django_http_response.content)

    def json_respond(self, dictResponse):
        jsontext = simplejson.dumps(dictResponse)
        django_http_response = HttpResponse(jsontext, mimetype="application/json")
        self.response.out.write(django_http_response.content)


    def respond_blank(self):
        obj_list = []
        #return HttpResponse(simplejson.dumps(None), mimetype='application/javascript')
        return HttpResponse("", mimetype='application/javascript')

    def setupSession(self):
        #1. Determine whether session is needed to be refreshed
        refresh_session = False
        session_refresh_session = None
        
        #1.5 Setup session refresh session variable
        refresh_session = self.getSessionVal('refresh_session')
        if refresh_session is None:
            self.setSessionVal('refresh_session', True)
            self.setSessionVal('user_id', 0)
            refresh_session = True

        #3. Is there a logged in user and no session information set
        if self.getSessionVal('user_id') == 0 and self.user:
            refresh_session = True

        #4. Refresh session variables
        if refresh_session:
            self.signup_user = DataServer().getMySignup()
            if self.signup_user:
                self.session['signup_user'] = self.signup_user
                self.session['signup_id'] = self.signup_user.key().id()
                self.session['is_admin'] = users.IsCurrentUserAdmin()
                accessRights = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()
                self.session['access_rights'] = accessRights
                #asd=1/0
            else:
                self.session['signup_user'] = "None"
                self.session['signup_id'] = 0
                self.session['is_admin'] = False

        #5. Allocate SOhoresponse variables from session
        self.signup_user = self.session['signup_user']
        self.signup_id = self.session['signup_id']
        self.is_admin = self.session['is_admin']
        self.session['refresh_session'] = False

    def setSessionVal(self, session_key, initial_Value):
        if self.session is None:
            self.session = Session()
        bolRet = True
        try:
            self.session[session_key] = initial_Value
        except KeyError:
            bolRet = False
        return bolRet            

    def getSessionVal(self, session_key):
        if self.session is None:
            self.session = Session()
        try:
            session_val_test = self.session[session_key]
        except KeyError:
            session_val_test = None
        return session_val_test

    def getUserAccessRights(self):
        #1. Does user have access anywhere?
        user_access_rights = entity.helpers.HelperSignupEntityAccess().getUserAccessRights()
        current_signup = DataServer().getMySignup()

        #2. If no access entries returned then assume this has not yet been setup for the user.
        #. Therefore create the required entries by returning all their entities.
        if user_access_rights.count() < 1:
            entity.helpers.HelperSignupEntityAccess().analyzeUserProfileAndCreateUserAccessRights(current_signup)
            #3. Re-get the entities and convert them into a dictionary for the session.
            user_access_rights = entity.helpers.HelperSignupEntityAccess().getUserAccessRights()

        #3. Get Access Information
        accessRights = []
        for gqr in user_access_rights:
            newRow = {}
            newRow['id'] = str(gqr.key().id())
            newRow['key'] = str(gqr.key())
            newRow['access_right_code'] = str(gqr.access_right_code.name)
            newRow['entity_id'] = str(gqr.entity_reference.key().id())
            accessRights.append(newRow)

        return accessRights

    def GetRedirectToDefaultDashboard(self, entity_id):
        #Called by functions on non ajax calls that redirects to dashboard 0 entity_id supplied

        #1. If entity_id is supplied then we do not need to redirect as everything is ok
        if int(entity_id) > 0:
            return None

        #2. Get Default Entity ID and or create one if not exists.
        this_entity = entity.helpers.HelperEntity().GetDefaultEntity(self.request)
        if this_entity:
            entity_id = this_entity.key().id()
            #return http.HttpResponseRedirect('/%s/%r/dashboard/' % (strCompanyEntity, int(entity_id)))
            redirect_url = reverse('dashboard.views.index', args=[entity_id])
            return  redirect_url
        else:
            return None

    def IsAjaxRequest(self):
        env = self.request.environ
        retVal = env.has_key('HTTP_X_REQUESTED_WITH') and env.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        return retVal

    def showNotification(self,this_message,message_type=""):
        self.session['temp_message_count'] = 0
        self.session['temp_message_body'] = this_message
        self.session['temp_message_type'] = message_type
        self.session['message_has_been_shown'] = False
        return None

    def IsAdminUser(self):
            #Check for admin user if not redirect to home
            bolIsAdminUser=False
            if self.user:
                bolIsAdminUser = users.is_current_user_admin()
            return bolIsAdminUser

    def IsRegularUser(self):
            #Check for admin user if not redirect to home
            bolIsUser=False
            if self.user:
                bolIsUser = True
            return bolIsUser

    def GetInt(self,input_value):
        retVal = input_value
        if retVal.isdigit():
            retVal = int(input_value)
        else:
            retVal = 0
        return retVal
