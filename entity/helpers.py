from appcode.dataserver import *
from designer.helpers import *
import about.helpers
import designer.helpers
import entity.helpers
import appcode.mailhelper

class HelperEntity():
    entityTypes = {
        'TypeEntityRegular':1,
        'TypeEntityTemplate':2,
        }

    def GetEntityCount(self):
        entitys = None
        entitys = entity.models.Entity.gql("WHERE active = True and signup_reference = :1", DataServer().getMySignup())
        return entitys.count()

    def GetMyEntitys(self,show_just_active=True):
        return GetMyEntitys(0,show_just_active)

    def GetMyEntitys(self, entity_render_type=0,show_just_active=True):
        entitys = None
        if show_just_active:
            if entity_render_type == 0:
                entitys = entity.models.Entity.gql("WHERE active = True and signup_reference = :1", DataServer().getMySignup())
            else:
                entitys = entity.models.Entity.gql("WHERE active = True and signup_reference = :1 and entity_render_type = :2", DataServer().getMySignup(),  entity_render_type)
        else:
            if entity_render_type == 0:
                entitys = entity.models.Entity.gql("WHERE signup_reference = :1", DataServer().getMySignup())
            else:
                entitys = entity.models.Entity.gql("WHERE signup_reference = :1 and entity_render_type = :2", DataServer().getMySignup(),  entity_render_type)

        return entitys

    def GetEntitysByMnemonic(self, mnemonic=None):
        entitys = None
        entitys = entity.models.Entity.gql("WHERE mnemonic = :1", mnemonic)
        return entitys

    def CheckAccess(self, entity_id):
        user = users.get_current_user()
        signup_reference = DataServer().getMySignup()
        this_entity = ServerEntity().Get(entity_id)
        bolRet = False
        if this_entity:
            if signup_reference.key().id() == this_entity.signup_reference.key().id():
                bolRet = True
        return bolRet

    def GetDefaultEntity(self,request):
        entity_access_rights = None
        default_entity = None
        default_entity_id = 0
        default_entity_access = None

        #Get Detault From Signup Extended Profile
        default_param = about.helpers.HelperSignupExtendedProfile().GetParam('default_entity_id')
        if default_param:
            default_entity_id = default_param.param_value

        #Is number and check we still have access
        if default_entity_id:
            if default_entity_id.isdigit():
                default_entity_id = int(default_entity_id)
                entity_access_rights = appcode.sohosecurity.SohoSecurityHelper().getEntityAccessRights(default_entity_id)
                has_access = entity_access_rights['View']
                if has_access==False:
                    about.helpers.HelperSignupExtendedProfile().DeleteParam('default_entity_id')
                    default_entity_id = 0
        else:
            default_entity_id = 0

        #Did we find a default, if not create one if we can
        if default_entity_id == 0:
            #Make a default entry
            default_entity_accesses = entity.helpers.HelperSignupEntityAccess().GetMyEntitys()
            if default_entity_accesses.count() > 0:
                default_entity_access = default_entity_accesses[0]
            if default_entity_access:
                default_entity_id = default_entity_access.entity_reference.key().id()
                about.helpers.HelperSignupExtendedProfile().SetParam('default_entity_id',default_entity_id)

        if default_entity_id > 0:
            default_entity = appcode.dataserver.ServerEntity().Get(default_entity_id)
        return default_entity

    def CreateDefaultEntry(self):
        entitys = None
        this_entity = None
        entitys = entity.models.Entity.gql("WHERE active = True and signup_reference = :1 and is_default = True", DataServer().getMySignup())
        if entitys.count() > 0:
            this_entity = entitys[0]
        else:
            #no default set but do they have entities - if yes set first entry to be the default.
            myentities = self.GetMyEntitys()
            if myentities.count() > 0:
                this_entity = myentities[0]
                this_entity.is_default = True
                this_entity.put()
        return this_entity

    def SetDefault(self, entity_id):
        default_entity = self.GetEntity(entity_id)
        entitys = self.GetMyEntitys()
        for entity in entitys:
            if entity == default_entity:
                entity.is_default = True
            else:
                entity.is_default = False
            entity.put()

    def GetRecentActivity(self, signup_reference,  Limit):
        querySet = entity.models.Entity.gql("WHERE signup_reference = :1", signup_reference)
        resultSet = querySet.fetch(Limit)
        return resultSet

    def GetRecentEntities(self, Limit):
        querySet = entity.models.Entity.gql("WHERE entity_render_type = 1 ORDER BY created DESC ")
        resultSet = querySet.fetch(Limit)
        for row in resultSet:
            try:
                signupref = row.signup_reference
            except Exception:
                row.signup_reference = None
                row.put()
        return resultSet

    def GetRecentTemplates(self, Limit):
        querySet = entity.models.Entity.gql("WHERE entity_render_type = 2 ORDER BY created DESC ")
        resultSet = querySet.fetch(Limit)
        return resultSet

    def CopyEntityFromTemplateNoSave(self, template_entity_id,  signup_reference):
        entity_template = self.GetEntity(template_entity_id)
        entity_name = "Blank Entity"
        entity_desc = "Empty entity ready for designing."
        entity_tags = " "
        if entity_template:
            entity_name = "" #New %s " % entity_template.name
            entity_desc = "" #entity_template.desc
            entity_tags = "" #entity_template.tags
        this_entity = None

        if this_entity == None:
            this_entity = Entity(name=entity_name, desc=entity_desc, signup_reference=signup_reference, tags=entity_tags)

        this_entity.entity_render_type = entity.helpers.HelperEntity().entityTypes['TypeEntityRegular']
        this_entity.derived_from_entity = entity_template
        return this_entity


class HelperEntityRating():

    def GetHighQualityTemplates(self):
        entitys = None
        entitys = entity.models.EntityRating.gql("WHERE entity_rating >= 10")
        return entitys

    def GetEntityRatingByEntity(self, this_entity):
        return self.GetByEntity(this_entity)

    def GetEntityRatingByEntityID(self, entity_id):
        #1. Get entity
        results = appcode.dataserver.ServerEntityRating().GetByEntity(entity_id)
        if results.count(50) > 0:
            return results[0]
        else:
            return None

    def ChangeTemplateRating(self, entity_id, rating):
        #1. Init
        entity_rating = self.GetEntityRatingByEntityID(entity_id)
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

        #2. return if not found
        if this_entity is None:
            return

        #3. Check rating exists
        if entity_rating is None:
            entity_rating = entity.models.EntityRating(entity_reference = this_entity, entity_rating=int(rating))
        else:
            entity_rating.entity_rating = int(rating)
        entity_rating.put()

        #4. Update Enitty to label as high quality
        if int(rating) > 9:
            entity.is_high_quality_template = True
        else:
            entity.is_high_quality_template = False
        this_entity.put()

default_entity_parameters = {
    'CustomerNameDefaultField':'CustomerName',
    'AppointmentDateDefaultField':'BookingDate',
}

class HelperEntityParams():

    def GetParam(self, this_entity, param_name):
        entity_param = None
        entity_params = entity.models.EntityParams.gql("WHERE entity_reference = :1 and param_name = :2", this_entity, param_name)
        if entity_params.count() > 0:
            entity_param = entity_params[0]
        return entity_param

    def GetAllBase(self, this_entity):
        q = db.GqlQuery("SELECT * FROM EntityParams WHERE entity_reference = :1", this_entity)
        results = q.fetch(50)
        return results

    def GetAll(self, this_entity):
        results = self.GetAllBase(this_entity)
        number_default_params = len(default_entity_parameters)
        if results.count(100) != len(default_entity_parameters):
            self.InsertDefaultValues(this_entity)
            results = self.GetAllBase(this_entity)
        return results

    def GetAllAsDict(self, this_entity):
        results = self.GetAllBase(this_entity)
        number_default_params = len(default_entity_parameters)
        if results.count(100) != len(default_entity_parameters):
            self.InsertDefaultValues(this_entity)
            results = self.GetAllBase()
        fooDict = {}
        for foo in results:
            fooDict[foo.param_name] = foo.param_value
        return fooDict

    def DoDefaultValuesNeedInserting(self):
        if self.GetCount() == len(default_entity_parameters):
            return True
        else:
            return False

    def InsertDefaultValues(self, this_entity):
        #1. Get all parameters
        current_params = {}
        results = self.GetAllBase(this_entity)
        for foo in results:
            current_params[foo.param_name] = foo.param_value
        default_params = default_entity_parameters

        #2. Loop through defaults and check they are all present in the application
        for dParamKey in default_params.keys():
            if current_params.has_key(dParamKey) == False:
                param_value = default_entity_parameters[dParamKey]
                self.SaveParam(this_entity, dParamKey,param_value)

    def SaveParam(self, this_entity, dParamKey, dParamValue):
        current_param = self.GetParam(this_entity, dParamKey)
        if current_param is None:
            current_param = entity.models.EntityParams(entity_reference=this_entity,param_name=dParamKey,param_value=dParamValue)
        else:
            current_param.param_value=dParamValue
        current_param.put()


class HelperAccessRightCode():
    def createDefaultEntries(self):
        current_rights = entity.models.AccessRightCode.all()
        if current_rights.count() < 1:
            #Create basic rights
            na = entity.models.AccessRightCode(key_name="Owner",mnemonic="Owner",name="Owner",desc="Indicates the owner.")
            na.put()
            na = entity.models.AccessRightCode(key_name="ReadWrite",mnemonic="ReadWrite",name="Edit",desc="Has access to read and write data to the forms in the application")
            na.put()
            na = entity.models.AccessRightCode(key_name="ReadOnly",mnemonic="ReadOnly",name="View",desc="Has a view only mode to the application.")
            na.put()
            na = entity.models.AccessRightCode(key_name="FormDesigner",mnemonic="FormDesign",name="Form Design",desc="Has form design access to the application.")
            na.put()
    
    def getByMnemonic(self, filter_name):
        access_code = None
        access_codes = entity.models.AccessRightCode.gql("WHERE mnemonic = :1", filter_name)
        if access_codes.count() > 0:
            access_code = access_codes[0]
        return access_code
        


class HelperSignupEntityAccess():

    def deleteAccessAndEntity(self,this_entity):
        #Handles all the delete code for entity

        #Delete entity so that it no longer should be shown
        this_entity.active = False
        this_entity.put()

        #Remove Accesss RIghts so it doesn't show up in anybodies dashboard lists
        this_signup = DataServer().getMySignup()
        entity_access = None
        entity_access = entity.models.SignupEntityAccess.gql("WHERE signup_reference = :1 and entity_reference = :2", this_signup, this_entity)
        for access_right in entity_access:
            access_right.delete()

        #Reset default access
        allentities = entity.helpers.HelperEntity().GetMyEntitys(entity_render_type=0,show_just_active=True)
        new_default_entity_id = 0
        if allentities.count() > 0:
            last_entry_index = int(allentities.count() - 1)
            new_default_entity_id  = allentities[last_entry_index].key().id()
        about.helpers.HelperSignupExtendedProfile().SetParam('default_entity_id',new_default_entity_id)

    def getUserAccessRights(self):
        entity_access = None
        entity_access = entity.models.SignupEntityAccess.gql("WHERE signup_reference = :1", DataServer().getMySignup())
        return entity_access

    def getBySignupAndEntity(self, signup_ref, this_entity):
        entity_access = None
        entity_access = entity.models.SignupEntityAccess.gql("WHERE signup_reference = :1 and entity_reference = :2", signup_ref, this_entity)
        return entity_access

    def getBySignupAndEntityFirst(self, signup_ref, this_entity):
        entity_access = None
        entity_accesses = self.getBySignupAndEntity(signup_ref, this_entity)
        if entity_accesses.count() > 0:
            entity_access = entity_accesses[0]
        return entity_access

    def GetMyEntitys(self):
        entitys = None
        entitys = entity.models.SignupEntityAccess.gql("WHERE active = True and signup_reference = :1", DataServer().getMySignup())
        return entitys

    def GetMyEntitysFirst(self):
        entity_access = None
        entity_accesses = self.GetMyEntitys()
        if entity_accesses.count() > 0:
            entity_access = entity_accesses[0]
        return entity_access

    def GetMyEntitysByRenderType(self,entity_render_type=1):
        entitys = self.GetMyEntitys()
        new_entitys = []
        if str(entity_render_type) == "0":
            return entitys
        else:
            for ent in entitys:
                if ent.entity_reference.entity_render_type == entity_render_type:
                    new_entitys.append(ent)
        return new_entitys

    def GetMyEntityCount(self):
        entitys = self.GetMyEntitys()
        return entitys.count(100)

    def FilterHelper(self,these_entities, entity_render_type=1, access_code_mnem='Owner',bol_equal_to=True):
        new_entitys = []
        for ent in these_entities:
            #Assume you can add and prove wrong
            bol_can_add = True

            #Entiry Render Type Filter
            if str(entity_render_type) != "0":
                if ent.entity_reference.entity_render_type != entity_render_type:
                    bol_can_add = False

            #Access Code Filter
            if bol_equal_to:
                if ent.access_right_code.mnemonic != access_code_mnem:
                    bol_can_add = False
            else:
                if ent.access_right_code.mnemonic == access_code_mnem:
                    bol_can_add = False

            if bol_can_add:
                    new_entitys.append(ent)
        return new_entitys
        
    def getByEntity(self, this_entity,filter_active=False):
        entity_access = None
        if filter_active:
            entity_access = entity.models.SignupEntityAccess.gql("WHERE active = True and entity_reference = :1", this_entity)
        else:
            entity_access = entity.models.SignupEntityAccess.gql("WHERE entity_reference = :1", this_entity)
        return entity_access

    def getUserAccessRightsAsList(self):
        #1. Does user have access anywhere?
        user_access_rights = self.getUserAccessRights()
        current_signup = DataServer().getMySignup()

        #2. If no access entries returned then assume this has not yet been setup for the user.
        #. Therefore create the required entries by returning all their entities.
        if user_access_rights.count() < 1:
            self.analyzeUserProfileAndCreateUserAccessRights(current_signup)
            #3. Re-get the entities and convert them into a dictionary for the session.
            user_access_rights = self.getUserAccessRights()

        #3. Get Access Information
        accessRights = []
        for gqr in user_access_rights:
            newRow = {}
            newRow['id'] = str(gqr.key().id())
            newRow['key'] = str(gqr.key())
            newRow['access_right_code'] = str(gqr.access_right_code.name)
            newRow['entity_id'] = str(gqr.entity_reference.key().id())
            newRow['entity_render_type'] = str(gqr.entity_reference.entity_render_type)
            accessRights.append(newRow)

        return accessRights

    def analyzeUserProfileAndCreateUserAccessRights(self, signup_ref=None):
        #User data association information this function takes a look at the entities and creates
        #the owner right to the correct users.

        if signup_ref is None:
            signup_ref = DataServer().getMySignup()

        #1. Get all entities including designs and templates
        allentities = entity.helpers.HelperEntity().GetMyEntitys(entity_render_type=0,show_just_active=False)

        #2. Check all entites have been deleted as necessary
        for each_entity in allentities:
            if each_entity.active == False:
                self.deleteAccessAndEntity(each_entity)

        #3. Now Get Just Active
        allentities = entity.helpers.HelperEntity().GetMyEntitys(entity_render_type=0,show_just_active=True)

        #2. Loop through all entities and reset
        for each_entity in allentities:
            this_entity_right = entity.helpers.HelperSignupEntityAccess().getBySignupAndEntity(signup_ref,each_entity)
            bol_create_new_right_code = False
            if this_entity_right.count() > 1:
                bol_create_new_right_code = True
                #Cannot have more than one right per Entity delete and start again
                for access_right in this_entity_right:
                    access_right.delete()
            elif this_entity_right.count() < 1:
                bol_create_new_right_code = True

            if bol_create_new_right_code:
                #Create right because this user is the owner
                owner_access_right_code = appcode.dataserver.ServerAccessRightCode().GetByKey(key_name='Owner')
                new_access_right = entity.models.SignupEntityAccess(signup_reference=signup_ref,entity_reference=each_entity,signup_user=users.get_current_user(),access_right_code=owner_access_right_code,active=True)
                new_access_right.put()

    def checkForInactiveEntities(self):
        this_signup = DataServer().getMySignup()
        entity_access = None
        entity_access = entity.models.SignupEntityAccess.gql("WHERE signup_reference = :1 and entity_reference = :2", this_signup, this_entity)
        for access_right in entity_access:
            access_right.delete()

class HelperInviteEntityAccess():

    def getByEntity(self, this_entity):
        entity_access = None
        entity_access = entity.models.InviteEntityAccess.gql("WHERE active = true and entity_reference = :1", this_entity)
        return entity_access

    def getByEmail(self, this_entity, this_email):
        this_entity_access = None
        invites = self.getByEntity(this_entity)
        for invite in invites:
            if str(invite.invite_email_address).lower().lstrip().rstrip() == str(this_email).lower().lstrip().rstrip():
                this_entity_access = invite
        return this_entity_access

    def getMyInvites(self, this_email):
        my_entity_invites = None
        my_entity_invites = entity.models.InviteEntityAccess.gql("WHERE active = true and invite_email_address = :1", this_email)
        return my_entity_invites

    def ProcessInvite(self,this_invite,accept_invite):
        #Mark invite as processed
        this_invite.active = False
        this_invite.invite_accepted = datetime.datetime.now()
        this_invite.put()

        #Create signup entity access if access granted
        if accept_invite:
            #Does user have acceess already?
            this_signup = DataServer().getMySignup()
            this_entity_access = entity.helpers.HelperSignupEntityAccess().getBySignupAndEntityFirst(this_signup, this_invite.entity_reference)
            if this_entity_access:
                this_entity_access.active = True
                this_entity_access.access_right_code = this_invite.access_right_code
                this_entity_access.put()
            else:
                this_access_right_code = this_invite.access_right_code
                new_access_right = entity.models.SignupEntityAccess(signup_reference=this_signup,
                                                        entity_reference=this_invite.entity_reference,
                                                        signup_user=users.get_current_user(),
                                                        access_right_code=this_access_right_code,active=True)
                new_access_right.put()

        return accept_invite




            


def CreateTemplateFromEntity(entity_id,  template_entity_id):
    entityType = entity.helpers.HelperEntity().entityTypes['TypeEntityTemplate']
    CopyEntityApplication(entity_id,  template_entity_id, entityType)

def CreateEntityFromTemplate(template_entity_id, entity_id):
    entityType = entity.helpers.HelperEntity().entityTypes['TypeEntityRegular']
    CopyEntityApplication(template_entity_id, entity_id, entityType)

def CreateBasicApplicationForExistingEntity(entity_id):
    #Fixes entities which don't have the correct forms
    entityType = entity.helpers.HelperEntity().entityTypes['TypeEntityRegular']
    srcEntitys = appcode.dataserver.ServerEntity().GetEntitysByMnemonic('BasicEntityTemplate')
    srcEntity = None
    if srcEntitys.count() > 0:
        srcEntity = srcEntitys[0]
    srcEntityID = srcEntity.key().id()
    CopyEntityApplication(srcEntityID,entity_id,entityType)

def CopyEntityApplication(srcEntityID,  destEntityID, entityType):
    #1. Ensure New Entity Information is properly entered
    srcEntity = appcode.dataserver.ServerEntity().Get(srcEntityID)
    destEntity = appcode.dataserver.ServerEntity().Get(destEntityID)

    #2. Update New entity template
    destEntity.entity_render_type = entityType
    destEntity.derived_from_entity = srcEntity
    destEntity.put()

    #3. Get
    source_form_crm = designer.helpers.HelperFormDesign().GetByEntityAndFormType(srcEntity, 2)
    designer.helpers.HelperFormDesign().CopyFormDesign(source_form_crm, destEntity)
    dest_form_crm = designer.helpers.HelperFormDesign().GetByEntityAndFormType(destEntity, 2)

    #3. Create Appointment FOrm
    source_form_appointment = designer.helpers.HelperFormDesign().GetByEntityAndFormType(srcEntity, 1)
    designer.helpers.HelperFormDesign().CopyFormDesign(source_form_appointment, destEntity)
    dest_form_appointment = designer.helpers.HelperFormDesign().GetByEntityAndFormType(destEntity, 1)

    #4. Get Form Design Fields
    designer.helpers.ProcessDesignChanges(dest_form_crm)
    designer.helpers.ProcessDesignChanges(dest_form_appointment)

    #5. Direct Copy of Entity Params
    CopyEntityParams(srcEntity,destEntity)

    #6. Alter parameters which apply to new forms.
    BespokeEntityParamsUpdate(destEntity, dest_form_crm, dest_form_appointment)

def CopyEntityParams(srcEntity, destEntity):
    src_params = entity.helpers.HelperEntityParams().GetAll(srcEntity)
    for param in src_params:
        new_param = None
        new_param = entity.helpers.HelperEntityParams().GetParam(destEntity, param.param_name)
        if new_param is None:
            new_param = entity.models.EntityParams(entity_reference=destEntity,param_name=param.param_name,param_value=param.param_value)
        new_param.put()
    return None

def BespokeEntityParamsUpdate(destEntity, dest_form_crm, dest_form_appointment):
    #This involves a bespoke change of params based on new ids generated when copying an application
    #Bespoke Change 1: Update fields CustomerNameDefaultField and AppointmentDateDefaultField with the correct field id for this new entity
    CopyFormDesignFieldEntityParameter(destEntity, dest_form_appointment, 'AppointmentDateDefaultField')
    CopyFormDesignFieldEntityParameter(destEntity, dest_form_appointment, 'AppointmentCRMDefaultField')
    CopyFormDesignFieldEntityParameter(destEntity, dest_form_crm, 'CustomerNameDefaultField')
    
def CopyFormDesignFieldEntityParameter(destEntity, dest_form, entityParameterName):
    #1. Get Currently stored field id.  Because the entity has just been copied this will contain an id
    #from the previous entity and needs to be updated
    param = entity.helpers.HelperEntityParams().GetParam(destEntity,entityParameterName)
    formdesignfield_id = param.param_value

    #2. Get this field name - which if using default data will already be the field name
    srcfield_name = None
    if formdesignfield_id.isdigit():
        srcfield_name = GetFieldName(formdesignfield_id)
    else:
        srcfield_name = formdesignfield_id  #in this instance it won't be an id but the name already usually happens with setup data

    #3. Look for this control ID in the new fields
    new_field = designer.helpers.HelperFormDesignField().GetByFieldName(dest_form,srcfield_name)

    #4. Update the entity parameter with the id for the new form.
    if new_field:
        param.param_value = str(new_field.key().id())
        param.put()

def GetFieldName(formdesignfield_id):
    srcField = appcode.dataserver.ServerFormDesignField().Get(formdesignfield_id)
    if srcField is None:
        return ""
    srcfield_name = str(srcField.field_name)
    return srcfield_name


def IsPostAuthenticatedAsValid(entity_key, entity_id, user_key):
    #1. Assume not valid
    bolRet = False

    #2. Get Data
    entity = appcode.dataserver.ServerEntity().Get(entity_id)
    user = appcode.dataserver.ServerSignup().Get(user_key)

    #3. Authenticate
    if entity:
        if entity.key().id() == entity_key:
            #ToDO: This will change as we allow multiple users to access the same system.
            if entity.signup_reference.key() == user_key:
                bolRet = True
    return bolRet


def EmailUserWithAccessInvitation(this_invite):
    #1. Create email message
    signupUser = this_invite.host_signup_reference
    toEmail = this_invite.invite_email_address
    subject = "Invitation to Soho Scheduler Application %s ." % this_invite.entity_reference.name
    body = """
        Soho Scheduler is a resource scheduling application for small businesses.

        You have been granted to the following application:
        
        Access to application: %s

        Granted by: %s

        Permissions: %s

        To accees this instance simply login to Soho Schduler using this email address %s at www.sohoappspot.com .  Your shared applications will be visible on the dashboard.
        
        Regards
        The Soho Scheduler Team
        www.sohoappspot.com
    """ % (this_invite.entity_reference.name,this_invite.host_signup_reference.signup_user.email(),this_invite.access_right_code.name,this_invite.invite_email_address)

    #2. Mark as sent

    #3. Send email
    mailHelper = appcode.mailhelper.SohoMailHelper(toEmail=toEmail, strSubject=subject, strMessageBody=body)
    mailHelper.send()

    return None
