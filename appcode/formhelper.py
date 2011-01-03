import google
from google.appengine.api.labs import taskqueue
from designer.models import *
from about.models import *
from entity.modesl import *
import entity.helpers
import designer.helpers

class FormHelper():
    def ProcessPost(self, entity_id, crm_id, formType, dictPOST):
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        formFields = designer.helpers.HelperFormDesignField().GetFormDesignFields(this_entity, formType)

        #1. Insert values into FlexFieldValue
        return None