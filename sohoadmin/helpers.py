from appcode.baseclass import *
from appcode.dataserver import *

class HelperApplicationParams():

    def GetAllBase(self):
        q = db.GqlQuery("SELECT * FROM ApplicationParams")
        results = q.fetch(50)
        return results

    def GetAllAsDict(self):
        results = self.GetAllBase()
        fooDict = {}
        for foo in results:
            fooDict[foo.param_name] = foo.param_value
        return fooDict

    def InsertDefaultValues(self):
        #1. Get all parameters
        current_params = {}
        results = self.GetAllBase()
        for foo in results:
            current_params[foo.param_name] = foo.param_value
        default_params = default_application_parameters

        #2. Loop through defaults and check they are all present in the application
        for dParamKey in default_params.keys():
            if current_params.has_key(dParamKey) == False:
                self.SaveDefaultParameter(dParamKey)

    def SaveDefaultParameter(self, dParamKey):
        param_name = dParamKey
        param_value = default_application_parameters[dParamKey]
        newParam = ApplicationParams(param_name=param_name,param_value=param_value)
        newParam.put()

    def GetParam(self, param_name):
        entity_param = None
        entity_params = sohoadmin.models.ApplicationParams.gql("WHERE  param_name = :1", param_name)
        if entity_params.count() > 0:
            entity_param = entity_params[0]
        return entity_param

    def SaveParam(self, dParamKey, dParamValue):
        current_param = self.GetParam(dParamKey)
        if current_param is None:
            current_param = sohoadmin.models.ApplicationParams(param_name=dParamKey,param_value=dParamValue)
        else:
            current_param.param_value=dParamValue
        current_param.put()            


