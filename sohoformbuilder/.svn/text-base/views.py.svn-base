from appcode.viewsbaseclass import *
from sohoformbuilder.models import *
import entity.helpers
import crm.helpers
import designer.helpers
import dashboard.helpers
import sohoformbuilder.helpers

form_titles  = {
                    '1':{'name':'Appointment'},
                    '2':{'name':'Client'}
                }

def jsonrequests():
    asd=1

class SohoFormBuilderPage(SohoResponse):
    @sohosecurity.authenticate('View')
    def sohoruntime(self, sohoapp_id, sohoformbuild_id,submission_id,submission_key):
        #assume loading by ajax
        formbuilder = appcode.dataserver.ServerSohoFormBuilder().Get(sohoformbuild_id)
        template = 'sohoformbuilder/runtime'
        if self.IsAjaxRequest():
            template = 'sohoformbuilder/_runtime'
        formdesigndict = formbuilder.form_design_dict
        fs = designer.helpers.HelperFormSubmission().AuthSubmissionKeyAndID(submission_key,submission_id)
        form_data = None
        form_type = 0
        if fs:
            pkid = fs.pkid
            dictResults = designer.helpers.getCurrentFormDataFromNewSubmission(submission_id)
            form_data = simplejson.dumps(dictResults)
            form_type = fs.formType

        #form_design_data = simplejson.loads(formdesigndict)
        #form_design_data = simplejson.dumps(form_design_data)
        form_name = 'Form Entry'
        if fs.formType == 1:
            form_name = 'Opened appointment form'
        if fs.formType == 2:
            form_name = 'Opened crm form'

        dashboard.helpers.log_action(self.request,"designer","sohoruntime", sohoapp_id, form_name)

        entity_access_rights = appcode.sohosecurity.SohoSecurityHelper().getEntityAccessRights(sohoapp_id)


        self.template = template
        self.submission_key = submission_key
        self.submission_id = submission_id
        self.formbuilder = formbuilder
        self.form_design_data = formdesigndict
        self.form_data = form_data
        self.template = template
        self.sohoapp_id = sohoapp_id
        self.form_name = form_name
        self.form_type = form_type
        self.entity_access_rights = entity_access_rights

        return self.respond()


    ### Renders the form designer to the screen
    def sohodesigntime(self, sohoapp_id, sohoformbuild_id):
        formbuilder = appcode.dataserver.ServerSohoFormBuilder().Get(sohoformbuild_id)
        template = 'sohoformbuilder/builder'
        formdesigndict = formbuilder.form_design_dict

        dashboard.helpers.log_action(self.request,"designer","sohoformbuilder_index", str(sohoapp_id), "Opened form designer", str(sohoformbuild_id))


        self.template = template
        self.formbuilder = formbuilder
        self.template = template
        self.sohoapp_id = sohoapp_id
        self.form_design_data = formdesigndict
        return self.respond()


    def runtime(self, sohoapp_id, sohoformbuild_id):
        submission_id = self.request.GET['submission_id']
        submission_key = self.request.GET['submission_key']

        return sohoruntime(self.request, sohoapp_id, sohoformbuild_id,submission_id,submission_key)

class SohoFormbuilderJsonPage(SohoResponse):
    def post(self,sohoapp_id):
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        strAction = self.request.POST['action']
        #return jsonloadform(request, 617)

        if strAction == "getFormData":
            return self.jsonloadform(this_entity)
        if strAction == "saveFormData":
            return self.jsonsaveform(this_entity)
        if strAction == "getFormSubmissionData":
            return self.jsonloadformData(this_entity)
        if strAction == "getFullFormData":
            return self.jsonGetFullFormData(this_entity)


    def jsonGetFullFormData(self,this_entity):
        #This is the latest Json request that gets all data required for displaying forms.

        #Init
        form_type = self.GetInt(self.request.POST['form_type'])
        form_data_record_id = self.GetInt(self.request.POST['data_record_id'])

        #Get Form Name
        form_name = form_titles[str(form_type)]['name']
        if form_data_record_id > 0:
            form_name = 'Edit %s' % form_name
        else:
            form_name = 'Add %s' % form_name

        #Get Form Design Data
        form_design = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity,form_type)
        form_design_dict = form_design.sohoformbuilder_reference.form_design_dict
        form_design_dict = simplejson.loads(form_design_dict)
        form_design_dict.keys().sort()

        form_design_record_id = form_design.key().id()

        #Get Form Submission Information
        sohoapp_id = this_entity.key().id()
        fs = designer.helpers.HelperFormSubmission().Create(sohoapp_id,form_type,form_data_record_id)
        submission_key = str(fs.key())
        submission_id = fs.key().id()

        #Get Form to Load Data
        form_data_dict = None
        if form_data_record_id > 0:
            form_data_dict = designer.helpers.HelperFlexFieldValue().getCurrentValuesBySubmissionIDAsDict(fs,form_data_record_id)

        #Create Json Dictionary
        jsonDict ={
                        'response': True,
                        'form_name':form_name,
                        'form_design_record_id':form_design_record_id,
                        'form_design_data':form_design_dict,
                        'form_data_record_id': form_data_record_id,
                        'form_data':form_data_dict,
                        'submission_key':submission_key,
                        'submission_id':submission_id,
                        'form_type':form_type
                }
        return self.json_respond(jsonDict)

    def jsonloadform(self,this_entity):
        sohoformbuild_id = self.request.POST['form_id']
        formbuilder = appcode.dataserver.ServerSohoFormBuilder().Get(sohoformbuild_id)
        #data = serializers.deserialize('json', formbuilder.form_design_dict)
        formdesigndict = formbuilder.form_design_dict
        data = simplejson.loads(formdesigndict)
        return self.json_respond(data)

    def jsonsaveform(self,this_entity):
        sohoformbuild_id = self.request.POST['form_id']
        formdesigndict = self.request.POST['form_design']
        jsontext = simplejson.loads(simplejson.dumps(formdesigndict))
        formbuilder = appcode.dataserver.ServerSohoFormBuilder().Get(sohoformbuild_id)
        formbuilder.form_design_dict = jsontext
        formbuilder.put()
        jsonDict = {'response': True}
        #jsontext = simplejson.dumps()

        #Process Design Changes
        formdesign = designer.helpers.HelperFormDesign().GetBySohoForm(this_entity,formbuilder)
        designer.helpers.ProcessDesignChanges(formdesign)

        #Save form as being edited in the user profile
        about.helpers.HelperSignupExtendedProfile().SetParam('has_used_designer','Yes')

        sohoapp_id = str(this_entity.key().id())
        activity_text = "%s design updated" % formbuilder.name
        dashboard.helpers.log_user_action(self.request,"designer","jsonsaveform", sohoapp_id, activity_text, sohoformbuild_id)

        return self.json_respond(jsonDict)

    def jsonloadformData(self, this_entity):
        #Init
        submission_id = self.request.POST['submission_id']
        submission_key = self.request.POST['submission_key']
        jsontext = ""

        #Auth
        fs = designer.helpers.HelperFormSubmission().AuthSubmissionKeyAndID(submission_key,submission_id)

        #Return if not authenticated
        if fs is None:
            jsonDict = {'response': True, form_submission_data: False}
            return self.json_respond(jsonDict)

        #If we get here we can return the form data
        pkid = fs.pkid
        dictResults = designer.helpers.HelperFlexFieldValue().getCurrentValuesBySubmissionIDAsDict(fs,pkid)
        jsonDict = {'response': True, 'results': dictResults}
        return self.json_respond(jsonDict)


