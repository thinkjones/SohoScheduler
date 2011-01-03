from appcode.dataserver import *
from appcode.viewsbaseclass import *
from google.appengine.api import users
import sohoadmin.helpers

PAGE_SIZE = 20

#######################################################
### User Events
#######################################################
def cronjobs(request,  cronjob):
	strMessage = "Start Job <br />"
	strMessage += "Started: %s <br />" % cronjob
	if cronjob == "RunFriendlyURL":
		strMessage = strMessage + RunFriendlyURL()
	if cronjob == "ProcessActivityStats":
		strMessage = strMessage + ProcessActivityStats()
	strMessage += "Finished: %s <br />" % cronjob
	
	return HttpResponse(strMessage)
	
def ProcessActivityStats():
	
	#Get APplication Parameter FOr Last Stats Processed
	last_record_processed  = sohoadmin.helpers.HelperApplicationParams().GetParam('recent_activity_last_record_processed')
	if last_record_processed is None:
		last_record_processed  = 0
		sohoadmin.helpers.HelperApplicationParams().SaveParam('recent_activity_last_record_processed',"0")
	
	# if last processed is 0 get the first record
	last_record_processed = dashboard.helpers.GetFirstActivity()
	
	#Get 100 records of recent activity
	recent_activities =  dashboard.helpers.GetOneHundredRecentActivities(last_record_processed.key().id())
	for each_activity in recent_activities:
		this_signup = each_activity.signup_reference
		this_application_zone = each_activity.application_zone 
		this_action_name = each_activity.action_name
		last_record_processed = each_activity.key().id()
		if this_signup:
			#Get Existing Total
			this_stat = dashboard.helpers.GetStatByAppZoneActionName(this_signup, this_application_zone,this_action_name)
			this_stat.total_count = this_stat.total_count + 1
			this_stat.put()
		
		sohoadmin.helpers.HelperApplicationParams().SaveParam('recent_activity_last_record_processed',str(last_record_processed))

	return "Finished %s" % str(last_record_processed)
	
				
def RunFriendlyURL():
	query = ListMap.all()
	listmaps = query.fetch(1000)
	strMessage = None
	for listmap in listmaps:
	  listmap_id = listmap.key().id()
	  ServerListMap().CreateFriendlyURL(listmap_id)
	  strMessage = "%s %s processed to %s<br />" % (strMessage,  listmap_id, listmap.friendly_url)
	return strMessage
