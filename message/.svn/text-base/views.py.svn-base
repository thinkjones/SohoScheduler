### Imports 
from appcode.viewsbaseclass import *

### Data
from message.models import *
import message.helpers

### User Events
def hidethis(request,  message_id):
	#Get user and message_id
	svrUM = message.helpers.ServerUserMessage()
	ServerUserMessage().MarkMessageAsRead(message_id)
	sohoResponse = SohoResponse(request, "blank")
	return sohoResponse.respond_blank()

