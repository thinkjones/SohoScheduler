from appcode.dataserver import *
from appcode.baseclass import *

class HelperSohoFormBuilder():

    def GetFormControls(self,idorkey):
        sohoformbuilder = ServerSohoFormBuilder().Get(idorkey)
        #using the form json return a list of fields and types
        strDict = sohoformbuilder.form_design_dict

        #Add things to string to make it able to be decoded by simplejson
        #strSJDict = '[name:"SohoFormBuilder",object:%s]' % strDict

        if strDict == "" or strDict is None:
            return None

        #Create Pythono class from JSON String.
        #newDict = ast.literal_eval(strDict)
        newDict = simplejson.loads(strDict)

        return newDict

    def CopySohoFormBuilder(self, srcFormRef):
        #1. Init
        formID = srcFormRef.key().id()
        srcForm = ServerSohoFormBuilder().Get(formID)
        newForm = sohoformbuilder.models.SohoFormBuilder(name=srcForm.name,description = srcForm.description,tags = srcForm.tags,form_design_dict=srcForm.form_design_dict)
        newForm = newForm.put()
        return newForm

    def ApplyRequiredFieldToFormDesignDict(self, form_design_dict, required_field_name):

        for ffKey in form_design_dict.keys():
            ff = form_design_dict[ffKey]
            if required_field_name == ff['label']:
                ff['required'] = "1"

        return form_design_dict

