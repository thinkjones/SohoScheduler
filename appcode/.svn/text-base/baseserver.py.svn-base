from google.appengine.ext import db
from google.appengine.api import users
import appcode.baseclass
import datetime
import time

EMPTY_VALUES = (None, '')

class BaseServer():
    def __init__(self,DataEntityBaseModel=None,entity_ref_field_name=None,active_field_name=None,request=None):
        self.datastore_entity = DataEntityBaseModel
        self.entity_ref_field_name = entity_ref_field_name
        self.active_field_name = active_field_name
        self.session = None
        if request is not None:
            self.session = request.session
        #self.signup_instance = about.helpers.ServerSignup()

    def Get(self, pk_id_or_key):
        dataobj = None
        pk_id_or_key = str(pk_id_or_key)
        if pk_id_or_key is None:
            return None
        if pk_id_or_key.isdigit():
            dataobj = self.GetByID(pk_id_or_key)
        else:
            dataobj = self.GetByKey(pk_id_or_key)
        return dataobj

    def GetByID(self, pk_id):
        dataobj = None
        try:
            dataobj = self.datastore_entity.get(db.Key.from_path(self.datastore_entity.kind(), int(pk_id)))
        except:
            dataobj = None
        return dataobj

    def GetByKey(self, key_name):
        dataobj = self.datastore_entity.get_by_key_name(key_name)
        return dataobj
    
    def GetByEntity(self,entity,is_active=True):
        if self.entity_ref_field_name is None:
            return None

        querySet = None
        strGQL = None
        if self.active_field_name:
            strGQL = "WHERE %s = :1 and %s  = :2" % (self.active_field_name,self.entity_ref_field_name)
            querySet = self.datastore_entity.gql(strGQL, is_active, entity)
        else:
            strGQL = "WHERE %s  = :1" % self.entity_ref_field_name
            querySet = self.datastore_entity.gql(strGQL, entity)

        total_count = querySet.count()
        return querySet.fetch(limit=100)

    def GetByEntityJsonDict(self, entity, list_field,filteredlist=None):
        gqlresults = filteredlist
        if filteredlist is None:
            gqlresults = self.GetByEntity(entity)

        #Pass in a field dictionary and this will return a dictionary with all your favourite fields in.
        listresults = []
        for gqr in gqlresults:
            dictRow = self.getRowDict(gqr, list_field)
            listresults.append(dictRow)
        return listresults

    def getRowDict(self, row, list_field):
        newRow = {}
        newRow['id'] = str(row.key().id())
        newRow['key'] = str(row.key())
        for efield in row.properties():
            if efield in list_field:
                new_value = self.datastore_entity.properties()[efield].get_value_for_datastore(row)
                newRow[efield] = new_value
        return newRow

    def getRowAsDict(self, row):
        newRow = {}
        newRow['id'] = str(row.key().id())
        newRow['key'] = str(row.key())
        for efield in row.properties():
            new_value = self.datastore_entity.properties()[efield].get_value_for_datastore(row)
            newRow[efield] = new_value
        return newRow

    def getDateFromString(self, value, format):
        dte = None
        if value in EMPTY_VALUES:
            return None
        try:
            if isinstance(value, str) or isinstance(value, unicode):
                dte = datetime.datetime.strptime(value, format)
            return dte
        except ValueError:
            dte = None
        return None

    def GetGParam(self, strKey):
        return appcode.baseclass.GlobalHelper().GetGParam(strKey)

    def setSessionVal(self, session_key, initial_Value):
        session_val_test = None
        try:
            self.session[session_key] = initial_Value
        except KeyError:
            session_val_test = None
        return session_val_test

    def getSessionVal(self, session_key):
        if self.session is None:
            return None
        
        session_val_test = None
        try:
            session_val_test = self.session[session_key]
        except KeyError:
            session_val_test = None
        return session_val_test

    def Delete(self, pk_id_or_key):
        dataobj = self.Get(pk_id_or_key)
        bolRet = True
        try:
            dataobj.active = False
            dataobj.put()
        except KeyError:
            bolRet = False
        return bolRet
