from appcode.viewsbaseclass import *
import urllib
import entity.helpers
import crm.helpers
import dashboard.helpers
import designer.helpers
import crm.wizards

tabs_settings = {'main':				{'index':0, 'title':'Customer Relationship Management (CRM)'},}


def index():
    asd=1
def new():
    asd=1
def quickadd():
    asd=1
def edit():
    asd=1
def view():
    asd=1
def delete():
    asd=1
def jsonselect():
    asd=1
def submit():
    asd=1
def viewinfo():
    asd=1
def jsonrequests():
    asd=1


class CRMPage(SohoResponse):
    @sohosecurity.authenticate('View')
    def get(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        crms = crm.helpers.HelperCRM().GetEntityCRMs(this_entity)
        crms_count = len(crms)

        self.template = 'crm/index'
        if self.IsAjaxRequest():
            self.template = 'crm/_main'

        jsoncrms = ServerCRM().GetByEntityJsonDict(this_entity,['name'],crms)
        jsontext = simplejson.dumps({'response': True, 'results': jsoncrms})

        dashboard.helpers.log_navigation(self.request, "crm", sohoapp_id)

        logging.debug(self.template)

        tab_info = tabs_settings['main']

        self.entity = this_entity
        self.customers = crms
        self.jsoncrms = jsontext
        self.crms_count = crms_count
        self.entity_id = sohoapp_id
        self.tabSelected = 'tabCRM'
        self.tab_info = tab_info

        return self.respond()

    @sohosecurity.authenticate('Edit')
    def new(self,sohoapp_id):
        return self.runtimeform(sohoapp_id,  0)

    def runtimeform(self,sohoapp_id, crm_id):
        #sohoformbuilder.views.runtime

        #Init
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        this_crm = None

        if int(crm_id) > 0:
            this_crm = ServerCRM().Get(crm_id)
            if this_crm is None:
                return http.HttpResponseNotFound('No CRM exists with that key (%r)' % crm_id)

        formtype = designer.helpers.HelperFormDesign().formTypes['TypeCRM']
        default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, formtype)
        sohoformbuilderid = default_form.sohoformbuilder_reference.key().id()

        submission = designer.helpers.HelperFormSubmission().Create(sohoapp_id,2,crm_id)
        submission_key = str(submission.key())
        submission_id = submission.key().id()

        import sohoformbuilder.views
        form_renderer = sohoformbuilder.views.SohoFormBuilderPage()
        form_renderer.request = self.request
        form_renderer.response = self.response
        return form_renderer.sohoruntime(sohoapp_id,sohoformbuilderid,submission_id,submission_key)
        #return sohoformbuilder_views_sohoruntime(self.request,sohoapp_id,sohoformbuilderid,submission_id,submission_key)

    def view(self, sohoapp_id, crm_id):
        this_crm = appcode.dataserver.ServerCRM().Get(crm_id)
        fs = this_crm.form_submission_ref
        ffvs = designer.helpers.HelperFlexFieldValue().GetValuesBySubmission(fs)

        #Has Google Information?
        external_system_id = None
        contact_entry = None
        bol_can_show_google_info = False
        if this_crm.external_system_id is not None:
            #Can we show this information
            current_signup = DataServer().getMySignup()
            bol_can_show_google_info = False

            #Did this user download this information?
            if this_crm.stored_token_ref:
                if this_crm.stored_token_ref.signup_reference == current_signup:
                    bol_can_show_google_info = True
                else:
                    #Is this information shared
                    bol_can_show_google_info = this_crm.stored_token_ref.is_shared

            if bol_can_show_google_info:
                external_system_id = this_crm.external_system_id

                form_renderer = crm.wizards.CRMWizardPage()
                form_renderer.request = self.request
                form_renderer.response = self.response
                contact_entry = form_renderer.get_oauth_contact_feed(external_system_id)



        self.template = 'crm/_crm_info'
        self.crm = this_crm
        self.ffvs = ffvs
        self.can_show_google = bol_can_show_google_info
        self.entity_id = sohoapp_id
        self.contact_entry = contact_entry
        return self.respond()


    def sidebar(request, entity_id):
            this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
            self.request = request
            self.template = 'crm/sidebar'
            return self.respond()


    def quickadd(request, entity_id):
        return edittemplate(request, entity_id, 0, 'crm/quickadd')

    @sohosecurity.authenticate('Edit')
    def edit(self,  entity_id,  crm_id):
        return self.runtimeform(entity_id,  crm_id)

    def submit(self, entity_id):
        return self.get(entity_id)

    def delete(request, entity_id, crm_id):
        crm_this_entity = CRM.get(db.Key.from_path(CRM.kind(), int(crm_id)))
        crm_this_entity.active = False
        crm_this_entity.put()
        return index(request,  entity_id)

    def jsonselect(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        obj_list = []
        lookup = self.request.GET['q']
        crms = crm.helpers.HelperCRM().FilterCRMs(this_entity, lookup)

        for obj in crms:
            strCreated = str(obj.created.strftime("%A %B %d, %Y"))
            strName = obj.name or "Not Specified"
            obj_list.append({'id':obj.key().id(), 'value': strName,'info': str('Created %s' % strCreated)},  )

        json_data = {"results":obj_list}
        return self.json_respond(json_data)

    def viewinfo(request, entity_id, crm_id):
        this_crm = appcode.dataserver.ServerCRM().Get(crm_id)
        fs = this_crm.form_submission_ref
        ffvs = designer.helpers.HelperFlexFieldValue().GetValuesBySubmission(fs)

        #Has Google Information?
        external_system_id = None
        contact_entry = None
        bol_can_show_google_info = False
        if this_crm.external_system_id is not None:
            #Can we show this information
            current_signup = DataServer().getMySignup()
            bol_can_show_google_info = False

            #Did this user download this information?
            if this_crm.stored_token_ref:
                if this_crm.stored_token_ref.signup_reference == current_signup:
                    bol_can_show_google_info = True
                else:
                    #Is this information shared
                    bol_can_show_google_info = this_crm.stored_token_ref.is_shared

            if bol_can_show_google_info:
                external_system_id = this_crm.external_system_id
                contact_entry = crm.wizards.get_oauth_contact_feed(request, external_system_id)


        self.request = request
        self.template = 'crm/_crm_info'
        self.crm = this_crm
        self.ffvs = ffvs
        self.can_show_google = bol_can_show_google_info
        self.entity_id = entity_id
        self.contact_entry = contact_entry
        return self.respond()

class CRMJsonPage(SohoResponse):
    def post(self,sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        strAction = self.request.POST['action']

        if strAction == "searchcrm":
            return self.jsonsimplesearch(this_entity,strAction)
        if strAction == "removefilter":
            return self.jsonsimplesearch(this_entity,strAction)
        if strAction == "deletecrm":
            return self.jsonDeleteCRM(this_entity,strAction)

    @sohosecurity.authenticate('View')
    def jsonsimplesearch(self, this_entity, strAction):
        apply_filter=True
        if strAction == "removefilter":
            apply_filter = False
        search_text = self.request.POST['simplesearch']
        crms_filtered = None
        if apply_filter:
            crms_filtered = crm.helpers.HelperCRM().FilterCRMs(this_entity, search_text)
        else:
            crms_filtered = crm.helpers.HelperCRM().GetEntityCRMs(this_entity)
        crms = ServerCRM().GetByEntityJsonDict(this_entity,['name'],crms_filtered)   #Second parameter is a list of fields that are returned to viewing.

        jsontext = {'response': True, 'action': strAction, 'results': crms}
        return self.json_respond(jsontext)
    
    @sohosecurity.authenticate('Edit')
    def jsonDeleteCRM(self, this_entity, strAction):

        #Check Access
        entity_id = this_entity.key().id()
        this_entityHasAccess = entity.helpers.HelperEntity().CheckAccess(entity_id)
        responseVal = "No Accesss"

        if this_entityHasAccess:
            responseVal = "Access"

            crm_id = self.request.POST['crm_id']
            crm_this_entity = appcode.dataserver.ServerCRM().Get(crm_id)
            crm_this_entity.active = False
            crm_this_entity.put()
            activity_text = "Contact deleted [%s]" % crm_this_entity.name
            dashboard.helpers.log_user_action(self.request,"crm","jsonDeleteCRM", entity_id, activity_text, crm_id)


        dictResponse = {'response': True, 'access_level': responseVal}
        return self.json_respond(dictResponse)
    