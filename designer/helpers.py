from appcode.dataserver import *
import re
import entity.helpers
import appointment.helpers
from crm.helpers import ServerCRM
import dashboard.helpers
import sohoformbuilder.helpers
import appcode.taskqueuehelper
import designer.helpers

from appcode.baseclass import *

class HelperFormDesign():
    formTypes = {
        'TypeReservationCalendar':1,
        'TypeCRM':2,
    }

    def GetByEntityAndFormType(self, entity, formType):
        oFormDesign = None
        formDesigns = designer.models.FormDesign.gql("WHERE entity_reference = :1  AND formType = :2", entity, formType)
        formDesigns_count = formDesigns.count()
        if formDesigns_count > 0:
            oFormDesign = formDesigns[0]
        return oFormDesign

    def GetBySohoForm(self, entity, sohoform):
        oFormDesign = None
        formDesigns = designer.models.FormDesign.gql("WHERE entity_reference = :1  AND sohoformbuilder_reference = :2", entity, sohoform)
        formDesigns_count = formDesigns.count()
        if formDesigns_count > 0:
            oFormDesign = formDesigns[0]
        return oFormDesign

    def CopyFormDesign(self, srcForm,  destEntity):
        #1. Init
        newFormForTemplate = None
        formType = srcForm.formType

        #2. Does the Dest entity already have a form?
        newForm = self.GetByEntityAndFormType(destEntity, formType)

        #2. If None create a new form.
        if newForm is None:
            newForm = designer.models.FormDesign()

        #3. Loop through source form entities and save them in the new form
        newForm.formType = srcForm.formType
        newForm.creator = srcForm.creator
        newForm.xhtmlCode = srcForm.xhtmlCode
        newForm.formatCode = srcForm.formatCode
        newForm.behaviorCode = srcForm.behaviorCode
        newForm.fieldsJSON = srcForm.fieldsJSON
        newForm.entity_reference = destEntity
        #newFormDesign.derived_from = source_form
        newForm.is_default = srcForm.is_default

        #3.5 Create Forms on Soho BUilder
        srcFormID = srcForm.sohoformbuilder_reference
        newFormKey = sohoformbuilder.helpers.HelperSohoFormBuilder().CopySohoFormBuilder(srcFormID)
        strDesc = "User: %s EntityID: %s FormType: %s" % (users.GetCurrentUser(), str(destEntity.key().id()), str(formType))
        newSohoBuilderForm = appcode.dataserver.ServerSohoFormBuilder().Get(newFormKey.id())
        newSohoBuilderForm.description = strDesc
        newSohoBuilderForm.put()

        #4. Save Form
        newForm.sohoformbuilder_reference = newSohoBuilderForm
        newForm = newForm.put()
        return newForm


class HelperFormDesignField():
    fieldTypes = {
        'BooleanProperty':1,
        'IntegerProperty':2,
        'IntegerProperty':3,
        'FloatProperty':4,
        'DateProperty':5,
        'TimeProperty':6,
        'DateTimeProperty':7,
        'StringProperty':8,
        'TextProperty':9,
    }

    def GetByControlID(self, formDesign, control_id):
        formDesignField = None
        formDesignFields = designer.models.FormDesignField.gql("WHERE formdesign_reference = :1 and control_id = :2", formDesign, control_id)
        if formDesignFields.count() > 0:
            formDesignField = formDesignFields[0]
        return formDesignField

    def GetByFieldName(self, formDesign, field_name):
        formDesignField = None
        formDesignFields = designer.models.FormDesignField.gql("WHERE formdesign_reference = :1 and field_name = :2", formDesign, field_name)
        if formDesignFields.count() > 0:
            formDesignField = formDesignFields[0]
        return formDesignField

    def GetByIdOrName(self, formdesign, id_or_name):
        formdesignfield_id = id_or_name
        if formdesignfield_id.isdigit():
            fdf = ServerFormDesignField().Get(formdesignfield_id)
            if fdf:
                srcfield_name = fdf.field_name
        else:
            srcfield_name = formdesignfield_id  #in this instance it won't be an id but the name already usually happens with setup data

        #3. Look for this control ID in the new fields
        new_field = designer.helpers.HelperFormDesignField().GetByFieldName(formdesign,srcfield_name)
        return new_field

    def GetFormDesignFields(self, formDesign):
        return self.GetFormDesignFieldsByType(formDesign)

    def GetFormDesignFieldsByType(self, formDesign, controlType=None):
        formDesignFields = None
        try:
            if controlType:
                formDesignFields = designer.models.FormDesignField.gql('WHERE formdesign_reference = :1 and control_type = :2 and is_active = True', formDesign, controlType)
            else:
                formDesignFields = designer.models.FormDesignField.gql('WHERE formdesign_reference = :1 and is_active = True', formDesign)
        except ValueError:
            formDesignFields = None
        return formDesignFields

    def GetFormDesignFieldsByEntityAndFormType(self, entity, formType):
        formdesign =  designer.helpers.HelperFormDesign().GetByEntityAndFormType(entity, formType)
        return self.GetFormDesignFields(formdesign)


class HelperFormSubmission():

    def Create(self, entity_id, formType, pkid):
        pkid = str(pkid)
        if pkid.isdigit():
            pkid=int(pkid)
        else:
            pkid=0
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        signup = DataServer().getMySignup()
        fs = designer.models.FormSubmission(entity_ref=this_entity,formType=formType,signup_reference=signup,pkid=pkid)
        fs.put()
        return fs

    #def GetByKey(self, form_submission_key):
    #    fs = FormSubmission.get_by_key_name(form_submission_key)
    #    return fs

    def GetByID(self, form_submission_id):
        fs = None
        try:
            fs = FormSubmission.get(db.Key.from_path(FormSubmission.kind(), int(form_submission_id)))
        except:
            fs = None
        return fs

    def AuthSubmissionKeyAndID(self,submission_key, submission_id):
        fs = None

        #Get Current PKID from form submission and form type so we can get the
        fs = ServerFormSubmission().GetByID(submission_id)

        #Test to see whether you can get data
        if fs is None:
            fs = None
        else:
            if str(fs.key()) != submission_key:
                fs = None

        return fs


class HelperFlexFieldValue():
    ffv_field_mappings = {
        'text':'value_string',
        'textarea':'value_text',
        'date':'value_date',
        'radio':'value_string'
    }
    ffv_sub_field_mappings = {
        'df':'value_date',
        'tf':'value_time',
        'dt':'value_date',
        'tt':'value_time'
    }
        
    def assignValueToCorrectField(self,flex_field_value):
        #Takes an already populated ffv and assigns the value_string to the correct value_<type>
        ffv_field_name = None
        try:
            ffv_field_name = self.ffv_field_mappings[flex_field_value.display_type]
        except:
            return flex_field_value

        #However if a sub type exists then do that
        if flex_field_value.sub_field_type:
            try:
                ffv_field_name = self.ffv_sub_field_mappings[flex_field_value.sub_field_type]
            except:
                return flex_field_value

        property_to_update = flex_field_value.properties()[ffv_field_name]
        value_string = flex_field_value.value_string
        #value_string = unicode_value_string.encode('utf-8')

        if property_to_update.name == "value_string":
            property_to_update.__set__(flex_field_value,value_string)

        if property_to_update.name == "value_date":
            dte = DataServer().getDateFromString(value_string,"%m/%d/%Y")
            if dte:
                property_to_update.__set__(flex_field_value,dte.date())

        if property_to_update.name == "value_time":
            dte = DataServer().getTimeFromString(value_string,"%I:%M %p")
            if dte:
                property_to_update.__set__(flex_field_value,dte)


        flex_field_value.put()
        return flex_field_value

    def GetByID(self, flex_field_value_id):
        ffv = None
        try:
            ffv = FlexFieldValue.get(db.Key.from_path(FlexFieldValue.kind(), int(flex_field_value_id)))
        except:
            ffv = None
        return ffv

    def GetValuesBySubmission(self,form_submission):
        ffvs = None
        try:
            ffvs = designer.models.FlexFieldValue.gql('WHERE form_submission_ref = :1', form_submission)
        except ValueError:
            ffvs = None
        return ffvs

    def getValuesBySubmissionAsDict(self,form_submission, pkid):
        #1. Get flex field values
        ffvs = self.GetValuesBySubmission(form_submission)

        #2. Convert to dictionary
        newRow = {}
        newRow['pkid'] = str(pkid)
        for ffv in ffvs:
            control_id = ffv.form_design_field_ref.control_id
            control_type = ffv.form_design_field_ref.control_type
            display_type = ffv.form_design_field_ref.display_type
            sft = ffv.sub_field_type or ""

            dict_value_date = None
            dict_value_time = None
            if ffv.value_date:
                dict_value_date = '{"value_date":new Date("%s")}' % ffv.value_date
            if ffv.value_time:
                dict_value_time = '{"value_time":new Date("%s")}' % ffv.value_time

            newVals = {'control_id':control_id,
                        'control_type':control_type,
                        'sub_field_type':str(sft),
                        'display_type':display_type,
                        'value_string':ffv.value_string,
                        'value_int':ffv.value_int,
                        'value_text':ffv.value_text,
                        'value_date':dict_value_date,
                        'value_time':dict_value_time,
                        }
            newRow[str(ffv.key().id())] = newVals
            #str(ffv.value_string)
        return newRow

def ProcessDesignChanges(formdesign):

    #1. Get Form Data
    sfb = formdesign.sohoformbuilder_reference
    if sfb is None:
        return
    sfb_id = int(sfb.key().id())
    
    #2. Get Current Fields Stored From Form Design
    storedFields = designer.helpers.HelperFormDesignField().GetFormDesignFields(formdesign)

    #3. Get Fields from form design dictionary.
    formFieldDesignDict = sohoformbuilder.helpers.HelperSohoFormBuilder().GetFormControls(sfb_id)
    formFields = formFieldDesignDict['formdesign']

    #2. Loop Through Frevvo Fields and insert if they don't exist in storedFields
    for ffKey in formFields.keys():
        ff = formFields[ffKey]
        ff_field_found = None
        sf_field_found = None
        for sf in storedFields:
            if sf.control_id == ff['id']:
                ff_field_found = ff
                sf_field_found = sf

        if ff_field_found:
            #Check entries still match
            bolUpdateReq = False
            if sf_field_found.field_name != ff_field_found['label']:
                bolUpdateReq = True
            if sf_field_found.control_type != ff_field_found['controlType']:
                bolUpdateReq = True
            if bolUpdateReq:
                sf_field_found.field_name = ff_field_found['label']
                sf_field_found.field_display_name = ff_field_found['label']
                sf_field_found.control_type = ff_field_found['controlType']
                sf_field_found.display_type = ff_field_found['displayType']
                sf_field_found.put()
        else:
            #Frevvo Field not in database
            fdf = designer.models.FormDesignField(
                    field_name=ff['label'],
                    field_display_name=ff['label'],
                    control_id=ff['id'],
                    control_type=ff['controlType'],
                    display_type=ff['displayType'],
                    formdesign_reference=formdesign,
                    is_active=True
                    )
            fdf.put()

    #3. Loop through stored fields and any not appearing are no longer with us
    for sf in storedFields:
        ff_field_found = None
        sf_field_found = None
        for ffKey in formFields:
            ff = formFields[ffKey]
            if sf.control_id == ff['id']:
                ff_field_found = ff
                sf_field_found = sf

        if ff_field_found is None:
            #Field no longer active deactivate.
            sf.is_active = False
            sf.put()


def ApplyMandatoryRequiredFields(entity_id, form_type_id):

    #1. Get Entity
    this_entity = entity.helpers.ServerEntity().Get(entity_id)

    #2. Get Form Design
    this_form_design = ServerFormDesign().GetByEntityAndFormType(this_entity, form_type_id)
    sfb = this_form_design.sohoformbuilder_reference
    sfb_id = int(sfb.key().id())

    #3. Get Form Fields
    dict_form_design_full = sohoformbuilder.helpers.ServerSohoFormBuilder().GetFormControls(sfb_id)
    dict_form_design = dict_form_design_full['formdesign']
    new_dict_form_design = dict_form_design

    #3. Get Entity Params and make fields as required
    if form_type_id == 1:
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'AppointmentDateDefaultField',new_dict_form_design)
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'AppointmentCRMDefaultField',new_dict_form_design)

    if form_type_id == 2:
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'CustomerNameDefaultField',new_dict_form_design)
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'CustomerEmailDefaultField',new_dict_form_design)

    dict_form_design_full['formdesign'] = new_dict_form_design
    string_new_dict = simplejson.dumps(dict_form_design_full)

    sfb.form_design_dict = string_new_dict
    sfb.put()

    return sfb

def ApplyMandatoryRequiredField(this_entity, this_form_design, param_name,current_form_design_dict):
    #THis function gets the mandatory field name and applies the required = 1 to the dictionary
    field_param = entity.helpers.ServerEntityParams().GetParam(this_entity, param_name)
    if field_param is None:
        return
    param_field = designer.helpers.ServerFormDesignField().GetByIdOrName(formdesign=this_form_design,id_or_name=field_param.param_value)
    if param_field is None:
        return
    new_dict_form_design = None
    if param_field:
        new_dict_form_design = sohoformbuilder.helpers.ServerSohoFormBuilder().ApplyRequiredFieldToFormDesignDict(current_form_design_dict,param_field.field_name)
    return new_dict_form_design


    

def convertDictionaryToFrevvoDataParameter(dict):
    strRet = "{"

    for eitem in dict:
        strRet = "%s %s:'%s'," % (strRet, eitem,dict[eitem])

    if len(strRet) > 1:
        strRet = strRet[0:len(strRet)-1]

    strRet = "%s}" % strRet

    return strRet

def getCurrentFormDataFromNewSubmission(submission_id):
    #Get Current PKID from form submission and form type so we can get the
    fs = ServerFormSubmission().Get(submission_id)
    bolCanGetData = True

    #Test to see whether you can get data
    if fs is None:
        bolCanGetData = False

    if bolCanGetData == False:
        dictText = {'response': True, 'form_submission_data': False}
        return dictText

    #If we get here we can return the form data
    pkid = fs.pkid
    formType = fs.formType
    record = None

    #if pkid is 0 then this is a new submission
    if pkid == 0:
        dictText = {'response': True, 'form_submission_data': False}
        return dictText

    #Get previous form submission so we can get the previous submission values
    if formType == 1:
        record = appcode.dataserver.ServerAppointment().Get(pkid)
    if formType == 2:
        record = ServerCRM().Get(pkid)

    prev_fs = record.form_submission_ref

    #Get previous field values
    dictResults = designer.helpers.HelperFlexFieldValue().getValuesBySubmissionAsDict(prev_fs,pkid)
    return dictResults


class ServerProcessPost():
    def __init__(self,form_submission=None, listVals=None):
        if form_submission:
            self.form_submission = form_submission
            self.entity_ref=form_submission.entity_ref
            self.formType=form_submission.formType
            self.listVals=listVals
            self.form_design_fields = designer.helpers.HelperFormDesignField().GetFormDesignFieldsByEntityAndFormType(self.entity_ref,self.formType)
            self.dict_form_design_fields = {}

            #These are used to store pkid and mnemonic values when items are updated 
            self.pkid = 0
            self.value_string = ""

            #1. Create dictionary of fieldnames and types
            for ff in self.form_design_fields:
                self.dict_form_design_fields[ff.field_name] = ff.display_type

    def ProcessValues(self):
        #1. Create Flex Field Values
        for dictRow in self.listVals:
            field_name = dictRow['name']
            field_value = dictRow['value']
            self.SubmitValue(field_name=field_name, field_value=field_value)

        #2. Get Default Fields and populate CRM or Appointment records.
        self.ProcessSubmissionToParent(self.form_submission)

    #Process values from FlexFieldValue back to the parent
    #ToDO this needs tidying up
    def ProcessSubmissionToParent(self, form_submission):
        #1. Get Data For This Submission
        ffvs = designer.helpers.HelperFlexFieldValue().GetValuesBySubmission(form_submission)

        activity_text = None

        #2. Main Processing
        if form_submission.formType == 1: #Appointment
            activity_text = self.ProcessSubmissionToAppointment(form_submission,ffvs)

        if form_submission.formType == 2: #CRM
            activity_text = self.ProcessSubmissionToCRM(form_submission,ffvs)

        entity_id = form_submission.entity_ref.key().id()
        dashboard.helpers.log_user_action(None,"postdata","ProcessSubmissionToParent", entity_id, activity_text, form_submission)

    def ProcessSubmissionToAppointment(self, form_submission,ffvs):
        #0. Init
        activity_text = None
        app_form_design = designer.helpers.HelperFormDesign().GetByEntityAndFormType(entity=form_submission.entity_ref,formType=1)
        strFormType = ""

        #1. Get AppointmentDateDefaultField Field
        appoint_field_id = entity.helpers.HelperEntityParams().GetParam(form_submission.entity_ref,'AppointmentDateDefaultField').param_value
        appoint_field = designer.helpers.HelperFormDesignField().GetByIdOrName(formdesign=app_form_design,id_or_name=appoint_field_id)

        #1. Get CRM Default name field
        appoint_crm_field_id = entity.helpers.HelperEntityParams().GetParam(form_submission.entity_ref,'AppointmentCRMDefaultField').param_value
        appoint_crm_field = designer.helpers.HelperFormDesignField().GetByIdOrName(formdesign=app_form_design,id_or_name=appoint_crm_field_id)

        #2. Get Date
        dteBooking = None
        custName = None
        for ffv in ffvs:
            if ffv.field_name == appoint_field.field_name:
                if dteBooking is None:
                    dteBooking = self.GetPrimaryDateValueFromFlexFields(appoint_field.field_name, ffvs)
            if ffv.field_name == appoint_crm_field.field_name:
                custID = ffv.value_int
                cust = ServerCRM().Get(custID)
                if cust:
                    custName = cust.name

        if form_submission.pkid > 0:
            activity_text = "Appointment updated [%s]" % custName
            appoint = appcode.dataserver.ServerAppointment().Get(form_submission.pkid)
            appoint.booking_date=dteBooking
            appoint.name=custName
            appoint.entity_reference=form_submission.entity_ref
            appoint.form_submission_ref = form_submission
            appoint.put()
        else:
            activity_text = "Appointment created [%s]" % custName
            appoint = appointment.models.Appointment(name=custName,booking_date=dteBooking,entity_reference=form_submission.entity_ref,form_submission_ref = form_submission)
            appoint.put()
            form_submission.pkid = appoint.key().id()
            form_submission.put()

        #Get Additional Information and save
        appoint.date_from = self.GetDateValueFromFlexFields(appoint_field.field_name, ffvs,"df")
        appoint.time_from = self.GetDateValueFromFlexFields(appoint_field.field_name, ffvs,"tf")
        appoint.time_to = self.GetDateValueFromFlexFields(appoint_field.field_name, ffvs,"tt")
        appoint.date_to = self.GetDateValueFromFlexFields(appoint_field.field_name, ffvs,"dt")
        appoint.put()


        self.pkid = appoint.key().id()
        self.mnemonic = appoint.name
        return activity_text

    def ProcessSubmissionToCRM(self, form_submission,ffvs):
        #0. Init
        activity_text = None
        crm_field_id = entity.helpers.HelperEntityParams().GetParam(form_submission.entity_ref,'CustomerNameDefaultField').param_value
        crm_form_design = designer.helpers.HelperFormDesign().GetByEntityAndFormType(entity=form_submission.entity_ref,formType=2)
        crm_field = designer.helpers.HelperFormDesignField().GetByIdOrName(formdesign=crm_form_design,id_or_name=crm_field_id)

        #2. Get Customer Name
        strCustomerName = None
        for ffv in ffvs:
            if ffv.field_name == crm_field.field_name:
                strCustomerName = ffv.value_string

        if form_submission.pkid > 0:
            activity_text = "Contact updated [%s]" % strCustomerName
            this_crm = ServerCRM().Get(form_submission.pkid)
            this_crm.name=strCustomerName
            this_crm.entity_reference=form_submission.entity_ref
            this_crm.form_submission_ref = form_submission
            this_crm.put()
        else:
            activity_text = "Contact created [%s]" % strCustomerName
            this_crm = crm.models.CRM(name=strCustomerName,entity_reference=form_submission.entity_ref,form_submission_ref = form_submission)
            this_crm.put()
            form_submission.pkid = this_crm.key().id()
            form_submission.put()

        self.pkid = this_crm.key().id()
        self.mnemonic = this_crm.name
        return activity_text

    #Process values from parent to FlexFieldValue
    def ProcessSubmissionToChild(self, form_submission):
     #1. Get Data For This Submission
        ffvs = designer.helpers.HelperFlexFieldValue().GetValuesBySubmission(form_submission)

        #2. Main Processing
        if form_submission.formType == 1: #Appointment
            #1. Get Default Field
            appoint_field_id = entity.helpers.HelperEntityParams().GetParam(form_submission.entity_ref,'AppointmentDateDefaultField').param_value
            app_form_design = designer.helpers.HelperFormDesign().GetByEntityAndFormType(entity=form_submission.entity_ref,formType=1)
            appoint_field = designer.helpers.HelperFormDesignField().GetByIdOrName(formdesign=app_form_design,id_or_name=appoint_field_id)

            #2. Get Date
            appoint = appcode.dataserver.ServerAppointment().Get(form_submission.pkid)
            dteBooking = appoint.booking_date

            #3. Update ffv
            for ffv in ffvs:
                if ffv.field_name == appoint_field.field_name:
                    if ffv.sub_field_type:
                        if ffv.sub_field_type == "df" or ffv.sub_field_type == "dt":
                            ffv.value_date = dteBooking
                            value_string = str(dteBooking.strftime("%m/%d/%Y"))
                            ffv.value_string = str(value_string)
                    else:
                        ffv.value_date = dteBooking
                        value_string = str(dteBooking.strftime("%m/%d/%Y"))
                        ffv.value_string = str(value_string)
                    ffv.put()

        if form_submission.formType == 2: #CRM
            asd=1/0

    def GetPrimaryDateValueFromFlexFields(self, date_field_name, ffvs):
        dteBooking = None
        for ffv in ffvs:
            if ffv.field_name == date_field_name:
                if ffv.sub_field_type is None:
                    dteBooking = ffv.value_date
                else:
                    if ffv.sub_field_type == 'df':
                        dteBooking = ffv.value_date
        return dteBooking
    
    def GetDateValueFromFlexFields(self, date_field_name, ffvs, sub_field_type):
        dte_or_time = None
        for ffv in ffvs:
            if ffv.field_name == date_field_name:
                if ffv.sub_field_type:
                    if ffv.sub_field_type == sub_field_type:
                        if sub_field_type == "df" or sub_field_type == "dt":
                            dte_or_time = ffv.value_date
                        if sub_field_type == "tf" or sub_field_type == "tt":
                            dte_or_time = ffv.value_time
        return dte_or_time

    def GetFieldInfo(self, field_name):
        fret = None
        #Look for || in the field name if processed the field name takes this information
        #field_name||sub_field_id

        logging.info('field_name:%s' % field_name)
        field_attributes = self.getSubmitValueAttributes(field_name)
        real_field_name = field_attributes['field_name']

        for finfo in self.form_design_fields:
            if finfo.field_name == real_field_name:
                fret = finfo
        return fret

    def getSubmitValueAttributes(self,field_name):
        field_attributes = field_name.split('||')
        default_dict = {'field_name':field_name, 'sub_field_Type': ''}
        for i in range(len(field_attributes)):
            if i == 0:
                default_dict['field_name'] = field_attributes[i]
            if i == 1:
                default_dict['sub_field_Type'] = field_attributes[i]
        return default_dict
        

    def SubmitValue(self, field_name, field_value):
        #1. Get Field Information
        finfo = self.GetFieldInfo(field_name)

        field_attributes = self.getSubmitValueAttributes(field_name)
        sub_field_type = field_attributes['sub_field_Type']

        #This field no longer exists
        if finfo is None:
            return
        
        #2. Create new flex field value
        ffv = None
        value_string = None
        value_text = None
        if finfo.display_type == 'textarea':
            value_text = field_value
        else:
            value_string = field_value

        ffv = designer.models.FlexFieldValue(
                                form_submission_ref=self.form_submission,
                                entity_ref=self.form_submission.entity_ref,
                                form_design_field_ref = finfo,
                                formType=self.form_submission.formType,
                                field_name = finfo.field_name,
                                display_name = finfo.field_display_name,
                                display_type = finfo.display_type,
                                value_string = value_string,
                                value_text = value_text,
                                sub_field_type = sub_field_type
                            )


        #2.1. Check for any additional fields to be updated.
        if finfo.control_type == 'customer':
            custID = field_value
            cust = ServerCRM().Get(custID)
            ffv.value_string = cust.name
            ffv.value_int = int(custID)
        
        #2.9 Update
        ffv.put()

        #3. Add Correct Value Inforamtion to the correct field
        designer.helpers.HelperFlexFieldValue().assignValueToCorrectField(ffv)

    def GetFieldType(field_name):
        return None


def ApplyMandatoryRequiredFields(entity_id, form_type_id):

    #1. Get Entity
    this_entity = appcode.dataserver.ServerEntity().Get(entity_id)

    #2. Get Form Design
    this_form_design = entity.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, form_type_id)
    sfb = this_form_design.sohoformbuilder_reference
    sfb_id = int(sfb.key().id())

    #3. Get Form Fields
    dict_form_design_full = sohoformbuilder.helpers.HelperSohoFormBuilder().GetFormControls(sfb_id)
    dict_form_design = dict_form_design_full['formdesign']
    new_dict_form_design = dict_form_design

    #3. Get Entity Params and make fields as required
    if form_type_id == 1:
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'AppointmentDateDefaultField',new_dict_form_design)
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'AppointmentCRMDefaultField',new_dict_form_design)

    if form_type_id == 2:
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'CustomerNameDefaultField',new_dict_form_design)
        new_dict_form_design = ApplyMandatoryRequiredField(this_entity,this_form_design,'CustomerEmailDefaultField',new_dict_form_design)

    dict_form_design_full['formdesign'] = new_dict_form_design
    string_new_dict = simplejson.dumps(dict_form_design_full)

    sfb.form_design_dict = string_new_dict
    sfb.put()

    return sfb

def ApplyMandatoryRequiredField(this_entity, this_form_design, param_name,current_form_design_dict):
    #THis function gets the mandatory field name and applies the required = 1 to the dictionary
    field_param = entity.helpers.HelperEntityParams().GetParam(this_entity, param_name)
    if field_param is None:
        return
    param_field = designer.helpers.HelperFormDesignField().GetByIdOrName(formdesign=this_form_design,id_or_name=field_param.param_value)
    if param_field is None:
        return
    new_dict_form_design = None
    if param_field:
        new_dict_form_design = sohoformbuilder.helpers.HelperSohoFormBuilder().ApplyRequiredFieldToFormDesignDict(current_form_design_dict,param_field.field_name)
    return new_dict_form_design
