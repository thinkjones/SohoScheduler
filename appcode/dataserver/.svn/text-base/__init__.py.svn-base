#Base Imports
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
import datetime
import time

#All Models Must Be Here
import about.models
import about.application_models
import appointment.models
import crm.models
import dashboard.models
import designer.models
import entity.models
import message.models
import sohoadmin.models
import sohoformbuilder.models

EMPTY_VALUES = (None, '')

class DataServer():
    def __init__(self,DataEntityBaseModel=None,entity_ref_field_name=None,active_field_name=None):
        self.datastore_entity = DataEntityBaseModel
        self.entity_ref_field_name = entity_ref_field_name
        self.active_field_name = active_field_name

    def Get(self, pk_id_or_key):
        dataobj = None
        pk_id_or_key = str(pk_id_or_key)
        if pk_id_or_key is None:
            return None
        if pk_id_or_key.isdigit():
            dataobj = self.GetByID(pk_id_or_key)
        else:
            dataobj = self.GetByKey(pk_id_or_key)
        return dataobj

    def GetByID(self, pk_id):
        dataobj = None
        try:
            dataobj = self.datastore_entity.get(db.Key.from_path(self.datastore_entity.kind(), int(pk_id)))
        except:
            dataobj = None
        return dataobj

    def GetByKey(self, key_name):
        dataobj = self.datastore_entity.get_by_key_name(key_name)
        return dataobj
    
    def GetByEntity(self,entity,is_active=True):
        if self.entity_ref_field_name is None:
            return None

        querySet = None
        strGQL = None
        if self.active_field_name:
            strGQL = "WHERE %s = :1 and %s  = :2" % (self.active_field_name,self.entity_ref_field_name)
            querySet = self.datastore_entity.gql(strGQL, is_active, entity)
        else:
            strGQL = "WHERE %s  = :1" % self.entity_ref_field_name
            querySet = self.datastore_entity.gql(strGQL, entity)

        total_count = querySet.count()
        return querySet.fetch(limit=100)

    def GetRecentInserts(self,number_to_get):
        strGQL = "Order By created Desc Limit %s " % number_to_get
        querySet = self.datastore_entity.gql(strGQL)
        results = querySet.fetch(number_to_get)
        return results


    def GetByEntityJsonDict(self, entity, list_field,filteredlist=None):
        gqlresults = filteredlist
        if filteredlist is None:
            gqlresults = self.GetByEntity(entity)

        #Pass in a field dictionary and this will return a dictionary with all your favourite fields in.
        listresults = []
        for gqr in gqlresults:
            dictRow = self.getRowDict(gqr, list_field)
            listresults.append(dictRow)
        return listresults

    def getRowDict(self, row, list_field):
        newRow = {}
        newRow['id'] = str(row.key().id())
        newRow['key'] = str(row.key())
        for efield in row.properties():
            if efield in list_field:
                new_value = self.datastore_entity.properties()[efield].get_value_for_datastore(row)
                newRow[efield] = new_value
        return newRow

    def getRowAsDict(self, row):
        newRow = {}
        newRow['id'] = str(row.key().id())
        newRow['key'] = str(row.key())
        for efield in row.properties():
            new_value = self.datastore_entity.properties()[efield].get_value_for_datastore(row)
            newRow[efield] = new_value
        return newRow

    def getDateFromString(self, value, format):
        dte = None
        if value in EMPTY_VALUES:
            return None
        try:
            if isinstance(value, str) or isinstance(value, unicode):
                dte = datetime.datetime.strptime(value, format)
            return dte
        except ValueError:
            dte = None
        return None

    def getTimeFromString(self, value, format):
        dte = None
        if value in EMPTY_VALUES:
            return None
        try:
            if isinstance(value, str) or isinstance(value, unicode):
                dte = datetime.datetime.strptime(value, format)
            return dte.time()
        except ValueError:
            dte = None
        return None

    #ToDo Cannot refer to a class higher than it in the hierarchy
    def GetGParam(self, strKey):
        return appcode.baseclass.GlobalHelper().GetGParam(strKey)

    def Delete(self, pk_id_or_key):
        dataobj = self.Get(pk_id_or_key)
        bolRet = True
        try:
            dataobj.active = False
            dataobj.put()
        except KeyError:
            bolRet = False
        return bolRet
   
    #ToDo THis might be ok check
    def getMySignup(self):
        return self.getSignupByUser(users.get_current_user())

    def getSignupByUser(self, signup_user):

        if signup_user is None:
            return None

        memcache_key_name = "signup_user_%s" % signup_user.email()
        this_signup = memcache.get(memcache_key_name)

        if this_signup is None:
            this_signups = None
            this_signup = None
            this_signups = about.models.Signup.gql("WHERE signup_user = :1", signup_user)
            if this_signups.count(2) > 0:
                this_signup = this_signups[0]
                memcache.add(memcache_key_name, this_signup, 60)

        return this_signup


#about.models
class ServerSignup(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=about.models.Signup)

class ServerContactUs(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=about.models.ContactUs)

class ServerSignupExtendedProfile(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=about.models.SignupExtendedProfile)

#about.application_models
class ServerStoredToken(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=about.application_models.StoredToken)

#appointment.models
class ServerAppointment(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=appointment.models.Appointment, entity_ref_field_name="entity_reference",active_field_name="active")

#crm.models
class ServerCRM(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=crm.models.CRM, entity_ref_field_name="entity_reference",active_field_name="active")

#dashboard.models
class ServerDashboard(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=dashboard.models.Dashboard)

class ServerDashboardRecentActivity(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=dashboard.models.DashboardRecentActivity)
        
class ServerDashboardRecentActivitySummary(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=dashboard.models.DashboardRecentActivitySummary)
        
#designer.models
class ServerFormDesign(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=designer.models.FormDesign, entity_ref_field_name="entity_reference",active_field_name="active")

class ServerFormDesignField(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=designer.models.FormDesignField)

class ServerFormSubmission(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=designer.models.FormSubmission, entity_ref_field_name="entity_ref")

class ServerFlexFieldValue(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=designer.models.FormSubmission, entity_ref_field_name="entity_ref")

#entity.models
class ServerEntity(DataServer):
    def __init__(self):
         DataServer.__init__(self, DataEntityBaseModel=entity.models.Entity)

class ServerEntityRating(DataServer):
    def __init__(self):
         DataServer.__init__(self, DataEntityBaseModel=entity.models.EntityRating,entity_ref_field_name="entity_reference")

class ServerEntityParams(DataServer):
    def __init__(self):
         DataServer.__init__(self, DataEntityBaseModel=entity.models.EntityParams,entity_ref_field_name="entity_reference")

class ServerAccessRightCode(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=entity.models.AccessRightCode)

class ServerSignupEntityAccess(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=entity.models.SignupEntityAccess)

class ServerInviteEntityAccess(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=entity.models.InviteEntityAccess)

#message.models
class ServerMessage(DataServer):
    def __init__(self):
            DataServer.__init__(self, DataEntityBaseModel=message.models.Message)

class ServerUserMessage(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=message.models.UserMessage)

#sohoadmin.models
class ServerApplicationParams(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=sohoadmin.models.ApplicationParams)

#sohoformbuilder.models
class ServerSohoFormBuilder(DataServer):
    def __init__(self):
        DataServer.__init__(self, DataEntityBaseModel=sohoformbuilder.models.SohoFormBuilder,active_field_name="active")