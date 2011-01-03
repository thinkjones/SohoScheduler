from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.api import users
from appcode.sohodatamodels import *

class ServerEveryone():
	def GetPublicTimeline(self,  page_id,  page_size):
		offset = str(page_id * page_size)
		strGQL = "SELECT * FROM ListMap ORDER BY created DESC LIMIT %s OFFSET %s" % (page_size,  offset)
		listmaps = db.GqlQuery(strGQL)
		return listmaps
