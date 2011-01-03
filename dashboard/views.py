### Imports 
from appcode.viewsbaseclass import *
from designer.models import *

import entity.helpers
import message.helpers
import about.helpers
import dashboard.helpers

import appcode.sohonotify

tabs_settings = {'main':{'index':0, 'title':'Dashboard Overview'},}

tab_selected = 'main'

def change_entity():
    asd=1
def index():
    asd=1

#######################################################
### User Event - New
#######################################################
class DashboardPage(SohoResponse):
    #@sohosecurity.authenticate('View')
    def get(self,sohoapp_id):
        if str(sohoapp_id).isdigit():
            about.helpers.HelperSignupExtendedProfile().SetParam('default_entity_id',int(sohoapp_id))
        tab_info = None
        try:
            tab_info = tabs_settings[request.GET['tab']]
        except:
            tab_info = tabs_settings['main']

        if tab_info['index'] == 0:
            return self.index_dashboard(entity_id=sohoapp_id)

    def index_dashboard(self,entity_id):
        """Request / -- show all gifts."""
        redirect_url = self.GetRedirectToDefaultDashboard(entity_id)
        if redirect_url:
            self.redirect(redirect_url)

        #myentities = appcode.dataserver.ServerEntity().GetMyEntitys(entity_render_type=1)
        all_my_entities = entity.helpers.HelperSignupEntityAccess().GetMyEntitys()
        myentities_owner = entity.helpers.HelperSignupEntityAccess().FilterHelper(all_my_entities,1,'Owner',True)
        myentities_shared_access = entity.helpers.HelperSignupEntityAccess().FilterHelper(all_my_entities,1,'Owner',False)
        mytemplates = entity.helpers.HelperSignupEntityAccess().FilterHelper(all_my_entities,2,'Owner',True)
        this_email = users.GetCurrentUser().email()
        myinvites = entity.helpers.HelperInviteEntityAccess().getMyInvites(this_email)

        mymessages = message.helpers.HelperUserMessage().GetUserMessages()
        template = 'dashboard/index'
        if self.IsAjaxRequest():
            template = 'dashboard/_main'

        can_add_entity = True
        if len(myentities_owner) > 2:
            can_add_entity = False

        #Get Recenet Activity
        recentactivity = None
        this_user = DataServer().getMySignup()
        recentactivity = dashboard.helpers.GetRecentActivity(this_user)

        tab_info = tabs_settings[tab_selected]

        self.session['Gene'] = 'Gene is set in session'

        #Has the user used the designer?
        has_used_designer = False
        str_has_used_designer = about.helpers.HelperSignupExtendedProfile().GetParam('has_used_designer',this_user)
        if str_has_used_designer:
            if str_has_used_designer.param_value == 'Yes':
                has_used_designer = True
        else:
            about.helpers.HelperSignupExtendedProfile().SetParam('has_used_designer','No')

        dashboard.helpers.log_navigation(self.request, "dash", entity_id)

        self.template = template
        self.myentities_owner = myentities_owner
        self.myentities_shared_access = myentities_shared_access
        self.mytemplates = mytemplates
        self.myinvites = myinvites
        self.tab_info = tab_info
        self.can_add_entity = can_add_entity
        self.recentactivity = recentactivity
        self.mymessages = mymessages
        self.has_used_designer = has_used_designer
        self.tabSelected = 'tabDashboard'
        self.signed_up = True
        self.entity_id = entity_id
        self.session_test = self.session['Gene']
        return self.respond()





class NewUserPage(SohoResponse):
    @sohosecurity.authenticate('View')
    def get(self):
        self.template = 'dashboard/newuser'
        this_email = users.GetCurrentUser().email()
        self.myinvites = entity.helpers.HelperInviteEntityAccess().getMyInvites(this_email)
        return self.respond()

class GotoNewApplication(SohoResponse):
    def get(self, sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        if this_entity:
            this_message = "You are now using application: %s" % this_entity.name
            self.showNotification(this_message)
        self.session['current_entity_id'] = sohoapp_id
        strURL = "%s%s" %(reverse('dashboard.views.index', args=[sohoapp_id]), "")
        return self.redirect(strURL)

class ApplicationFormHandler4(SohoResponse):
    def get(self, sohoapp_id, form_type, action, id):
        if form_type == "crm" and action == "view":
            import crm.views
            form_renderer = crm.views.CRMPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.view(sohoapp_id,id)

        if form_type == "crm" and action == "edit":
            import crm.views
            form_renderer = crm.views.CRMPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.edit(sohoapp_id,id)

        if form_type == "crm" and action == "edit":
            import crm.views
            form_renderer = crm.views.CRMPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.edit(sohoapp_id,id)

        if form_type == "appointment" and action == "edit":
            import appointment.views
            form_renderer = appointment.views.AppointmentPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.edit(sohoapp_id,id)

        if form_type == "designer" and action == "wizards" and id == "publishtemplate":
            import designer.wizards
            form_renderer = designer.wizards.PublishTemplateWizardPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.runwizard(sohoapp_id)

        if form_type == "crm" and action == "wizard" and id == "synchwithgoogle":
            import crm.wizards
            form_renderer = crm.wizards.CRMWizardPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.runwizard(sohoapp_id,'synchwithgoogle')

        if form_type == "designer" and action == "byformtype":
            import designer.views
            form_renderer = designer.views.DesignerPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            if id == "1": return form_renderer.designAppointment(sohoapp_id)
            if id == "2": return form_renderer.designCRM(sohoapp_id)


        self.response.out.write("ApplicationFormHandler4: sohoapp_id: %s, form_type: %s, action: %s, id: %s" %(sohoapp_id,form_type,action,id))

    def post(self, sohoapp_id, form_type, action, id):
        if form_type == "designer" and action == "wizards" and id == "jsonrequests":
            import designer.wizards
            form_renderer = designer.wizards.PublishTemplateJson()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.post(sohoapp_id)

        self.response.out.write("ApplicationFormHandler4:POST: sohoapp_id: %s, form_type: %s, action: %s, id: %s" %(sohoapp_id,form_type,action,id))


class ApplicationFormHandler3(SohoResponse):
    def get(self, sohoapp_id, form_type, action):
        can_render = False
        if form_type == "crm" and action == "new":
            import crm.views
            form_renderer = crm.views.CRMPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.new(sohoapp_id)

        if form_type == "appointment" and action == "new":
            import appointment.views
            form_renderer = appointment.views.AppointmentPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.new(sohoapp_id)

        if action == "design":
            import designer.views
            form_renderer = designer.views.DesignerPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            if form_type == "appointment": return form_renderer.designAppointment(sohoapp_id)
            if form_type == "crm": return form_renderer.designCRM(sohoapp_id)

        if form_type == "crm" and action == "jsonselect":
            import crm.views
            form_renderer = crm.views.CRMPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.jsonselect(sohoapp_id)

        self.response.out.write("ApplicationFormHandler3: sohoapp_id: %s, form_type: %s, action: %s" %(sohoapp_id,form_type,action))

    #Does home page type actions for a particular form
    def post(self, sohoapp_id, form_type, action):
        form_renderer = None
        if form_type == "appointment" and action == "jsonrequests":
            import appointment.views
            form_renderer = appointment.views.AppointmentJsonPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.post(sohoapp_id)

        if form_type == "crm" and action == "jsonrequests":
            import crm.views
            form_renderer = crm.views.CRMJsonPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.post(sohoapp_id)

        if form_type == "sohoformbuilder" and action == "jsonrequests":
            import sohoformbuilder.views
            form_renderer = sohoformbuilder.views.SohoFormbuilderJsonPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.post(sohoapp_id)

        if form_type == "settings" and action == "invitedusers":
            import designer.views
            form_renderer = designer.views.DesignerPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.index_permissions_invitedusers(sohoapp_id)

        if form_type == "designer" and action == "updatedsettings":
            import designer.views
            form_renderer = designer.views.DesignerPage()
            form_renderer.request = self.request
            form_renderer.response = self.response
            return form_renderer.updatedsettings(sohoapp_id)

        self.response.out.write("ApplicationFormHandler3:POST: sohoapp_id: %s, form_type: %s, action: %s" %(sohoapp_id,form_type,action))

class ApplicationFormHandler2(SohoResponse):
    #Does home page type actions for a particular form
    def get(self, sohoapp_id, form_type):

        #if we get here then response has not been made.
        self.response.out.write( "ApplicationFormHandler2: sohoapp_id: %s, form_type: %s" %(sohoapp_id,form_type))