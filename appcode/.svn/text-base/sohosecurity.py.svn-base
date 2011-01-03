import entity.helpers
from google.appengine.api import users

entity_access_rights = {
    'Owner':False,
    'Edit':False,
    'View':False,
}

from appengine_utilities.sessions import Session
request_session = Session()

def authenticate(required_access_code_mnemonic):
    if required_access_code_mnemonic is None:
        #Assume strictest security
        required_access_code_mnemonic = 'Owner'
    def authenticate2(f):
        def wrap(*args, **kwargs):
            #0. Init
            bol_is_authenticated = False
            entity_id = 0

            #1. Get Entity ID
            for key in kwargs:
                if key =='entity_id':
                    entity_id = kwargs[key]

            #2. Determine Entities Access
            request = request_session

            #3. Determine authentication
            bol_is_authenticated = False
            if required_access_code_mnemonic == "Owner":
                bol_is_authenticated = SohoSecurityHelper().hasEntityOwnerAccess(entity_id)

            if required_access_code_mnemonic == "Edit":
                bol_is_authenticated = SohoSecurityHelper().hasEntityEditAccess(entity_id)

            if required_access_code_mnemonic == "View":
                bol_is_authenticated = SohoSecurityHelper().hasEntityReadAccess(entity_id)

            #3. If entity is 0 then always authenticated
            if str(entity_id) == "0":
                bol_is_authenticated = True
            
            #4. Is this user an admin devloper user?
            if users.IsCurrentUserAdmin():
                bol_is_authenticated = True

            #2. Determine Response
            if bol_is_authenticated:
                return f(*args, **kwargs)
            else:
                if IsAjaxRequest(request):
                    #Send Back an ajax no access
                    jsontext = simplejson.dumps({'response': False, 'access_level': 'No Access'})
                    return HttpResponse(jsontext, "application/json")
                else:
                    import about.views
                    access_rights = getAccessRights(request)
                    return about.views.errorpage(request,access_rights)
        return wrap
    return authenticate2

class SohoSecurityHelper():
    def __init__(self,request_session=None):
        self.session = None
        if request_session:
            self.session = request_session
        else:
            import appengine_utilities.sessions
            self.session = appengine_utilities.sessions.Session()
        
    def getAccessRights(self):
        import appcode.baseserver
        access_rights = self.session.get('access_rights')
        refresh_this_session = self.session.get('refresh_session', True)
        if access_rights is None or refresh_this_session:
            access_rights = entity.helpers.HelperSignupEntityAccess().getUserAccessRightsAsList()
            self.session['access_rights'] = access_rights
        return access_rights

    def getEntityRenderType(self,entity_id):
        access_rights = self.getAccessRights()
        entity_render_type = "0"
        for each_right in access_rights:
            if str(entity_id) == str(each_right['entity_id']):
                entity_render_type = str(each_right['entity_render_type'])
        return entity_render_type

    def getEntityAccessRights(self,entity_id):
        entity_access_rights['Owner'] = self.hasEntityOwnerAccess(entity_id)
        entity_access_rights['Edit'] = self.hasEntityEditAccess(entity_id)
        entity_access_rights['View'] = self.hasEntityReadAccess(entity_id)
        return entity_access_rights

    def hasEntityOwnerAccess(self,entity_id):
        has_access = False
        has_access = self.hasEntityRequiredAccess(entity_id,'Owner')
        return has_access

    def hasEntityEditAccess(self,entity_id):
        has_access = False
        has_access = self.hasEntityRequiredAccess(entity_id,'Edit')
        return has_access

    def hasEntityReadAccess(self,entity_id):
        has_access = False
        has_access = self.hasEntityRequiredAccess(entity_id,'View')
        return has_access

    def hasEntityRequiredAccess(self,entity_id, access_code_mnemonic):
        #returns true
        # For a user to have Read Only Access it must have an entry in the sesion dictionary for this user
        access_rights = self.getAccessRights()

        if access_rights is None:
            return False

        if_owner = False
        if_edit = False
        if_read = False

        if access_code_mnemonic == "Owner":
            if_owner = True

        if access_code_mnemonic == "Edit":
            if_owner = True
            if_edit = True

        if access_code_mnemonic == "View":
            if_owner = True
            if_edit = True
            if_read = True

        has_access = False
        for each_right in access_rights:
            if str(entity_id) == str(each_right['entity_id']):
                if str(each_right['access_right_code']) == "Owner":
                    if has_access == False:
                        has_access = if_owner
                elif str(each_right['access_right_code']) == "Edit":
                    if has_access == False:
                        has_access = if_edit
                elif str(each_right['access_right_code']) == "View":
                    if has_access == False:
                        has_access = if_read
        return has_access


