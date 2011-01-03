#from about.models import *
from appcode.viewsbaseclass import *
from designer.views import mainSettingsHandler as designer_mainSettingsHandler
#from entity.forms import *
import dashboard.helpers
import entity.helpers
import about.helpers
from entity.models import *

def NewEntityWizard():
    asd=1
def loadNewEntityWizard():
    asd=1/0
def jsonrequests():
    asd=1
def gotonewapplication():
    asd=1
def gotonewentity():
    asd=1
    
class NewEntityWizard(SohoResponse):
    def get(self):
        #1. Get High Quality Templates
        entities = entity.helpers.HelperEntityRating().GetHighQualityTemplates()
        ec = entities.count()

        #Choose template
        template = 'dashboard/newentitywizard/_wizard'
        dashboard.helpers.log_navigation(self.request, "newentitywizard", "0")

        #Prepare Response
        self.template = template
        self.tabSelected = 'tabDashboard'
        self.entities = entities
        self.respond()

class GotoNewEntity(SohoResponse):
    def get(self, action_name=None):
        if action_name == "gotonewapplication": self.gotonewapplication()

    def gotonewapplication(self):
        entity_id = 0
        session_new_entity_id = self.session.get('new_entity_id',0)
        if session_new_entity_id:
            entity_id = session_new_entity_id

        redirect_url = None
        if entity_id is None:
            redirect_url = reverse('/')
        else:
            redirect_url = reverse('dashboard.views.index', args=[entity_id])
        return self.redirect(redirect_url)


class JsonRequests(SohoResponse):
    def post(self):
        strAction = self.request.POST['action']
        if strAction == "savenewentity":
            return self.jsonProcessNewEntityWizard()

    def jsonProcessNewEntityWizard(self):
        #Get new entity details
        #newEntityWizardValues = '{"templateID": "50","templateName": "test","title": "test","description": "test","tags": "tags"}'
        #newEntityWizardValues = '{"formdesign":{"0":{"id":"0","pos":0,"parentcontrol":"pa_0","type":"text","label":"Customer","help":"Please enter the customer name.","defaultoption":"","choices":{}}}}'
        newentity = self.request.POST['newentity']
        newentityDict = simplejson.loads(newentity)

        #Get Entity Template
        entity_template_id = newentityDict['templateID']

        #Save New Entity
        this_signup = DataServer().getMySignup()
        new_entity = Entity(name=newentityDict['title'],desc=newentityDict['description'],tags = newentityDict['tags'])
        new_entity.signup_reference = this_signup
        new_entity.entity_render_type = entity.helpers.HelperEntity().entityTypes['TypeEntityRegular']
        new_entity.is_admin = False
        new_entity.put()
        new_entity_id = new_entity.key().id()

        #redirect to new web page
        #request.session['new_entity_id'] = new_entity_id
        new_entity_url = reverse('dashboard.views.index', args=[new_entity_id])

        #Create a copy of this companies form designs and create new entity
        entity.helpers.CreateEntityFromTemplate(entity_template_id, new_entity_id)

        activity_text = "Entity created [%s]" % newentityDict['title']
        dashboard.helpers.log_user_action(self.request,"newentitywizard","jsonProcessNewEntityWizard", new_entity_id, activity_text, "0")

        #Refresh user access information
        entity.helpers.HelperSignupEntityAccess().analyzeUserProfileAndCreateUserAccessRights(this_signup)
        self.session['access_rights'] = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()

        #Creater Json response
        self.session['refresh_session'] = True
        dictResponse = {'response': True, 'new_entity_id': str(new_entity_id),'new_entity_url':new_entity_url}
        self.json_respond(dictResponse)



def updatedsettings(request, entity_id):
    #jsontext = serializers.serialize("json", {'response': True})
    this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

    entity_access_rights = appcode.sohosecurity.getEntityAccessRights(request, entity_id)
    EntityHasAccess = entity_access_rights['Owner']

    responseVal = "No Accesss"

    if EntityHasAccess:
        responseVal = "Access"
        default_field = request.POST['default_field']
        if request.POST['form_type'] == 1:
            ServerEntityParams().SaveParam(this_entity, "AppointmentDateDefaultField", default_field)
        else:
            ServerEntityParams().SaveParam(this_entity, "CustomerNameDefaultField", default_field)

    #jsontext = simplejson.dumps({'response': True, 'access_level': responseVal})
    jsontext = {'response': True, 'access_level': responseVal}
    return HttpResponse(jsontext, "application/json")

