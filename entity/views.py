#from about.models import *
from appcode.viewsbaseclass import *
from appointment.models import *
from crm.models import *
from designer.views import mainSettingsHandler as designer_mainSettingsHandler
from entity.forms import *
from entity.models import *
from about.models import Signup
import about.helpers
import designer.helpers
import entity.helpers
import appcode.util

tabs_settings = {
    'main':				{'index':0, 'title':'Dashboard Overview'},
}

tab_selected = 'main'

#URL Mappings For Django
def index(sohoapp_id):
    asd=1
def docpost(sohoapp_id):
    asd=1
def formpost(sohoapp_id):
    asd=1
def docdesignpost(sohoapp_id):
    asd=1
def index2(sohoapp_id):
    asd=1
def new(sohoapp_id):
    asd=1
def edit(sohoapp_id):
    asd=1
def view(sohoapp_id):
    asd=1
def delete(sohoapp_id):
    asd=1
def jsonrequests(sohoapp_id):
    asd=1

#######################################################
### User Event - New
#######################################################
class EntityPage(SohoResponse):
    @sohosecurity.authenticate('Owner')
    def get(self,sohoapp_id):
            return _index(request, "0")

    def index2(request, entity_id):
            return _index(request, entity_id)

    def _index(request, entity_id):
        """Request / -- show all gifts."""
        """Request / -- show all gifts."""
        redirect_url = GetRedirectToDefaultDashboard(request, entity_id)
        if redirect_url:
            return self.redirect(redirect_url)
        user = users.GetCurrentUser()
        entitys = entity.helpers.HelperEntity().GetMyEntitys()

        template = 'entity/index'
        if IsAjaxRequest(self):
            template = 'entity/_main'

        tab_info = tabs_settings[tab_selected]

        sohoResponse = SohoResponse(request, template)
        sohoResponse.entitys = entitys
        sohoResponse.tabSelected = 'tabEntity'
        sohoResponse.signed_up = True
        sohoResponse.entity_id = entity_id
        sohoResponse.tab_info = tab_info
        sohoResponse.mode = 'Manage All Companies'
        return sohoResponse.respond()

    def new(request, entity_id):
            return edit(request, entity_id, 0)

    def edit(request, entity_id, edit_entity_id):
        #1. Init
        edit_entity = None
        this_entity = None

        if entity_id > 0:
            this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

        if int(edit_entity_id) > 0:
            edit_entity = appcode.dataserver.ServerEntity().Get(edit_entity_id)
            if edit_entity is None:
                return http.HttpResponseNotFound('No entity exists with that key (%r)' % edit_entity_id)

        #Get Form
        form = None #entityForm(data=request.POST or None, instance=edit_entity)

        #Choose template
        template = 'entity/edit'
        if IsAjaxRequest(self):
            template = 'entity/_Edit'

        tab_info = tabs_settings[tab_selected]

        #Prepare Response
        sohoResponse = SohoResponse(request, template)
        sohoResponse.entity = this_entity
        sohoResponse.edit_entity = edit_entity
        sohoResponse.tabSelected = 'tabEntity'
        sohoResponse.tab_info = tab_info
        sohoResponse.signed_up = True
        sohoResponse.entity_id = entity_id
        sohoResponse.edit_entity_id = edit_entity_id
        sohoResponse.form = form

        if not self.request.POST:
            return sohoResponse.respond()

        errors = form.errors
        if not errors:
            try:
                edit_entity = form.save(commit=False)
            except ValueError, err:
                errors['__all__'] = unicode(err)
        if errors:
            return sohoResponse.respond()

        #Save Record
        if not edit_entity.signup_reference:
            edit_entity.signup_reference = DataServer().getMySignup()
            edit_entity.is_admin = True
        edit_entity.put()

        edit_entity_id = edit_entity.key().id()

        if edit_entity.is_default == True:
            entity.helpers.HelperEntity().SetDefault(edit_entity_id)
        else:
            if appcode.dataserver.ServerEntity().GetEntityCount() == 1:
                entity.helpers.HelperEntity().SetDefault(edit_entity_id)

        return self.redirect('/entity/%s/dashboard' % edit_entity_id)
        #sohoResponse.redirect_to_url = '/entity/%s/dashboard' % edit_entity_id
        #return sohoResponse.respond()

    def view(request, entity_id, view_entity_id):
            #default
            this_entity = appcode.dataserver.ServerEntity().Get(view_entity_id)

            if request.method == 'GET':
                    message = ''

            sohoResponse = SohoResponse(request, 'entity/view')
            sohoResponse.entity = this_entity
            sohoResponse.tabSelected = 'tabEntity'
            sohoResponse.signed_up = True
            sohoResponse.entity_id = entity_id
            sohoResponse.view_entity_id = view_entity_id
            return sohoResponse.respond()

    def delete(request, entity_id, delete_entity_id):
            this_entity = appcode.dataserver.ServerEntity().Get(delete_entity_id)
            this_entity.active = False
            this_entity.put()

            if IsAjaxRequest(self):
                    sohoResponse = SohoResponse(request, "blank")
                    return sohoResponse.respond_blank()
            else:
                    return index2(request, entity_id)


class JsonRequests(SohoResponse):
    def post(self):
        strAction = self.request.POST['action']

        if strAction == "deleteentity":
            return self.jsonProcessDeleteEntity()
        if strAction == "invite_user_to_access_entity":
            return self.jsonInviteUserToAccess()
        if strAction == "delete_user_invite_or_access":
            return self.jsonDeleteUserInviteOrAccess()
        if strAction == "save_entity_profile":
            return self.jsonSaveEntityProfile()
        if strAction == "process_my_invite":
            return self.jsonProcessMyInvite()

    @sohosecurity.authenticate('Owner')
    def jsonProcessDeleteEntity(self):
        entity_id = self.request.POST['entity_id']
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

        responseVal = "No Accesss"

        EntityHasAccess = True #BEcause of decorator
        if EntityHasAccess:
            responseVal = "Access"
            entity.helpers.HelperSignupEntityAccess().deleteAccessAndEntity(this_entity)


        dictResponse = {'response': True, 'access_level': responseVal}
        return self.json_respond(dictResponse)

    def jsonInviteUserToAccess(self):
        entity_id = self.request.POST['entity_id']
        EntityHasAccess = entity.helpers.HelperEntity().CheckAccess(entity_id)
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        responseVal = "No Accesss"
        bolResponse = None
        this_invite_email_address = None
        this_access_right_code = None
        this_access_right_code_name = None
        already_exists = None

        if EntityHasAccess:
            #Get Data
            responseVal = "Access"
            bolResponse = False
            this_invite_email_address = self.request.POST['email_address']
            this_access_right_code_string = self.request.POST['access_right_code']
            this_access_right_code = entity.helpers.HelperAccessRightCode().getByMnemonic(this_access_right_code_string)
            this_access_right_code_name = this_access_right_code.name
            signup_ref = DataServer().getMySignup()
            new_invite = None
            already_exists = True

            #Create Invite
            if this_access_right_code:
                #Has this user already been emailed?
                new_invite = entity.helpers.HelperInviteEntityAccess().getByEmail(this_entity, this_invite_email_address)

                if new_invite is None:
                    already_exists = False
                    new_invite = InviteEntityAccess(host_signup_reference = signup_ref,
                                                    invite_email_address = this_invite_email_address,
                                                    entity_reference = this_entity,
                                                    access_right_code=this_access_right_code,
                                                    active=True)
                    new_invite.put()

            #If Invite Created Then Send Invite
            if new_invite is not None:
                entity.helpers.EmailUserWithAccessInvitation(new_invite)
                bolResponse = True

        dictResponse = {'response': bolResponse, 'access_level': responseVal,'email_address':this_invite_email_address,'access_right_code':this_access_right_code_name,'already_exists':already_exists}
        return self.json_respond(dictResponse)

    def jsonDeleteUserInviteOrAccess(self):
        entity_id = self.request.POST['entity_id']
        delete_user_invite_id = self.request.POST['delete_user_invite_id']
        user_type = self.request.POST['user_type']

        EntityHasAccess = entity.helpers.HelperEntity().CheckAccess(entity_id)
        responseVal = "No Accesss"

        if EntityHasAccess:
            responseVal = "Access"
            if user_type == 'current':
                appcode.dataserver.ServerSignupEntityAccess().Delete(delete_user_invite_id)
            if user_type == 'invite':
                appcode.dataserver.ServerInviteEntityAccess().Delete(delete_user_invite_id)

        dictResponse = {'response': True, 'access_level': responseVal}
        return self.json_respond(dictResponse)


    def jsonSaveEntityProfile(self):
        entity_id = self.request.POST['entity_id']
        EntityHasAccess = entity.helpers.HelperEntity().CheckAccess(entity_id)
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        responseVal = "No Accesss"

        if EntityHasAccess:
            #Get Data
            responseVal = "Access"
            bolResponse = True
            entity_form_data = simplejson.loads(self.request.POST['entity_form_data'])
            entity_form_dict = appcode.util.convert_list_to_dict(entity_form_data, 'name')
            this_entity.name = entity_form_dict['entity_name']['value']
            this_entity.desc = entity_form_dict['entity_desc']['value']
            this_entity.tags = entity_form_dict['entity_tags']['value']
            this_entity.is_default = False
            this_entity.put()

        dictResponse = {'response': True, 'access_level': responseVal}
        return self.json_respond(dictResponse)

    def jsonProcessMyInvite(self):
        #Get Info
        responseVal = "No Accesss"
        invite_id = self.request.POST['invite_id']
        invite_email_address = self.request.POST['invite_email']
        accept_invite = self.request.POST['accept_invite']
        bol_is_good = False

        #Get Invite
        this_invite = appcode.dataserver.ServerInviteEntityAccess().Get(invite_id)

        #Check it matches the email address to check against spoofing
        if this_invite.invite_email_address == invite_email_address:
            bol_is_good = True

        if bol_is_good:
            responseVal = "Access"
            entity.helpers.HelperInviteEntityAccess().ProcessInvite(this_invite,accept_invite)
            self.session['refresh_session'] = True

        dictResponse = {'response': True, 'access_level': responseVal}
        return self.json_respond(dictResponse)


class DocPostPage(SohoResponse):
    def post(self):
        #1. Authenticate
        submission_key = self.request.POST['submission_key']
        submission_id = self.request.POST['submission_id']

        fs = ServerFormSubmission().Get(submission_id)
        bolIsValid = False
        strError = ""
        if fs:
            if str(fs.key()) == submission_key:
                if fs.form_submitted == False:
                    fs.submitted = datetime.datetime.now()
                    fs.form_submitted = True
                    fs.put()
                    bolIsValid = True
                else:
                    strError = "Not Value: Already Submitted"
            else:
                strError = "Not Valud: Submission Key and ID Do not match error"
        else:
            strError = "Not Valud: Submission ID doesn't exit in db."


        if bolIsValid == False:
            jsonDict = {'response': bolIsValid,'error':strError}
            self.json_respond(jsonDict)

        #2.Insert Data
        listVals = simplejson.loads(self.request.POST['form_data'])
        #for dictKey in dictVals.keys():
        #    ffVal = FlexFieldValueTest(ffkey=dictKey, ffval=dictVals[dictKey])
        #    ffVal.put()
        #sss = FlexFieldValueTest.all()

        #3. Really insert data
        processValues = designer.helpers.ServerProcessPost(form_submission=fs,listVals=listVals)
        processValues.ProcessValues()

        #4. return Values back to client

        #jsontext = simplejson.dumps(sss)
        jsonDict = {'response': bolIsValid,'error':strError,'pkid':processValues.pkid,'mnemonic':processValues.mnemonic}
        self.json_respond(jsonDict)

class FormPostPage(SohoResponse):
    def post(self):
        template = 'designer/_form_post'
        sohoResponse = SohoResponse(request, template)
        return sohoResponse.respond()

class DocDesignPost(SohoResponse):
    def post(self):
        #1. Authenticate
        entity_key = request.GET['ekey']
        entity_id = request.GET['eid']
        signup_key = request.GET['skey']
        formType = request.GET['formtype']
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        signup_ref = appcode.dataserver.ServerSignup().Get(signup_key)
        bolIsValid = False
        form_to_update = None
        strError = ""
        if entity:
            if str(this_entity.key()) == entity_key:
                if str(this_entity.signup_reference.key()) == str(signup_key):
                    bolIsValid = True
                else:
                    strError = "Not Authorised 1 %s %s" % (this_entity.signup_reference.key(),signup_key)
            else:
                strError = "Not Authorised 2"
        else:
            strError = "Not Authorised 3"


        if bolIsValid == False:
            return HttpResponse(strError)
        else:
            #Get new design fields
            if formType.isdigit():
                formType = int(formType)
            form_to_update = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity,formType)
            ProcessDesignChanges(form_to_update)

        return formpost(self)
