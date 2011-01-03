#from about.models import *
from appcode.viewsbaseclass import *
from django.core.urlresolvers import reverse
from designer.views import mainSettingsHandler as designer_mainSettingsHandler
from entity.forms import *
import dashboard.helpers
import entity.helpers
import about.helpers

def publishTemplateWizard():
    asd=1
def jsonrequests():
    asd=1
    
class PublishTemplateWizardPage(SohoResponse):
    def runwizard(self,sohoapp_id):

        #1. Get Current Entity
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)

        #Choose template
        template = 'designer/publishtemplate/_wizard'

        dashboard.helpers.log_navigation(self.request, "publishtemplatewizard", "0")

        #Prepare Response
        self.template = template
        self.tabSelected = 'tabDesigner'
        self.entity_id = sohoapp_id
        self.entity = this_entity
        return self.respond()

class PublishTemplateJson(SohoResponse):
    def post(self, sohoapp_id):
        strAction = self.request.POST['action']

        if strAction == "publishtemplate":
            return self.jsonProcessPublishTemplateWizard(sohoapp_id)

    def jsonProcessPublishTemplateWizard(self,sohoapp_id):
        #Get new entity details
        newentity = self.request.POST['newtemplate']
        newentityDict = simplejson.loads(newentity)

        #Get Source Entity Template
        source_entity_id = newentityDict['source_entity_id']
        source_entity = appcode.dataserver.ServerEntity().Get(source_entity_id)

        #Save New Entity Template
        this_signup = DataServer().getMySignup()
        new_entity = Entity(name=newentityDict['title'],desc=newentityDict['description'],tags = newentityDict['tags'])
        new_entity.signup_reference = this_signup
        new_entity.entity_render_type = entity.helpers.HelperEntity().entityTypes['TypeEntityTemplate']
        new_entity.derived_from_entity = source_entity
        new_entity.is_admin = False
        new_entity.put()
        new_entity_id = new_entity.key().id()

        #Store new entity in session
        #request.session['new_entity_id'] = new_entity_id
        new_entity_url = reverse('dashboard.views.index', args=[new_entity_id])

        #Create a copy of this companies form designs and create new entity
        #TaskQueueHelper().CreateCopyEntityTask(entity_id, entity_template_id)
        entity.helpers.CreateTemplateFromEntity(sohoapp_id,new_entity_id)

        activity_text = "Template created [%s]" % newentityDict['title']
        dashboard.helpers.log_user_action(self.request,"publishtemplatewizard","jsonProcessPublishTemplateWizard", new_entity_id, activity_text, "0")

        #Refresh user access information
        entity.helpers.HelperSignupEntityAccess().analyzeUserProfileAndCreateUserAccessRights(this_signup)
        self.session['access_rights'] = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()

        #Creater Json response
        dictResponse = {'response': True, 'new_entity_id': str(new_entity_id),'new_entity_url':new_entity_url}
        return self.json_respond(dictResponse)
