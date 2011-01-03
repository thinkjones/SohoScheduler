# Main View Import
from appcode.viewsbaseclass import *
from appcode.sohodatamodels import *
from appcode.taskqueuehelper import *
from entity.forms import *
from entity.helpers import *
from designer.helpers import *
import logging
logging.logMultiprocessing = 0
import sys
import getopt
import getpass
import atom
import gdata.service
import appcode.sohosecurity
from django.utils import simplejson

import sohoformbuilder.views
import gdata
from gdata.alt.appengine import run_on_appengine

import entity.helpers
import crm.helpers
import dashboard.helpers

gd_client = None

tabs_settings = {
    'profile':		{'index':0, 'title':'Profile'},
    'configuration':    {'index':1, 'title':'Configuration'},
    'permissions':      {'index':2, 'title':'Access Permissions'},
}

tab_selected = 'main'
def index():
    asd=1
def index_permissions_currentusers():
    asd=1
def index_permissions_invitedusers():
    asd=1
def index_permissions():
    asd=1
def designCRM():
    asd=1
def designAppointment():
    asd=1
def designForms():
    asd=1
def updatedsettings():
    asd=1
    
#######################################################
### Main Web Page Access Points
#######################################################
class DesignerPage(SohoResponse):
    @sohosecurity.authenticate('Owner')
    def get(self, sohoapp_id):
        return self.get_post(sohoapp_id)

    def post(self,sohoapp_id):
        return self.get_post(sohoapp_id)

    def get_post(self,sohoapp_id):
        tab_info = None
        try:
            tab_name = self.request.GET['tab']
            tab_info = tabs_settings[tab_name]
        except:
            tab_info = tabs_settings['profile']

        if tab_info['index'] == 0:
            dashboard.helpers.log_navigation(self.request, "entityprofile", sohoapp_id)
            return self.designerProfile(sohoapp_id)

        if tab_info['index'] == 1:
            dashboard.helpers.log_navigation(self.request, "applicationdesigner", sohoapp_id,tab_info['title'])
            return self.designForms(sohoapp_id)

        if tab_info['index'] == 2:
            dashboard.helpers.log_navigation(self.request, "entity.views.shareapplication", sohoapp_id,tab_info['title'])
            return self.index_permissions(sohoapp_id)

    def designerProfile(self, sohoapp_id):
        # Init
        this_entity = None
        tab_selected = 'tabDesigner'
        tab_info = tabs_settings['profile']
        bolIsAJaxRequest = self.IsAjaxRequest()

        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        if this_entity is None:
            return http.HttpResponseNotFound('No entity exists with that key (%r)' % sohoapp_id)

        #Choose template
        template = 'designer/index'
        if bolIsAJaxRequest:
            template = 'designer/_profile'

        #Get Form
        #form = entityForm(data=request.POST or None, instance=this_entity)

        #Prepare Response
        self.template = template
        self.entity = this_entity
        self.tabSelected = tab_selected
        self.tab_info = tab_info
        self.entity_id = sohoapp_id
        self.respond()

    def designForms(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)

        template = 'designer/index'
        if self.IsAjaxRequest():
            template = 'designer/_configuration'

        #Get Form designs
        appFormDesign = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity,HelperFormDesign().formTypes['TypeReservationCalendar'])
        crmFormDesign = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity,HelperFormDesign().formTypes['TypeCRM'])
        appointDateFields = designer.helpers.HelperFormDesignField().GetFormDesignFieldsByType(appFormDesign, "date")
        appointCustomerFields = designer.helpers.HelperFormDesignField().GetFormDesignFieldsByType(appFormDesign, "customer")
        crmTextFields = designer.helpers.HelperFormDesignField().GetFormDesignFieldsByType(crmFormDesign, "text")

        #Check length of fields if 0 then they should be refreshed
        if appointDateFields.count() == 0:
            ProcessDesignChanges(appFormDesign)
        if crmTextFields.count() == 0:
            ProcessDesignChanges(crmFormDesign)

        #Get Entity Params
        defaultAppDate = entity.helpers.HelperEntityParams().GetParam(this_entity,'AppointmentDateDefaultField')
        defaultAppCRM = entity.helpers.HelperEntityParams().GetParam(this_entity,'AppointmentCRMDefaultField')
        defaultCRMText = entity.helpers.HelperEntityParams().GetParam(this_entity,'CustomerNameDefaultField')
        defaultCRMEmail = entity.helpers.HelperEntityParams().GetParam(this_entity,'CustomerEmailDefaultField')

        tab_selected = 'configuration'
        tab_info = tabs_settings[tab_selected]

        self.template = template
        self.entity = this_entity
        self.entity_id = sohoapp_id
        self.tab_info = tab_info
        self.tabSelected = "tabDesigner"
        self.title = "Form Designer"
        self.appointDateFields = appointDateFields
        self.appointCustomerFields = appointCustomerFields
        self.crmTextFields = crmTextFields
        self.defaultAppDate = defaultAppDate
        self.defaultAppCRM = defaultAppCRM
        self.defaultCRMText = defaultCRMText
        self.defaultCRMEmail = defaultCRMEmail
        self.respond()


    def index_permissions(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        current_users_with_access = entity.helpers.HelperSignupEntityAccess().getByEntity(this_entity,True)
        current_users_with_invites = entity.helpers.HelperInviteEntityAccess().getByEntity(this_entity)
        template = 'dashboard/index'
        if self.IsAjaxRequest():
            template = 'dashboard/_UserAccess'

        tab_info = tabs_settings['permissions']

        self.template = template
        self.current_users_with_access = current_users_with_access
        self.current_users_with_invites = current_users_with_invites
        self.tab_info = tab_info
        self.tabSelected = 'tabEntity'
        self.entity_id = sohoapp_id
        return self.respond()

    def index_permissions_invitedusers(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        current_users_with_invites = entity.helpers.HelperInviteEntityAccess().getByEntity(this_entity)
        template = 'dashboard/_UserAccess_Invited'
        self.template = template
        self.current_users_with_invites = current_users_with_invites
        self.tabSelected = 'tabEntity'
        self.entity_id = sohoapp_id
        return self.respond()

    def index_permissions_currentusers(request, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        current_users_with_access = entity.helpers.HelperSignupEntityAccess().getByEntity(this_entity,True)
        template = 'dashboard/_UserAccess_CurrentUsers'
        self.template = template
        self.current_users_with_access = current_users_with_access
        self.tabSelected = 'tabEntity'
        self.entity_id = sohoapp_id
        return self.respond()

    @sohosecurity.authenticate('Owner')
    def designAppointment(self, entity_id):
        dashboard.helpers.log_action(self.request,"designer","designAppointment", entity_id, "Open appointment designer.")
        return self.indexFormDesign(entity_id, designer.helpers.HelperFormDesign().formTypes['TypeReservationCalendar'])

    @sohosecurity.authenticate('Owner')
    def designCRM(self, entity_id):
        dashboard.helpers.log_action(self.request,"designer","designCRM", entity_id, "Open CRM designer.")
        return self.indexFormDesign(entity_id, designer.helpers.HelperFormDesign().formTypes['TypeCRM'])

    def indexFormDesign(self, entity_id, formType=HelperFormDesign().formTypes['TypeReservationCalendar']):
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        signup = DataServer().getMySignup()

        default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, formType)
        if default_form is None:
            CreateBasicApplicationForExistingEntity(entity_id)
            default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, formType)

        if default_form.sohoformbuilder_reference is None:
            CreateBasicApplicationForExistingEntity(entity_id)
            default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, formType)
        sohoformbuild_id = default_form.sohoformbuilder_reference.key().id()

        import sohoformbuilder.views
        form_renderer = sohoformbuilder.views.SohoFormBuilderPage()
        form_renderer.request = self.request
        form_renderer.response = self.response
        return form_renderer.sohodesigntime(entity_id,sohoformbuild_id)

    @sohosecurity.authenticate('Owner')
    def updatedsettings(self, entity_id):

        this_entity = ServerEntity().Get(entity_id)
        entity_access_rights = appcode.sohosecurity.getEntityAccessRights(entity_id)
        EntityHasAccess = entity_access_rights['Owner']

        responseVal = "No Accesss"

        if EntityHasAccess:
            responseVal = "Access"
            default_field = self.request.POST['default_field']
            default_field_name = self.request.POST['default_field_name']
            entity.helpers.HelperEntityParams().SaveParam(this_entity, default_field_name, default_field)

            #Ensure any mandatory fields are set in required flag.
            designer.helpers.ApplyMandatoryRequiredFields(entity_id, 1)
            designer.helpers.ApplyMandatoryRequiredFields(entity_id, 2)

        dashboard.helpers.log_action(self.request,"designer","updatedsettings", entity_id, "Save entity settings.")

        jsontext = {'response': True, 'access_level': responseVal}
        self.json_respond(jsontext)


def designByType(request, entity_id, form_type_id):
    form_type_id = int(form_type_id)
    return indexFormDesign(request, entity_id, form_type_id)

def mainSettings(request, entity_id):
    redirect_if_new = False
    if entity_id == '0':
        redirect_if_new = True
    return mainSettingsHandler(request, entity_id, 0, redirect_if_new)

def newEntityWizard(request, entity_id):
    return mainSettingsHandler(request, entity_id, 0, True)


        
def mainSettingsHandler(request, entity_id, template_entity_id, redirect_if_new ):
    #1. Init
    from_template_chooser = False
    edit_entity = None
    this_entity = None
    edit_entity_id = entity_id
    if int(template_entity_id) > -1:
        from_template_chooser = True

    tab_selected = 'main'
    tab_info = tabs_settings[tab_selected]

    if entity_id > 0:
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

    if int(edit_entity_id) > 0:
        edit_entity = appcode.dataserver.ServerEntity().Get(edit_entity_id)
        if edit_entity is None:
            return http.HttpResponseNotFound('No entity exists with that key (%r)' % edit_entity_id)

    #Get Form
    #form = entityForm(data=request.POST or None, instance=edit_entity)

    #Choose template
    template = 'designer/index'
    if IsAjaxRequest(request):
        template = 'designer/_main_settings'

    #Prepare Response
    sohoResponse = SohoResponse(request, template)
    sohoResponse.title = "Main Settings"
    sohoResponse.sortfield = "mainsettings"
    sohoResponse.entity = this_entity
    sohoResponse.edit_entity = edit_entity
    sohoResponse.tabSelected = 'tabDesigner'
    sohoResponse.tab_info = tab_info
    sohoResponse.signed_up = True
    sohoResponse.entity_id = entity_id
    sohoResponse.edit_entity_id = edit_entity_id
    sohoResponse.from_template_chooser = from_template_chooser
    #sohoResponse.form = form
    sohoResponse.formType = 0

    if not request.POST:
        return sohoResponse.respond()

    errors = form.errors
    if not errors:
        try:
            edit_entity = form.save(commit=False)
        except ValueError, err:
            errors['__all__'] = unicode(err)
    if errors:
        return sohoResponse.respond()

    is_new_record = True
    if entity_id < 1:
        is_new_record = False

    #Save Record
    if not edit_entity.signup_reference:
        edit_entity.signup_reference = DataServer().getMySignup()
        edit_entity.is_admin = True
    edit_entity.put()

    edit_entity_id = edit_entity.key().id()

    if edit_entity.is_default == True:
        ServerEntity().SetDefault(edit_entity_id)
    else:
        if ServerEntity().GetEntityCount() == 1:
            ServerEntity().SetDefault(edit_entity_id)

    if is_new_record and from_template_chooser:
        CreateFormsForEntityIfBasedOnTemplate(edit_entity_id, template_entity_id)

    if redirect_if_new:
        sohoResponse.redirect_to_url = '/entity/%s/dashboard' % edit_entity_id
    return sohoResponse.respond()

def CreateFormsForEntityIfBasedOnTemplate(entity_id, template_entity_id):
    #1. Get Signup Reference
    signup_reference = DataServer().getMySignup()

    #2. Create new entity based on this template
    new_entity = entity.helpers.HelperEntity().CreateEntityFromTemplate(entity_id, template_entity_id,signup_reference)

    #3. new entity id
    entity_id = new_entity.key().id()

    return entity_id

def GetFormTitle(formType=HelperFormDesign().formTypes['TypeReservationCalendar']):
	strRet = None
	if formType == 0:
		strRet = "Main Entity Settings"
	if formType == designer.helpers.HelperFormDesign().formTypes['TypeReservationCalendar']:
		strRet = "Appointment Form Design"
	if formType == designer.helpers.HelperFormDesign().formTypes['TypeCRM']:
		strRet = "CRM Form Design"
	return strRet

def shareMyDesign(request, entity_id):
	return shareMyDesignWizard(request, entity_id, 0, "0")
	
def shareMyDesignWizard(request, entity_id, entity_template_id, stage_id):
    #1. Init
    this_entity = None
    entity_template = None
    stage_id = str(stage_id)

    if entity_id > 0:
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
    if entity_template_id > 0:
        entity_template = appcode.dataserver.ServerEntity().Get(entity_template_id)

    if int(entity_id) > 0:
        if this_entity is None:
            return http.HttpResponseNotFound('No entity exists with that key (%r)' % entity_id)

    if int(entity_template_id) > 0:
        if entity_template is None:
            return http.HttpResponseNotFound('No entity exists with that key (%r)' % entity_template_id)

    #Get Form
    #form = entityForm(data=request.POST or None, instance=entity_template)

    #Choose template
    template = 'designer/sharemydesignwizard/_manager'
    if IsAjaxRequest(request):
        template = 'designer/sharemydesignwizard/_manager'

    #Prepare Response
    sohoResponse = SohoResponse(request, template)
    sohoResponse.entity_id = entity_id
    sohoResponse.entity_template_id = entity_template_id
    sohoResponse.entity = this_entity
    sohoResponse.edit_entity = entity_template
    sohoResponse.tabSelected = 'tabDesigner'
    #sohoResponse.form = form
    sohoResponse.wizardstage = stage_id

    if not request.POST or stage_id == 0 or stage_id == 2:
        return sohoResponse.respond()

    errors = form.errors
    if not errors:
        try:
            entity_template = form.save(commit=False)
        except ValueError, err:
            errors['__all__'] = unicode(err)
    if errors:
        return sohoResponse.respond()

    #Save Record
    this_signup = DataServer().getMySignup()
    if not entity_template.signup_reference:
        entity_template.signup_reference = this_signup
    entity_template.entity_render_type = entity.helpers.HelperEntity().entityTypes['TypeEntityTemplate']
    entity_template.is_admin = True
    entity_template.put()
    entity_template_id = entity_template.key().id()

    #Create a copy of this companies form designs and create new entity
    #TaskQueueHelper().CreateCopyEntityTask(entity_id, entity_template_id)
    entity.helpers.CreateTemplateFromEntity(entity_id,entity_template_id)

    entity.helpers.HelperSignupEntityAccess().analyzeUserProfileAndCreateUserAccessRights(this_signup)
    request.session['access_rights'] = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()


    #CreateTemplateFromEntity(entity_id, entity_template_id)
    sohoResponse.wizardstage = "2"

    return sohoResponse.respond()
	
	
#edits, creates a new form version or creates a new form from template or from scratch
#TODO: check the ownership of the editing form
#TODO: data validation

def edit(request, entity_id, form_id, formType):
    #if not request.POST:
        #return http.HttpResponseRedirect('/entity/%r/designer/' % (int(entity_id)))

    #TODO: make use of templates
    template = 2
    form_type = int(formType)
    entity = appcode.dataserver.ServerEntity().Get(entity_id)
    form_id = int(form_id)
    new_form = int(request.POST['new_form_version'])
    is_default = int(request.POST['is_default'])

    #edit a existing form or create a new form
    if form_id > 0 and new_form == 0:
        custom_form = designer.helpers.HelperFormDesign().GetFormDesign(form_id)
        if custom_form  is None:
            return http.HttpResponseNotFound('No Form exists with that key (%r)' % form_id)
    else:
        custom_form = designer.models.FormDesign()
        custom_form.formType = form_type
        custom_form.derived_from = designer.helpers.HelperFormDesign().GetFormDesign(form_id)

    custom_form.xhtmlCode = '';#TODO: build this from fields JSON
    custom_form.fieldsJSON = request.POST['fieldsJSON']

    #custom_form.template = template #TODO: make this work
    #is this the default form?
    custom_form.is_default = bool(is_default)

    #identity data
    custom_form.creator = users.GetCurrentUser()
    custom_form.entity_reference = entity

    #get the current default form to make it !default
    default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(entity, formtype)

    #save to database
    if (custom_form.put() and default_form and default_form.key() != custom_form.key()):
        default_form.is_default = False
        default_form.put()

    #TODO: set a success message here
    if (is_default):
        if (form_type == designer.helpers.HelperFormDesign().formTypes['TypeReservationCalendar']):
            #return http.HttpResponseRedirect('/entity/%r/designer/appointment/' % (int(entity_id)))
            return designAppointment(request, entity_id)
        else:
            #return http.HttpResponseRedirect('/entity/%r/designer/crm/' % (int(entity_id)))
            return designCRM(request, entity_id)
    else:
        return self.redirect('/entity/%r/designer/%r/%r/edit/' % (int(entity_id), custom_form.key().id(), form_type))

def submit(request, entity_id):
    entity = appcode.dataserver.ServerEntity().Get(entity_id)

        #if we get some data lets save it
    if request.POST:
        form = designer.helpers.HelperFormDesign().GetFormDesign(request.POST['hid_form_id'])

        for field_name in request.POST:
            field_value = request.POST[field_name]
            if field_name[:3] == 'hid':
                continue
            #first try edit
            form_values = designer.models.FlexFieldValue().GetField(form, field_name, '')
            if form_values is None:
                form_values = designer.models.FlexFieldValue() #did not found an existing one, so crate new
            form_values.fieldName = field_name
            #TODO: save in appropriate column, based on field type
            form_values.value_string = field_value

            form_values.form = form

            #TODO: add appointment
            form_values.put()


    default_form = designer.helpers.HelperFormDesign().defaultForm(entity)

    #TODO: if we have a crm select make it work :D
    #TODO: get form with selected values
    form_values = designer.models.FlexFieldValue().GetFields(default_form, '')

    if form_values is not None:
        for field in form_values:
            field_name = field.fieldName
            field_value = field.value_string
            #input type="text" values
            default_form.xhtmlCode = default_form.xhtmlCode.replace(
                'name="' + field_name + '"',
                'name="' + field_name + '"'
                ' value="' + field_value + '"',)


    template = 'designer/submit_data'

    sohoResponse = SohoResponse(request, template)
    sohoResponse.entity = entity
    sohoResponse.tabSelected = "tabDesigner"
    sohoResponse.signed_up = True
    sohoResponse.entity_id = entity_id

    sohoResponse.default_form = default_form
    sohoResponse.form_id = default_form.key().id()
    return sohoResponse.respond()

def delete(request):
    return None



def processdesignchanges(request, entity_id, form_id):
    #formdesign_id is the key().id() value from the database
    formdesign = appcode.dataserver.ServerFormDesign().Get(form_id)
    if formdesign is None:
        return index(entity_id)
    #security does this entity match the form otherwise spoofing maybe happening.
    form_entity_id = formdesign.entity_reference.key().id()
    if str(form_entity_id) != entity_id:
        return index(request, entity_id)

    #2. Process Form Changes.
    ProcessDesignChanges(formdesign)

    #3. Return
    return index(request, entity_id)

def jsonrequests(request,entity_id):
    this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
    strAction = request.POST['action']

    if strAction == "save_entity_profile":
        return None
