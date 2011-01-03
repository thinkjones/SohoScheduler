from appcode.viewsbaseclass import *

import appcode.mailhelper
import about.helpers
import dashboard.helpers
import gdata.alt.appengine
import gdata.service
import gdata.contacts
import gdata.contacts.service
import gdata.auth

#URL Mappings For Django
def index():
    asd=1
def jsoncontactus():
    asd=1

class LandingPage(SohoResponse):
    def get(self):
        if users.GetCurrentUser():
            return self.index_logged_in()
        else:
            return self.index_not_logged_in()

    def index_logged_in(self):
        #Perform login process
        current_signup = about.helpers.CreateUser()
        company_entity = entity.helpers.HelperEntity().GetDefaultEntity(self.request)
        #current_signup = DataServer().getMySignup()
        current_signup.modified = datetime.datetime.now()
        current_signup.put()
        #dashboard.helpers.log_login(None,current_signup)
        access_rights = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()

        self.session['refresh_session'] = True
        self.session['access_rights'] = access_rights

        if company_entity is None:
            #Attempt to get a default entity from Signup Entity List
            ea = entity.helpers.HelperSignupEntityAccess().GetMyEntitysFirst()
            if ea:
                company_entity = ea.entity_reference

        #Redirect to the appropriate dashboard
        redirect_url = '/newuser/'
        if company_entity:
            redirect_url = '/application/%s/' % (company_entity.key().id())
        self.redirect(redirect_url)
        
    def index_not_logged_in(self):
        #2. Not logged in
        self.template = 'about/landing'
        self.tabSelected = 'tabLanding'
        self.signed_up = False
        self.company_id = 0
        self.logged_in_required = False
        return self.respond()

class ContactUsPage(SohoResponse):
    def post(self):
        curuser = users.GetCurrentUser()
        signup_ref = DataServer().getMySignup()
        inquiry_type = self.request.POST['inquiry_type']
        inquiry_details = self.request.POST['inquiry_details']
        http_referer = self.request.environ.get('HTTP_REFERER', '')
        cus = about.models.ContactUs(
                signup_user=curuser,
                signup_ref=signup_ref,
                http_referer=http_referer,
                inquiry_type=inquiry_type,
                inquiry_details=inquiry_details

            )
        cus.put()

        #Email Information
        strSubject="Quick Contact Inquiry from %s.  Signup:[%s], InquiryRef:[%s]" % (curuser.email(),signup_ref.key().id(),cus.key().id())
        strMessageBody = """
            %s

            http_referer: %s

            Type:%s

            Details: %s
            """  % (strSubject,http_referer, inquiry_type,inquiry_details)
        emailer = appcode.mailhelper.SohoMailHelper(fromEmail="admin@sohoappspot.com",toEmail="admin@sohoappspot.com",strSubject=strSubject,strMessageBody=strMessageBody)
        emailer.send()

        jsontext = {'response': True}
        return self.json_respond(jsontext)


def info(request, entity_id):
    sohoResponse = SohoResponse(request, 'about/index')
    sohoResponse.tabSelected = 'tabAbout'
    return infopages(entity_id,  sohoResponse)

def feedback(request, entity_id):
    sohoResponse = SohoResponse(request, 'about/feedback')
    sohoResponse.tabSelected = 'tabFeedback'
    return infopages(entity_id,  sohoResponse)

def infopages(entity_id,  sohoResponse):
	#	return http.HttpResponseRedirect('http://info.sohoappspot.com')
	#0. Determine whether user has signed up	
	user = users.GetCurrentUser()
	signed_up = False
	entity_count = appcode.dataserver.ServerEntity().GetEntityCount()
	if user:
		signed_up = True

	this_entity = None
	if entity_id:
		this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

	#template = 'about/index'
	#if request.method == 'GET':
	#	template = 'about/index'

	#sohoResponse = SohoResponse(request, template)
	sohoResponse.company = this_entity
	sohoResponse.signed_up = signed_up
	sohoResponse.entity_id = entity_id
	sohoResponse.logged_in_required = True
	return sohoResponse.respond()

def signup(request):
	#0.Init
	user = users.GetCurrentUser()
	signed_up = False
	company = None
	company_count = 0

	#1. Check for user logged in ?
	if user:
		company_count = svrCompany.GetCompanyCount()
		signed_up = True
		company = about.helpers.ServerSignup().PerformSignupProcess()
		return self.redirect('/company/%r/schedule/' % (int(company.key().id())))
	else:
		#1. Check for user and record user
		return self.redirect(users.CreateLoginURL(request.path))



def googleauth(request):
    # Get Entity
    entity_id = request.GET.get('entity_id','0')

    #Get Token
    authsub_token_string = unicode(request.GET['token'])
    self.setSessionVal('google_contacts_session_token', authsub_token_string)

    #Upgrade token with existing client
    gd_client = gdata.contacts.service.ContactsService()
    gdata.alt.appengine.run_on_appengine(gd_client)
    asToken = gdata.auth.AuthSubToken()
    asToken.set_token_string(authsub_token_string)
    gd_client.UpgradeToSessionToken(asToken)
    sfeed = gd_client.GetGroupsFeed()
    sfeed_entry = sfeed.entry

    #Do it with a new client
    gd_client2 = gdata.contacts.service.ContactsService()
    gdata.alt.appengine.run_on_appengine(gd_client2)
    asToken2 = gdata.auth.AuthSubToken()
    asToken2.set_token_string(authsub_token_string)

    sfeed2 = gd_client2.GetGroupsFeed()
    sfeed2_entry = sfeed2.entry
    
    #Return to regular URL
    redirect_url = "%s%s" %(reverse('crm.wizards.loadSyncWithGoogleWizard', args=[entity_id]), "?stage=1&token=%s" % authsub_token_string)
    return self.redirect(redirect_url)

def errorpage(request,access_rights):
    template = 'about/errorpage'
    sohoResponse = SohoResponse(request, template)
    sohoResponse.tabSelected = 'tabDasboard'
    sohoResponse.logged_in_required = False
    sohoResponse.error_access_rights = access_rights
    return sohoResponse.respond()
