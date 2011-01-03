from appcode.dataserver import *


def GetRecentUsers(number_to_get):
    import about.models
    query = about.models.Signup.gql("Order By created Desc Limit %s " % number_to_get)
    results = query.fetch(number_to_get)
    return results

def CreateUser():
    #1. Check if user has registered?
    current_signup = DataServer().getMySignup()

    #2. If not registered please log user
    if current_signup is None:
        current_signup = about.models.Signup(signup_user=users.get_current_user())
        current_signup.put()
        newUserID = current_signup.key().id()
        import appcode.taskqueuehelper
        appcode.taskqueuehelper.TaskQueueHelper().CreateNewUserTasks(newUserID)

    return current_signup

class HelperStoredToken():
    def GetBySignup(self, this_signup):
        qryST = None
        qryST = about.application_models.StoredToken.gql("WHERE signup_reference = :1", signup)
        qryCount = qryST.count()
        if qryST.count() > 0:
            return qryST[0]
        else:
            return None

    def GetBySignupAndPurpose(self,this_signup,this_purpose):
        qryST = None
        qryST = about.application_models.StoredToken.gql("WHERE signup_reference = :1 and purpose = :2", this_signup,this_purpose)
        qryCount = qryST.count()
        if qryST.count() > 0:
            return qryST[0]
        else:
            return None

    def RemoveToken(self,this_signup,purpose):
        this_token = self.GetBySignupAndPurpose(this_signup,purpose)
        if this_token:
            this_token.delete()
        return None

class HelperSignupExtendedProfile():

    def GetParam(self,param_type,this_signup_user=None):
        if this_signup_user is None:
            this_signup_user = DataServer().getMySignup()
        query = about.models.SignupExtendedProfile.all()
        query.filter("param_type =",  param_type)
        query.filter("signup_reference =",  this_signup_user)
        resultSet = query.fetch(1)
        countSet = query.count(1)
        retResult = None
        if countSet > 0:
            retResult = resultSet[0]
        return retResult

    def SetParam(self,param_type,param_value,this_signup_user=None):
        if this_signup_user is None:
            this_signup_user = DataServer().getMySignup()
        signup_user_param = self.GetParam(param_type,this_signup_user)
        bolRet = False
        if signup_user_param:
            signup_user_param.param_value = unicode(param_value)
            signup_user_param.put()
            bolRet = True
        else:
            newParam = about.models.SignupExtendedProfile(signup_reference=this_signup_user,
                                            param_type = param_type,
                                            param_value = unicode(param_value)
                                            )
            newParam.put()
            bolRet = True

        return bolRet

    def DeleteParam(self,  param_type):
        this_param = self.GetParam(param_type)
        if this_param:
            this_param.delete()
        return True

    def GetAll(self,signup_user=None):
        if signup_user is None:
            signup_user = DataServer().getMySignup()
        query = about.models.SignupExtendedProfile.all()
        query.filter("signup_reference =",  signup_user)
        countSet = query.count(100)
        if countSet == 0:
            self.SetupExtendedProfile(signup_user)
        resultSet = query.fetch(100)
        return resultSet

    def SetupExtendedProfile(self,signup_user):
        self.SetParam('has_used_designer','No',signup_user)
    
