# This script installs the necessary static data for version 7.
from google.appengine.api import urlfetch
from appcode.baseclass import *
from sohoadmin.models import *
from crm.models import *
from appointment.models import *
from entity.models import *
from designer.models import *
from sohoformbuilder.models import *
from appcode.taskqueuehelper import *
import about.helpers
import entity.helpers
import designer.helpers
import sohoadmin.helpers

default_application_parameters = {
    'mail_send_rule':'test',
    'test_mail_account':'test@thinkjones.co.uk',
    'mail_send_from_email':'admin@sohoappspot.com',
    'basic_entity_id':'0'
}

def runInstall07():
    ##############################################################################
    # 1 - Install Application Parameters
    current_params = {}
    results = sohoadmin.helpers.HelperApplicationParams().GetAllBase()
    for foo in results:
        current_params[foo.param_name] = foo.param_value
    default_params = default_application_parameters
    for dParamKey in default_params.keys():
        if current_params.has_key(dParamKey) == False:
            newAppParam = ApplicationParams(param_name=dParamKey,param_value=default_application_parameters[dParamKey])
            newAppParam.put()

    ##############################################################################
    #2. Get Admin User
    signup_ref = about.helpers.ServerSignup().getSignupByUser(users.GetCurrentUser())


    ##############################################################################
    #3. Create Basic Entity Template
    strMnemonic = "BasicEntityTemplate"
    #Check if already exists before creating
    blankentity = None
    entitys = entity.helpers.HelperEntity().GetEntitysByMnemonic(mnemonic=strMnemonic)

    if entitys.count() > 0:
        blankentity = entitys[0]
    else:
        blankentity = Entity(name = "Basic Application",desc = "Basic starter application easily modifiable by users.",tags = "basic")
        
    blankentity.active = True
    blankentity.derived_from_entity = None
    blankentity.desc = "Basic starter application easily modifiable by users."
    blankentity.entity_render_type = 2
    blankentity.is_admin = False
    blankentity.is_collaborator = False
    blankentity.is_default = False
    blankentity.is_high_quality_template = True
    blankentity.is_readonly = True
    blankentity.name = "Basic Application"
    blankentity.signup_reference = signup_ref
    blankentity.tags = "basic"
    blankentity.mnemonic = strMnemonic
    #blankentity.frevvo_application_id = GetGParam("frevvo_hq_templates_application_id")
    blankentity.put()

    ##############################################################################
    #4. Create SohoFormBuilder Apppointment
    dictAppointmentForm = """{"formdesign":{"0":{"id":"0","pos":0,"parentcontrol":"pa_3","controlType":"customer","displayType":"autocomplete","required":0,"label":"Customer","help":"Please select the customer.  Start typing to show filtered list.","defaultoption":"","choices":{}},"1":{"id":"1","pos":1,"parentcontrol":"pa_2","controlType":"date","displayType":"date","required":"1","label":"Booking Date","help":"The date of service.","defaultoption":"","choices":{}},"2":{"id":"2","pos":2,"parentcontrol":"pa_1","controlType":"textarea","displayType":"textarea","required":0,"label":"Booking Details","help":"Please enter the job details.","defaultoption":"","choices":{}}}}"""
    sohoAppointmentForm = SohoFormBuilder(name='Appointment Form',description='Appointment Form',tags='Appointment Form',form_design_dict=dictAppointmentForm)
    sohoAppointmentForm.put()


    ##############################################################################
    #4. Create SohoFormBuilder CRM
    dictCRMForm = """{"formdesign":{"0":{"id":"0","pos":0,"parentcontrol":"pa_0","controlType":"text","displayType":"text","label":"Customer","help":"Please enter the customer name.","defaultoption":"","choices":{}}}}"""
    sohoCRMForm = SohoFormBuilder(name='CRM Form',description='CRM Form',tags='CRM Form',form_design_dict=dictCRMForm)
    sohoCRMForm.put()

    ##############################################################################
    #2.5 Set Rating on entity so it appearsin HQ templates
    entity.helpers.HelperEntityRating().ChangeTemplateRating(blankentity.key().id(), 10)

    #3. Create Customer Form
    newFormForTemplateCRM = None
    newFormForTemplateCRM = designer.helpers.HelperFormDesign().GetByEntityAndFormType(blankentity,2)
    if newFormForTemplateCRM is None:
        newFormForTemplateCRM = FormDesign()
    newFormForTemplateCRM.formType = 2
    newFormForTemplateCRM.entity_reference = blankentity
    #newFormForTemplate.frevvo_application_id = GetGParam("frevvo_hq_templates_application_id")
    #newFormForTemplate.frevvo_formtype_id = "_QcAaMGA3Ed6_kL1DdfAfQg!_OP-AcWA3Ed6_kL1DdfAfQg!thinkjones3"
    newFormForTemplateCRM.sohoformbuilder_reference = sohoCRMForm
    newFormForTemplateCRM.put()

    #3. Create Appointment Form
    newFormForTemplateApp = None
    newFormForTemplateApp = designer.helpers.HelperFormDesign().GetByEntityAndFormType(blankentity,1)
    if newFormForTemplateApp is None:
        newFormForTemplateApp = FormDesign()
    newFormForTemplateApp.formType = 1
    newFormForTemplateApp.entity_reference = blankentity
    #newFormForTemplate.frevvo_application_id = GetGParam("frevvo_hq_templates_application_id")
    #newFormForTemplate.frevvo_formtype_id = "_t6pIt2HHEd6_kL1DdfAfQg!_OP-AcWA3Ed6_kL1DdfAfQg!thinkjones3"
    newFormForTemplateApp.sohoformbuilder_reference = sohoAppointmentForm
    newFormForTemplateApp.put()

    #3. Get Form Fields Extracted
    designer.helpers.ProcessDesignChanges(newFormForTemplateCRM)
    designer.helpers.ProcessDesignChanges(newFormForTemplateApp)

    #4. Create Entity Params
    entity.helpers.HelperEntityParams().SaveParam(blankentity,'AppointmentDateDefaultField','Booking Date')
    entity.helpers.HelperEntityParams().SaveParam(blankentity,'AppointmentCRMDefaultField','Customer')
    entity.helpers.HelperEntityParams().SaveParam(blankentity,'CustomerNameDefaultField','Customer')
    #Update params with ids from forms
    entity.helpers.BespokeEntityParamsUpdate(blankentity, newFormForTemplateCRM, newFormForTemplateApp)

    #4. Create a task to check all entities has forms and designs
    entities = Entity.all()
    for this_entity in entities:
        if this_entity.mnemonic <> "BasicEntityTemplate":
            TaskQueueHelper().CreateCheckEntityForForms(this_entity.key().id())
