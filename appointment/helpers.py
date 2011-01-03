from appcode.dataserver import *


class HelperAppointment():
    def GetAppointmentCount(self, this_entity):
        schedule = None
        schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1", this_entity)
        return schedule.count()

    def GetAppointments(self, this_entity):
        schedule = None
        schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1 order by booking_time", this_entity)
        return schedule

    def GetAppointmentsLikeGmail(self, this_entity,  pageNumber):
        schedule = None
        schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1 order by modified DESC LIMIT 0,20", this_entity)
        return schedule

    def GetAppointmentsByDate(self, this_entity, filteryear, filtermonth, filterday):
        schedule = None
        schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1 and booking_date = :2  order by booking_time", this_entity, datetime.datetime(int(filteryear), int(filtermonth), int(filterday)))
        return schedule

    def GetAppointmentsBetweenDates(self, this_entity, fromDate, toDate):
        schedule = None
        #ToDo Fix time ordering adding a order by booking time in this select makes all resultsdisappear
        #schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1 and booking_date > :2 and booking_date < :3  order by booking_date, booking_time", entity, fromDate,  toDate)
        schedule = appointment.models.Appointment.gql("WHERE active = True and entity_reference = :1 and booking_date > :2 and booking_date < :3  order by booking_date", this_entity, fromDate,  toDate)
        return schedule

    def GetAppointmentsYesterday(self, this_entity, svrDateHelper):
        schedule = None
        #dteFrom = datetime.date.today() + datetime.timedelta(days=-2)
        #dteTo = datetime.date.today()  + datetime.timedelta(days=0)
        dteFrom = svrDateHelper.getDateInfo('yesterday','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('yesterday','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentsToday(self, this_entity, svrDateHelper):
        schedule = None
        dteFrom = svrDateHelper.getDateInfo('today','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('today','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentsTomorrow(self, this_entity, svrDateHelper ):
        schedule = Appointment.all()
        dteFrom = svrDateHelper.getDateInfo('tomorrow','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('tomorrow','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentNextSevenDays(self, this_entity, svrDateHelper):
        schedule = Appointment.all()
        dteFrom = svrDateHelper.getDateInfo('nextseven','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('nextseven','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentThisMonth(self, this_entity,svrDateHelper):
        dteFrom = svrDateHelper.getDateInfo('thismonth','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('thismonth','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentsByMonth(self, this_entity, svrDateHelper, GetWeekEitherSide=False):
        dteFrom = svrDateHelper.getDateInfo('bymonth','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('bymonth','gqlWhereTo')
        if GetWeekEitherSide:
            dteFrom = dteFrom + datetime.timedelta(days=-7)
            dteTo = dteTo + datetime.timedelta(days=7)
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointmentsByYear(self, this_entity, svrDateHelper):
        dteFrom = svrDateHelper.getDateInfo('byyear','gqlWhereFrom')
        dteTo = svrDateHelper.getDateInfo('byyear','gqlWhereTo')
        return self.GetAppointmentsBetweenDates(this_entity,  dteFrom,  dteTo)

    def GetAppointment(self, appointment_id):
        return ServerAppointment().Get(appointment_id)

    def GetRecentActivity(self, owner,  Limit):
        q = db.GqlQuery("SELECT * FROM Appointment WHERE owner = :1 order by activity_date DESC", owner)
        results = q.fetch(Limit)
        return results
