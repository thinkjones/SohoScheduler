import datetime

class datehelper:
    #Creates a series of dates that are useful for the applications.
    #output_formats = ["%A %B %d %I:%M:%S %p %Y"]
    output_formats = ["%A %B %d, %Y"]
    predefined_dates = {}

    def __init__(self, attrs=None, output_formats=None):
        #Init
        self.attrs = attrs or {}
        self.output_formats = output_formats or self.output_formats
        
        #Setup Dates
        dteToday = datetime.date.today()
        dteYesterday = dteToday + datetime.timedelta(days=-1)
        dteTomorrow = dteToday  + datetime.timedelta(days=1)

        self.predefined_dates['today'] = self.dictGetDateInfo(dteToday,1)
        self.predefined_dates['yesterday'] = self.dictGetDateInfo(dteYesterday,1)
        self.predefined_dates['tomorrow'] = self.dictGetDateInfo(dteTomorrow,1)
        self.predefined_dates['nextseven'] = self.dictGetDateInfo(dteToday,7)
        self.predefined_dates['thismonth'] = self.dictGetDateInfoThisMonth(dteToday)
    
    def getDateInfo(self, strDatePeriod, strValueType):
        oRetVal = self.predefined_dates[strDatePeriod][strValueType]
        return oRetVal

    def SetupDateInfoByYear(self, filterYear):
        dteFrom = datetime.date(int(filterYear), 01, 01)
        dteTo = datetime.date(int(filterYear), 12, 31)
        self.predefined_dates['byyear'] = self.dictGetDateInfoBetweenDates(dteFrom, dteTo, 365)
        oRetVal = self.predefined_dates['byyear']
        return oRetVal
            
    def SetupDateInfoByMonthForFullCalendar(self, filterDay, filterMonth, filterYear):
        
        #Add a month because months are zero based 
        filterMonth = filterMonth + 1 
        
        dteEnd = datetime.date(int(filterYear), filterMonth, filterDay)
        dteStart = dteEnd + datetime.timedelta(days=-40)
        self.predefined_dates['bymonth'] = self.dictGetDateInfoBetweenDates(dteStart, dteEnd, 35)
        oRetVal = self.predefined_dates['bymonth']
        return oRetVal

    def SetupDateInfoByMonth(self, filterYear, filterMonth):
        dteFrom = datetime.date(int(filterYear), filterMonth, 01)
        filterNextMonth = filterMonth + 1
        if filterNextMonth > 12:
            filterNextMonth = 1
            filterYear = filterYear + 1
        dteTo = datetime.date(int(filterYear), filterNextMonth, 01)  + datetime.timedelta(days=-1)
        self.predefined_dates['bymonth'] = self.dictGetDateInfoBetweenDates(dteFrom, dteTo, 30)
        oRetVal = self.predefined_dates['bymonth']
        return oRetVal

    def ConvertFullCalendarMonth(self,filterMonth):
        #The JQUery FullClaendar stores dates in a 0-11 format
        #This class converst on a 1-2 format
        #This code centralisese the conversion

        real_month = 1
        real_month = int(filterMonth) + 1
        if real_month > 12:
            real_month = 1
        return real_month

    def PadDateWithZeros(self,strVal):

        intVal = 0
        strRet = "01"
        if str(strVal).isdigit():
            intVal = int(strVal)
            if intVal < 9:
                strRet = "0%s" % intVal
            else:
                strRet = str(strVal)
        return strRet
        
    def SetupDateInfoByDate(self, filterYear, filterMonth, filterDay):
        dteFrom = datetime.date(int(filterYear), filterMonth, filterDay)
        dteTo = datetime.date(int(filterYear), filterMonth, filterDay)
        self.predefined_dates['bydate'] = self.dictGetDateInfo(dteFrom, 1)
        oRetVal = self.predefined_dates['bydate']
        return oRetVal


    def dictGetDateInfo(self, dteVal, lengthDays):
        #returns a dictionary containing, actualDate, gqlWhereFrom, gqlWhereTo, FormattedDate
        retval = {}

        #init
        dteFrom = dteVal + datetime.timedelta(days=-1)
        dteTo = dteVal  + datetime.timedelta(days=lengthDays)

        retval = self.createDict(dteVal, dteFrom, dteTo, lengthDays)
        return retval

    def dictGetDateInfoBetweenDates(self, dteFrom, dteTo, lengthDays):
        #returns a dictionary containing, actualDate, gqlWhereFrom, gqlWhereTo, FormattedDate
        retval = {}

        #init
        dteFrom = dteFrom + datetime.timedelta(days=-1)
        dteTo = dteTo  + datetime.timedelta(days=1)

        retval = self.createDict(dteFrom, dteFrom, dteTo, lengthDays)
        return retval

    def dictGetDateInfoThisMonth(self, dteVal):
        filterMonth = dteVal.month
        filterYear = dteVal.year
        nextMonth = filterMonth + 1
        nextYear = filterYear
        if nextMonth> 12:
            nextMonth= 1
            nextYear = nextYear+ 1
        dteFrom = datetime.date(filterYear, filterMonth, 1) + datetime.timedelta(days=-1)
        dteTo= datetime.date(nextYear, nextMonth, 1)

        retval = self.createDict(dteFrom, dteFrom, dteTo, 30)
        return retval


    def createDict(self, actualDate, gqlWhereFrom, gqlWhereTo, lengthDays):
        retval = {}
        dateFormat = self.output_formats[0]
        formattedDate = str(actualDate.strftime(dateFormat))
        retval['actualDate'] = actualDate
        retval['gqlWhereFrom'] = gqlWhereFrom
        retval['gqlWhereTo'] = gqlWhereTo
        retval['FormattedDate'] = formattedDate
        
        if lengthDays > 1:
            dteDisplayFrom = gqlWhereFrom  + datetime.timedelta(days=1)
            dteDisplayTo = gqlWhereTo  + datetime.timedelta(days=-1)
            formattedDateFrom = str(dteDisplayFrom.strftime(dateFormat))
            formattedDateTo = str(dteDisplayTo.strftime(dateFormat))
            retval['FormattedDate'] = "%s - %s" % (formattedDateFrom, formattedDateTo)

        return retval