from google.appengine.dist import use_library
use_library('django', "1.0")

#Standard Imports
import logging
import os
import sys
import getopt
import getpass
import datetime
import time
from StringIO import StringIO

#Google Imports
import atom
import gdata
import gdata.service
from gdata.alt.appengine import run_on_appengine
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import users

#Django Imports
import django
from django import http
from django import shortcuts
from django import forms

#from django.forms import ModelChoiceField, ModelMultipleChoiceField
#from django.forms.widgets import *
#from django.forms.util import flatatt, StrAndUnicode, smart_unicode

from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.utils.datastructures import MultiValueDict
from django.core.urlresolvers import reverse
from django.core import serializers
from django.conf import settings

#Django Helper
#from appengine_django.models import BaseModel

#Apis

#Global Parameters
_global_params_loaded = False
_global_params = {}



def GetUser(self):
	return users.get_current_user()

def GetGParam(strKey):
    return GlobalHelper().GetGParam(strKey)

def GetInt(input_value):
    retVal = input_value
    if retVal.isdigit():
        retVal = int(input_value)
    else:
        retVal = 0
    return retVal

class GlobalHelper():
    def GetGParam(self, strKey):
        self.LoadGlobalParameters()
        return _global_params[strKey]

    def LoadGlobalParameters(self):
        import sohoadmin.helpers
        global _global_params_loaded
        global _global_params
        if _global_params_loaded == False:
            _global_params = {}
            app_params = sohoadmin.helpers.HelperApplicationParams().GetAllAsDict()
            for ParamKey in app_params.keys():
                _global_params[ParamKey] = app_params[ParamKey]