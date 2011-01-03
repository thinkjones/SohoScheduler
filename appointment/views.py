    # Main View Import
from appcode.viewsbaseclass import *
from appcode.datehelper import *
#from sohoformbuilder.views import sohoruntime as sohoformbuilder_views_sohoruntime

import designer.helpers
import dashboard.helpers
import appointment.helpers

# Setup Form
def jsonrequests():
    asd=1

tabs_settings = {
    'main':{'index':0, 'title':'Appointments'},
    }
tab_selected = 'main'

def index():
    asd = 1
def new():
    asd=1
def delete():
    asd=1
def view():
    asd=1
def edit():
    asd=1

#######################################################
### Main Web Page Access Points
#######################################################
class AppointmentPage(SohoResponse):
    @sohosecurity.authenticate('View')
    def get(self, sohoapp_id):
        dashboard.helpers.log_navigation(self.request, "appointment", sohoapp_id)
        return self.ByLastModified(sohoapp_id)

    def ByLastModified(self, entity_id):
	this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
	these_events = appointment.helpers.HelperAppointment().GetAppointmentsLikeGmail(this_entity, 0)
	return self.returnAppointment(this_entity, these_events, entity_id, "All (Order by Last modified)", "showall")

    def returnAppointmentNoTitle(self, this_entity, appointments, entity_id):
            return returnAppointment(this_entity, appointments, entity_id, "appointmentr")

    def returnAppointment(self, this_entity, appointments, entity_id, subtitle, sortfield):
        template = 'appointment/index'
        if self.IsAjaxRequest():
                template = 'appointment/_FullCalendar'

        tab_info = tabs_settings[tab_selected]

        self.template = template
        self.entity = this_entity
        self.appointments = appointments
        self.appointments_count = appointments.count
        self.tabSelected = "tabAppointment"
        self.tab_info = tab_info
        self.signed_up = True
        self.entity_id = entity_id
        self.title = "Appointments"
        self.subtitle = subtitle
        self.sortfield = sortfield
        return self.respond()





    @sohosecurity.authenticate('Edit')
    def new(self, sohoapp_id):
        return self.runtimeform(sohoapp_id, 0)

    def runtimeform(self, sohoapp_id, appointment_id):
        #sohoformbuilder.views.runtime

        #Init
        this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
        this_appointment = None

        #Test to see if appointment exists
        if int(appointment_id) > 0:
            this_appointment = appointment.helpers.HelperAppointment().GetAppointment(appointment_id)
            if this_appointment  is None:
                return http.HttpResponseNotFound('No appointment exists with that key (%r)' % appointment_id)

        formtype = designer.helpers.HelperFormDesign().formTypes['TypeReservationCalendar']
        default_form = designer.helpers.HelperFormDesign().GetByEntityAndFormType(this_entity, formtype)
        sohoformbuilderid = default_form.sohoformbuilder_reference.key().id()

        submission = designer.helpers.HelperFormSubmission().Create(sohoapp_id,1,appointment_id)
        submission_key = str(submission.key())
        submission_id = submission.key().id()

        import sohoformbuilder.views
        form_renderer = sohoformbuilder.views.SohoFormBuilderPage()
        form_renderer.request = self.request
        form_renderer.response = self.response
        return form_renderer.sohoruntime(sohoapp_id,sohoformbuilderid,submission_id,submission_key)

    @sohosecurity.authenticate('Edit')
    def edit(self, sohoapp_id, appointment_id):
        return self.runtimeform(sohoapp_id,  appointment_id)
    
    def view(self, sohoapp_id, appointment_id):
            this_entity = appcode.dataserver.ServerEntity().Get(sohoapp_id)
            this_appointment = appointment.helpers.HelperAppointment().GetAppointment(appointment_id)

            if request.method == 'GET':
                    message = ''

            self.template = 'appointment/view'
            if self.IsAjaxRequest():
                    self.template = 'appointment/_view'

            tab_info = tabs_settings[tab_selected]

            self.entity_id = entity_id
            self.appointment_id = appointment_id
            self.entity = this_entity
            self.tab_info = tab_info
            self.appointment = this_appointment
            self.tabSelected = "tabAppointment"
            self.signed_up = True
            return self.respond()

    def delete(request, entity_id, appointment_id):
            this_appointment = appointment.get(db.Key.from_path(appointment.kind(), int(appointment_id)))
            this_appointment.active = False
            this_appointment.put()
            return index(request,  entity_id)


#######################################################
##  Return method
#######################################################


class AppointmentJsonPage(SohoResponse):
    def post(self,entity_id):
        this_entity = appcode.dataserver.ServerEntity().Get(entity_id)
        strAction = self.request.POST['action']

        if strAction == "getCalendarData":
            return self.getCalendarData(this_entity, False)
        if strAction == "getCalendarDataFullCalendar":
            return self.getCalendarData(this_entity, True)
        if strAction == "viewinfo":
            return self.viewinfo(entity_id)
        if strAction == "updateEventDate":
            return self.updateEventDate(entity_id)
        if strAction == "updateEventDateDelta":
            return self.updateEventDateDelta(entity_id)
        if strAction == "deleteappointment":
            return self.jsonDeleteAppointment(this_entity,strAction)

    def updateEventDate(self, entity_id):
        EntityHasAccess = entity.helpers.HelperEntity().CheckAccess(entity_id)
        responseVal = "No Accesss"
        strD = None
        strM = None
        strY = None
        app = None
        dictResponse = None
        if EntityHasAccess == False:
            dictResponse = {'response': False}
            self.json_respond(dictResponse)

        try:
            strD = self.request.POST['Da']
            strM = self.request.POST['Mo']
            strY = self.request.POST['Ye']
        except:
            jsontext = simplejson.dumps({'response': False})
            return HttpResponse(jsontext, "application/json")
        dteHelp = datehelper()
        dictDateInfo = dteHelp.SetupDateInfoByDate(int(strY), int(strM), int(strD))
        dteUpdateTo = dictDateInfo['actualDate']
        appointment_id = self.request.POST['appointment_id']
        app = appcode.dataserver.ServerAppointment().Get(appointment_id)

        if app:
            app.booking_date = dteUpdateTo
            app.put()
            designer.helpers.ServerProcessPost().ProcessSubmissionToChild(app.form_submission_ref)
            dictResponse = {'response': True,'appointment_id':appointment_id}
            self.json_respond(dictResponse)

        dictResponse = {'response': False}
        self.json_respond(dictResponse)

    @sohosecurity.authenticate('Edit')
    def updateEventDateDelta(self, entity_id):
        responseVal = "No Accesss"
        deltaDay = None
        deltaMin = None
        app = None

        try:
            deltaDay = self.request.POST['Da']
            deltaMin = self.request.POST['Mi']
        except:
            dictResponse = {'response': False}
            return self.json_respond(dictResponse)
            
        #Get Appointment
        appointment_id = self.request.POST['appointment_id']
        app = appcode.dataserver.ServerAppointment().Get(appointment_id)
        dteCurrentDate = app.booking_date
        dteUpdateTo = dteCurrentDate + datetime.timedelta(days=int(deltaDay))

        if app:
            app.booking_date = dteUpdateTo
            app.put()
            designer.helpers.ServerProcessPost().ProcessSubmissionToChild(app.form_submission_ref)
            dictResponse = {'response': True,'appointment_id':appointment_id}
            return self.json_respond(dictResponse)

        dictResponse = {'response': False}
        return self.json_respond(dictResponse)


    @sohosecurity.authenticate('View')
    def getCalendarData(self, this_entity,for_full_calendar=False):
        entity_id = this_entity.key().id()
        responseVal = "No Accesss"
        appointments_count = 0
        listEvents = None
        strD = None
        strM = None
        strY = None
        responseVal = "Access"
        try:
            strD = self.request.POST['Da']
            strM = self.request.POST['Mo']
            strY = self.request.POST['Ye']
        except:
            dteToday = datetime.date.today()
            strD = "01"
            strM = dteToday.month
            strY = dteToday.year
        dteHelp = datehelper()
        dteHelp.SetupDateInfoByMonthForFullCalendar(int(strD), int(strM), int(strY))
        these_events = appointment.helpers.HelperAppointment().GetAppointmentsByMonth(this_entity, dteHelp,True)
        listEvents = []
        appointments_count = these_events.count()
        for app in these_events:
            dte = app.booking_date
            strEventName = "%s : %s" % (app.key().id(), app.name)
            newEvent = None
            if for_full_calendar:
                strM = datehelper().PadDateWithZeros(dte.month)
                strD = datehelper().PadDateWithZeros(dte.day)

                strStartDate = "%s-%s-%s" % (dte.year, strM, strD)
                strEndDate = strStartDate
                newEvent = {"id": app.key().id(), "start": strStartDate, "end": strEndDate, "title": strEventName, "url": "", "description": strEventName }
            else:
                intM = int(dte.month) - 1
                if intM == -1:
                    intM = 11
                strM = datehelper().PadDateWithZeros(intM)
                strStartDate = "new Date(%s, %s, %s)" % (dte.year, strM, dte.day)
                strEndDate = strStartDate
                newEvent = {"EventID": app.key().id(), "StartDateTime": strStartDate, "EndDateTime": strEndDate, "Title": strEventName, "URL": "", "Description": strEventName }

            listEvents.append(newEvent)

        dictResponse = {'response': True, 'access_level': responseVal,'appointments_count':appointments_count,'events':listEvents}
        self.json_respond(dictResponse)


    @sohosecurity.authenticate('Edit')
    def jsonDeleteAppointment(self, this_entity, strAction):

        entity_id = this_entity.key().id()
        responseVal = "Access"

        appointment_id = self.request.POST['appointment_id']
        appointment_entity = appcode.dataserver.ServerAppointment().Get(appointment_id)
        appointment_entity.active = False
        appointment_entity.put()
        activity_text = "Appointment deleted [%s]" % str(appointment_entity.name)
        dashboard.helpers.log_user_action(self.request,"appointment","jsonDeleteAppointment", entity_id, activity_text, appointment_id)


        dictResponse = {'response': True, 'access_level': responseVal}
        self.json_respond(dictResponse)

    @sohosecurity.authenticate('View')
    def viewinfo(self, entity_id):
        appointment_id = self.request.POST['appointment_id']
        template = 'appointment/_info'
        self.template = template
        this_appointment = appcode.dataserver.ServerAppointment().Get(appointment_id)
        self.appointment = this_appointment
        fs = this_appointment.form_submission_ref
        #Get Values
        ffvs = designer.helpers.HelperFlexFieldValue().GetValuesBySubmission(fs)
        self.ffvs = ffvs
        self.entity_id = entity_id
        return self.respond()