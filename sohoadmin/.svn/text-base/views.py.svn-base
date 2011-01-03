from appcode.dataserver import *
from appcode.viewsbaseclass import *
from google.appengine.api import users
from sohoadmin.helpers import *
from appcode.install.version_0_7 import *
from appcode.install.version_0_8 import *
from appcode.taskqueuehelper import *

import about.helpers

import csv
PAGE_SIZE = 20
DEFAULT_FREVVO_SERVER = 'test.frevvo.com:9092'
import logging
logging.logMultiprocessing = 0

import sys
import getopt
import getpass
import atom
import gdata
import gdata.service
from gdata.alt.appengine import run_on_appengine

def changetemplaterating():
    asd=1
def downloadusers():
    asd=1
def queue():
    asd=1
def install07():
    asd=1
def install08():
    asd=1
def index():
    asd=1/0

class SohoAdminPage(SohoResponse):
    @sohosecurity.authenticate('Owner')
    def get(self,param1=None, param2=None):
        if param1=="install":
            self.installReleaseCode(param2)
        if param1 is None:
            self.default()

    def installReleaseCode(self, version):
        if version == "07": runInstall07()
        if version == "08": runInstall08()
        return self.default()

    def default(self):
        template = 'sohoadmin/index'
        if self.IsAjaxRequest():
                template = 'admin/_main'

        signup_users = appcode.dataserver.ServerSignup().GetRecentInserts(10)
        entities = appcode.dataserver.ServerEntity().GetRecentInserts(10)
        templates = entity.helpers.HelperEntity().GetRecentTemplates(20)

        signupUser = appcode.dataserver.DataServer().getMySignup()
        myExtendedProfile = about.helpers.HelperSignupExtendedProfile().GetAll(signupUser)

        self.template = template
        self.is_admin_screen = True
        self.tabSelected = 'tabDashboard'
        self.signup_users = signup_users
        self.entities = entities
        self.templates = templates
        self.myExtendedProfile = myExtendedProfile
        self.respond()

    def downloadusers(self):
        #Get Last 1000 Users
        signup_users = about.helpers.GetRecentUsers(1000)
        signup_user = None

        #Create Spreadsheet
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=sohoscheduleruseres.csv'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Created'])
        for signup_user in signup_users:
                writer.writerow([str(signup_user.signup_user), signup_user.created])
        return response

    def changetemplaterating(self, entity_id, rating):
        #1. Makes a template high quality ready for public consumption
        ServerEntityRating().ChangeTemplateRating(entity_id, rating)
        return self.default()

class SohoAdminQueuePage(SohoResponse):
    def post(self, task_name):
        TaskQueueHelper().RunTask(self.request.POST, task_name)
        strMessage = "Task %s completed" % task_name
        self.json_respond(strMessage)
