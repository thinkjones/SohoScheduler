#from about.models import *
from appcode.viewsbaseclass import *
from designer.views import mainSettingsHandler as designer_mainSettingsHandler
from django.conf import settings

from appcode.dataserver import *
from about.application_models import *

import gdata.auth
import gdata.alt.appengine
import gdata.contacts.service


GOOGLE_CONTACTS_URI = 'http://www.google.com/m8/feeds/'

import dashboard.helpers
import entity.helpers
import crm.helpers
import entity.forms
import cgi
import about.helpers

CONSUMER_KEY = 'sohoplayground.appspot.com'
CONSUMER_SECRET = '8fgCiWmFYsOg2yKGbCAReWM7'
SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1

def jsonrequests():
    asd=1
def loadSyncWithGoogleWizard():
    asd=1

class CRMWizardPage(SohoResponse):
    def runwizard(self, entity_id, wizard_type):
        if wizard_type == "synchwithgoogle":
            return self.loadSyncWithGoogleWizard(entity_id)
        
    def post(self,entity_id):
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        strAction = self.request.POST['action']

        if strAction == "getgroupcontacts":
            return self.jsonGetGroupContacts(this_entity)
        if strAction == "savenewcontacts":
            return self.jsonSaveNewContacts(this_entity)

    def jsonGetGroupContacts(self, entity):
        #Get Group ID
        group_id = self.request.POST['group_id']

        #Get Contacts From Google
        group_contacts = self.get_oauth_contacts_feed( group_id)

        #Create Dictionary Of Values
        listContacts = []
        for i, entry in enumerate(group_contacts):
            #Get Email
            strEmail = ""
            for email in entry.email:
                if email.primary and email.primary == "true":
                    strEmail = email.address

            newContact = {"ContactID": entry.id.text, "ContactName": entry.title.text, "ContactEmail": strEmail}
            listContacts.append(newContact)

        dictResponse = {'response': True, 'results': listContacts}
        self.json_respond(dictResponse)

    def jsonSaveNewContacts(self,this_entity):
        self.request.encoding ='utf-8'
        newContacts = self.request.POST['newcontacts']
        newContactsDict = simplejson.loads(newContacts, encoding='utf-8')
        bolIsSharedToken = False
        if self.request.POST['IsSharedToken'] == "true":
            bolIsSharedToken = True

        #Was the token identified as being shared?
        current_signup = DataServer().getMySignup()
        access_token = about.helpers.HelperStoredToken().GetBySignupAndPurpose(current_signup,'GoogleContacts')
        if access_token:
            access_token.is_shared = bolIsSharedToken
            access_token.put()

        #Save New Contacts
        #This takes a while so defer the task
        crm.helpers.CreateAndUpdateContacts(this_entity,  newContactsDict,access_token)
        #crm.helpers.CreateAndUpdateContactsDefer(this_entity.key().id(),  newContactsDict,access_token.key().id())

        #Creater Json response
        dictResponse = {'response': True, 'new_contacts': str(10),'updated_contacts': str(5)}
        self.json_respond(dictResponse)
        
    def loadSyncWithGoogleWizard(self, entity_id):
        #Determine what stage we are in
        self.request.encoding = 'utf-8'


        #init
        url_stage_id = self.request.GET.get('stage','1')
        stage_id = 1
        access_token = None
        this_url = self.request.url
        current_signup = None

        #1. Does the URL have an uth token?
        oauth_token = gdata.auth.OAuthTokenFromUrl(this_url)
        if oauth_token:
            stage_id = 2

        #2. Do we have a token in the database?
        if url_stage_id == "1" or url_stage_id == "3":
            current_signup = DataServer().getMySignup()
            access_token = about.helpers.HelperStoredToken().GetBySignupAndPurpose(current_signup,'GoogleContacts')

        if access_token:
            stage_id = 3

        if url_stage_id == "-1":
            about.helpers.HelperStoredToken().RemoveToken(current_signup,'GoogleContacts')
            stage_id = 1
            #request.session['google_contacts_oauth_token_secret'] = None
            #request.session['google_contacts_oauth_token_key'] = None

        #2. Do we have an auth token in the session?
        #oauth_token_secret = request.session.get('google_contacts_oauth_token_secret')
        #oauth_token_key = request.session.get('google_contacts_oauth_token_key')


        #3. Return correct screen
        if stage_id == 1:
            return self.loadSyncWithGoogleWizard_Stage1(entity_id)
        if stage_id == 2:
            return self.loadSyncWithGoogleWizard_Stage2(entity_id)
        if stage_id == 3:
            return self.loadSyncWithGoogleWizard_Stage3(entity_id)




    def loadSyncWithGoogleWizard_Stage1(self, entity_id):
        #This is the pre-authentication stage

        #Get Client
        gd_client = self.get_ouath_client()
        req_token = gd_client.FetchOAuthRequestToken()
        gd_client.SetOAuthToken(req_token)

        #Get Token Info
        sync_wizard_url = reverse('crm.wizards.loadSyncWithGoogleWizard', args=[entity_id])
        env = self.request.environ
        http_host = env.get('HTTP_HOST')
        oauth_callback_url = 'http://%s%s?stage=2&oauth_token_secret=%s' % (http_host,sync_wizard_url, req_token.secret)
        approval_page_url = gd_client.GenerateOAuthAuthorizationURL(callback_url=oauth_callback_url, request_token=req_token)

        #Choose template
        template = 'crm/syncgooglewizard/_wizard'
        start_step_id = '0'

        crm_redirect_url = ('http://%s%s%s' % (http_host, reverse('crm.views.index', args=[entity_id]),""))
        

        #Prepare Response
        self.template = template
        self.tabSelected = 'tabDashboard'
        self.google_auth_url = approval_page_url
        self.LIVE_HOST_NAME = settings.LIVE_HOST_NAME
        self.HOST_NAME = settings.HOST_NAME
        self.current_step = start_step_id
        self.groups_feed = None
        self.contacts_feed = None
        self.entity_id = entity_id
        self.crm_redirect_url = crm_redirect_url

        return self.respond()


    def loadSyncWithGoogleWizard_Stage2(self, entity_id):
        #This is post-authentication - time to upgrade the token stage

        #init
        gd_client = self.get_ouath_client()
        this_url = self.request.url

        #Extracting the token from the callback URL
        authorized_token = gdata.auth.OAuthTokenFromUrl(this_url)
        if authorized_token:
            authorized_token.secret = cgi.escape(self.request.GET.get('oauth_token_secret'))
            authorized_token.oauth_input_params = gdata.auth.OAuthInputParams(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            gd_client.SetOAuthToken(authorized_token)
        else:
            print 'No oauth_token found in the URL'

        #Upgrading to an access token
        #gd_client.current_token = authorized_token
        gd_client.current_token = authorized_token
        gd_client.SetOAuthInputParameters(signature_method=SIG_METHOD, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        oauth_access_token = gd_client.UpgradeToOAuthAccessToken()
        #gd_client.SetOAuthToken(oauth_token=oauth_access_token)

        oauth_token_secret = oauth_access_token.secret
        oauth_token_key = oauth_access_token.key

        #If successful store all details in session
        #request.session['google_contacts_oauth_token'] = oauth_access_token.get_token_string()
        #request.session['google_contacts_oauth_token_secret'] = oauth_token_secret
        #request.session['google_contacts_oauth_token_key'] = oauth_token_key
        current_signup = DataServer().getMySignup()
        this_token = about.helpers.HelperStoredToken().GetBySignupAndPurpose(current_signup,"GoogleContacts")
        if this_token:
            this_token.token_string = oauth_access_token.get_token_string()
        else:
            this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
            this_token = about.application_models.StoredToken(purpose="GoogleContacts",token_string=oauth_access_token.get_token_string(),signup_reference=current_signup,entity_reference=this_entity)
        this_token.put()


        #Now move to stage 3 but this time create client with access
        #client.SetOAuthToken(oauth_access_token)
        #gd_client2 = get_ouath_client(self, True)
        ##sfeed = gd_client2.GetGroupsFeed()
        #contact_entries = sfeed.entry
        return self.loadSyncWithGoogleWizard_Stage3(entity_id)


    def loadSyncWithGoogleWizard_Stage3(self, entity_id):
        #Authentication stage
        gd_client = self.get_ouath_client(True)
        template = 'crm/syncgooglewizard/_wizard'
        groups_feed = None
        contacts_feed = None

        groups_feed = self.get_oauth_groups_feed()

        env = self.request.environ
        http_host = env.get('HTTP_HOST')
        crm_redirect_url = ('http://%s%s%s' % (http_host, reverse('crm.views.index', args=[entity_id]),""))


        #Prepare Response
        self.template = template
        self.tabSelected = 'tabDashboard'
        self.google_auth_url = None
        self.LIVE_HOST_NAME = settings.LIVE_HOST_NAME
        self.HOST_NAME = settings.HOST_NAME
        self.session_token = None
        self.current_step = "1"
        self.groups_feed = groups_feed
        self.contacts_feed = contacts_feed
        self.entity_id = entity_id
        self.crm_redirect_url = crm_redirect_url

        return self.respond()


    def get_ouath_client(self, bolAuthenticate=False):
        # set up service
        gd_client = gdata.contacts.service.ContactsService(source='sohoplaygound-appspot-com')
        gdata.alt.appengine.run_on_appengine(gd_client)
        gd_client.SetOAuthInputParameters(signature_method=SIG_METHOD, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)

        if bolAuthenticate:
            current_signup = DataServer().getMySignup()
            this_token = about.helpers.HelperStoredToken().GetBySignupAndPurpose(current_signup,"GoogleContacts")
            oauth_input_params = gdata.auth.OAuthInputParams(signature_method=SIG_METHOD, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            access_token = gdata.auth.OAuthToken(oauth_input_params=oauth_input_params)
            access_token_string = this_token.token_string
            access_token.set_token_string(access_token_string)
            gd_client.current_token = access_token

        return gd_client


    def get_oauth_groups_feed(self):
        #Get Token
        gd_client = self.get_ouath_client(True)
        sfeed = gd_client.GetGroupsFeed()
        contact_groups = sfeed.entry
        return contact_groups

    def get_oauth_contacts_feed(self, group_id):
        #Init Get Client Object
        gd_client = self.get_ouath_client(True)

        #Create Query Parameters to return more results
        query = gdata.contacts.service.ContactsQuery()
        query.max_results = 1000
        query['group'] = str(group_id)

        #sfeed = gd_client.GetContactsFeed()
        sfeed = gd_client.GetContactsFeed(query.ToUri())
        contact_entries = sfeed.entry
        return contact_entries

    def get_oauth_contact_feed(self, uri_contact_id):
        #Init Get Client Object
        gd_client = self.get_ouath_client(True)

        #Create Query Parameters to return more results
        query = gdata.contacts.service.ContactsQuery()
        query.max_results = 10

        #sfeed = gd_client.GetContactsFeed()
        sfeed = gd_client.GetContact(uri_contact_id)
        contact_entry = sfeed
        return contact_entry
