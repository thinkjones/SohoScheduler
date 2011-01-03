from google.appengine.ext import deferred

from appcode.dataserver import *

import designer.helpers
import entity.helpers
import crm.helpers
import appcode.dataserver

class HelperCRM():
    def GetCRMCount(self, this_entity):
        entitys = None
        entitys = crm.models.CRM.gql("WHERE active = True and entity_reference = :1", this_entity)
        return entitys.count()

    def GetEntityCRMs(self, this_entity):
        return ServerCRM().GetByEntity(this_entity)

    #TODO: modify this to meet the new way of storing data
    def FilterCRMs(self, this_entity, searchFilter):
        this_crms = None
        this_crms = crm.models.CRM.gql("WHERE active = True and entity_reference = :1 order by name", this_entity)
        obj_list = []
        for this_crm in this_crms:
            if this_crm.name is None:
                this_crm.name = "Not Specified"
                this_crm.put()

            if this_crm.name.lower().find(searchFilter.lower()) > -1:
                obj_list.append(this_crm, )
        return obj_list

    def GetCRMByRef(self, crm_ref):
        return ServerCRM().Get(crm_ref)

    def GetorCreate(self, this_entity, crm_name):
        this_crm = None
        this_crms = crm.models.CRM.gql("WHERE active = True and name = :1 and entity_reference = :2", crm_name, this_entity)

        crms_count = this_crms.count()
        if crms_count > 0:
          this_crm  = crms[0]
        else:
          this_crm = crm.models.CRM(name=crm_name, entity_reference=this_entity)
          this_crm.put()

        return this_crm

    def GetRecentActivity(self, owner,  Limit):
        q = db.GqlQuery("SELECT * FROM CRM WHERE owner = :1 order by activity_date DESC", owner)
        results = q.fetch(Limit)
        return results

def CreateAndUpdateContactsDefer(this_entity_id,  newContactsList, access_token_id):
    deferred.defer(CreateAndUpdateContactsByIds, this_entity_id,  newContactsList, access_token_id)
    return True

def CreateAndUpdateContactsByIds(this_entity_id,  newContactsList, access_token_id):
    access_token = appcode.dataserver.ServerStoredToken().Get(access_token_id)
    this_entity = appcode.dataserver.ServerEntity().Get(this_entity_id)
    CreateAndUpdateContacts(this_entity,  newContactsList, access_token)
    return True

def CreateAndUpdateContacts(this_entity,  newContactsList, access_token):

    #1. Get default values
    crm_name_default_field = entity.helpers.HelperEntityParams().GetParam(this_entity,'CustomerNameDefaultField')
    crm_email_default_field = entity.helpers.HelperEntityParams().GetParam(this_entity,'CustomerEmailDefaultField')

    #2. Get default customer name
    crm_name_field_name = None
    if crm_name_default_field:
        crm_name_field_id = crm_name_default_field.param_value
        crm_name_field = ServerFormDesignField().Get(crm_name_field_id)
        crm_name_field_name = crm_name_field.field_name

    #3. Get default customer email
    crm_email_field_name = None
    if crm_email_default_field:
        crm_email_field_id = crm_email_default_field.param_value
        crm_email_field = ServerFormDesignField().Get(crm_email_field_id)
        crm_email_field_name = crm_email_field.field_name

    #4. Loop through list.
    for newContact in newContactsList:
        #CreateAndUpdateEntry(this_entity,newContact,crm_name_field_name,crm_email_field_name,access_token)
        CreateAndUpdateEntryDefer(this_entity.key().id(),newContact,crm_name_field_name,crm_email_field_name,access_token.key().id())

    return True

def CreateAndUpdateEntryDefer(this_entity_id,  new_contact, defaultCRMText,defaultCRMEmail, access_token_id):
    deferred.defer(CreateAndUpdateEntryByIds, this_entity_id,  new_contact, defaultCRMText,defaultCRMEmail, access_token_id)
    return True

def CreateAndUpdateEntryByIds(this_entity_id,  new_contact, defaultCRMText,defaultCRMEmail, access_token_id):
    access_token = appcode.dataserver.ServerStoredToken().Get(access_token_id)
    this_entity = appcode.dataserver.ServerEntity().Get(this_entity_id)
    CreateAndUpdateEntry(this_entity,new_contact,defaultCRMText,defaultCRMEmail, access_token)
    return True


def CreateAndUpdateEntry(entity,newContact,defaultCRMText,defaultCRMEmail, stored_token):

    #Create a listVals list that contains data to update
    entity_id = entity.key().id()

    #1. Create Form Submission
    fs = designer.helpers.HelperFormSubmission().Create(entity_id,2,0)
    submission_key = str(fs.key())
    submission_id = fs.key().id()

    #2. Create listvals
    listVals = []
    if defaultCRMText:
        listVals.append({'name':defaultCRMText,'value':newContact['ContactName']})
    if defaultCRMEmail:
        listVals.append({'name':defaultCRMEmail,'value':newContact['ContactEmail']})

    #3. Insert Data
    processValues = designer.helpers.ServerProcessPost(form_submission=fs,listVals=listVals)
    processValues.ProcessValues()

    #4. Get Form Submission
    fs = ServerFormSubmission().Get(submission_id)

    #5. Get the new entry to update the external id
    this_crm = ServerCRM().Get(fs.pkid)
    this_crm.external_system_id = newContact['ContactID']
    this_crm.stored_token_ref = stored_token
    this_crm.put()

    return True
