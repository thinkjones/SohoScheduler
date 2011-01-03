from appcode.dataserver import *
from django.core.urlresolvers import reverse
from google.appengine.ext import deferred
import about.helpers


def GetDashboard(  dashboard_id):
    dash = None
    try:
        dash = UserMessage.get(db.Key.from_path(Dashboard.kind(), int(dashboard_id)))
    except:
        dash = None
    return dash

def GetDashboardByUser(  signup):
    querySet = dashboard.models.Dashboard.gql("WHERE signup_reference = :1", signup)
    resultSet = querySet.fetch(1)
    if querySet.count(1) > 0:
        return resultSet[0]
    else:
        return None

def GetOrCreateNewDashBoardEntry(  this_signup):
    dashBoard = None
    dashBoard = GetDashboardByUser(this_signup)
    if dashBoard is None:
        dashBoard = dashboard.models.Dashboard()
        dashBoard.signup_reference = this_signup
        dashBoard.refresh_activity_type = 0
        dashBoard.put()

    return dashBoard

def MarkActivityAsRefreshed( this_signup):
    dashBoard = GetOrCreateNewDashBoardEntry(this_signup)
    dashBoard.refresh_activity_type = 0
    dashBoard.requires_refresh = True
    dashBoard.put()




def GetRecentActivityNoProcess(  signup):
    querySet = dashboard.models.DashboardRecentActivity.gql("WHERE signup_reference = :1 and show_to_user = :2 order by activity_date DESC", signup, True)
    resultSet = querySet.fetch(20)
    return resultSet

def DeleteAllActivity(  this_signup):
    q = db.GqlQuery("SELECT * FROM DashboardRecentActivity WHERE signup_reference = :1", this_signup)
    results = q.fetch(1000)
    db.delete(results)

def DeleteAllActivity(  this_signup):
    q = db.GqlQuery("SELECT * FROM DashboardRecentActivity WHERE signup_reference = :1", this_signup)
    results = q.fetch(200)
    db.delete(results)

def GetRecentActivity(  this_signup):
    return GetRecentActivityNoProcess(this_signup)

def log_action( request, application_zone, action_name, entity_id, activity_text,param_1=None ):
    #application_zone options, app, dash, appointment, crm, designer
    strURL = request.path
    log_activity(None, application_zone,action_name,strURL,entity_id, param_1, None,None,activity_text)

def log_activity(signup_ref, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user=False):
    #deferred.defer(log_activity_deferred, signup_ref, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user)
    log_activity_deferred(signup_ref, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user)
    return None

def log_activity_deferred(signup_ref, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user=False):
    
    this_signup = signup_ref or None
    if signup_ref == None:
        this_signup = DataServer().getMySignup()

    this_signup_id = 0
    if this_signup:
        this_signup_id = this_signup.key().id()
        
    this_user_email = None
    if users.get_current_user():
        this_user_email = users.get_current_user().email()
        
    #save_new_activity(this_signup_id, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user,this_user_email)
    deferred.defer(save_new_activity, this_signup_id, application_zone, action_name, action_url, entity_id, param_1, param_2, param_3, activity_text, show_to_user,this_user_email)
    return True
    
def save_new_activity(signup_id,application_zone,action_name,action_url,entity_id,param_1,param_2,param_3,activity_text,show_to_user,user_email ):
    
    #Get Signup
    this_signup = None
    if signup_id:
        if str(signup_id).isdigit():
            this_signup = ServerSignup().Get(signup_id)
    
    newEntry = dashboard.models.DashboardRecentActivity()
    newEntry.signup_reference = None
    newEntry.application_zone = application_zone
    newEntry.action_name = action_name
    newEntry.action_url = action_url
    newEntry.entity_id = str(entity_id)
    newEntry.param_1 = param_1
    newEntry.param_2 = param_2
    newEntry.param_3 = param_3
    newEntry.activity_text = activity_text
    newEntry.show_to_user = show_to_user
    newEntry.signup_reference = this_signup 
    newEntry.signup_user = None
    newEntry.signup_user_email = user_email
    newEntry.put()
    return True

def log_login(request, signup_ref):
    strURL = request.path
    activity_text = None
    if signup_ref:
        activity_text = "User %s signed In" % users.get_current_user()
    else:
        activity_text = "User %s signed In" % "[not specified]"

    log_activity(signup_ref, "app","login",strURL,None, None, None,None,activity_text)

def log_navigation( request, application_zone, entity_id, param_1=None):
    activity_text = None

    #application_zone options, app, dash, appointment, crm, designer
    if application_zone == "app":
        activity_text = "General application"
    if application_zone == "dash":
        activity_text = "Navigate to dashboard area"
    if application_zone == "appointment":
        activity_text = "Navigate to appointment schedule"
    if application_zone == "crm":
        activity_text = "Navigate to crm manager"
    if application_zone == "entityprofile":
        activity_text = "Navigate to entity profile"
    if application_zone == "applicationdesigner":
        activity_text = "Navigate to application designer manager"
    if application_zone == "sharemyapplication":
        activity_text = "Navigate to the Publish Template wizard"
    if application_zone == "newentitywizard":
        activity_text = "Opened the New Entity Wizard"
    if application_zone == "importgooglecontacts":
        activity_text = "Opened the Import Google Contacts Wizard"
    if application_zone == "openformdesignCRM":
        activity_text = "Opened form designer for the CRM system"
    if application_zone == "openformdesignAppointment":
        activity_text = "Opened form designer for the Appointment Schedule"

    log_action(request, application_zone,"index",entity_id, activity_text, param_1)

def log_action( request, application_zone, action_name, entity_id, activity_text,param_1=None ):
    #application_zone options, app, dash, appointment, crm, designer
    strURL = request.path
    signup_ref = DataServer().getMySignup();
    log_activity(signup_ref, application_zone,action_name,strURL,entity_id, param_1, None,None,activity_text)

def log_user_action( request, application_zone, action_name, entity_id, activity_text, param_1=None ):
    #application_zone options, app, dash, appointment, crm, designer
    strURL = None
    new_param_1 = param_1

    if request:
        strURL = request.path

    signup_ref = DataServer().getMySignup();

    if application_zone == "designer" and action_name == "jsonsaveform":
        strURL = "%s%s" %(reverse('designer.views.index', args=[entity_id]), "?tab=configuration")
    if application_zone == "newentitywizard" and action_name == "jsonProcessNewEntityWizard":
        strURL = "%s%s" %(reverse('dashboard.views.index', args=[entity_id]), "")
    if application_zone == "crm" and action_name == "jsonDeleteCRM":
        strURL = "%s%s" %(reverse('crm.views.index', args=[entity_id]), "")
    if application_zone == "postdata" and action_name == "ProcessSubmissionToParent":
        form_submission = param_1
        new_param_1 = str(form_submission.pkid)
        if form_submission.formType == 1:
            strURL = "%s%s" %(reverse('appointment.views.index', args=[entity_id]), "")
        if form_submission.formType == 2:
            strURL = "%s%s" %(reverse('crm.views.index', args=[entity_id]), "")

    log_activity(signup_ref, application_zone,action_name,strURL,str(entity_id), new_param_1, None,None,activity_text,True)


def GetOneHundredRecentActivities(last_record_id):
    #SELECT * FROM Entity where __key__ > Key('Entity', 90381) order by __key__
    str_last_record_id = str(last_record_id)
    strGQL = " where __key__ > Key('DashboardRecentActivity', %s) order by __key__ Limit 20 " % str_last_record_id
    querySet = dashboard.models.DashboardRecentActivity.gql(strGQL)
    results = querySet.fetch(20)
    return results

def GetFirstActivity():
    strGQL = " order by __key__ Limit 1 "
    querySet = dashboard.models.DashboardRecentActivity.gql(strGQL)
    results = querySet.fetch(1)
    if querySet.count(1) > 0:
        return results[0]
    else:
        return None

def GetStatByAppZoneActionName(this_signup, this_application_zone,this_action_name):
    querySet = dashboard.models.DashboardRecentActivitySummary.gql("Where signup_reference = :1 and application_zone = :2 and action_name = :3 ", this_signup, this_application_zone,this_action_name)
    results = querySet.fetch(1)
    this_stat = None
    if querySet.count(1) > 0:
        this_stat = results[0]
    else:
        this_stat = dashboard.models.DashboardRecentActivitySummary(signup_reference=this_signup, application_zone=this_application_zone,action_name=this_action_name)
    return this_stat
    
    