import google
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from appcode.mailhelper import *
import about.helpers
from entity.helpers import *
from google.appengine.ext import deferred

class TaskQueueHelper():
    def GetQueue(self, queue_name):
        return google.appengine.api.labs.taskqueue.Queue(name=queue_name)
    
    def CreateNewUserTasks(self, signupuser_id):
        #1. Get queue
        emailQueue = self.GetQueue('mail-queue')
        newTask = google.appengine.api.labs.taskqueue.Task(url='/sohoadmin/queue/newusertask/', params={'id': signupuser_id})
        emailQueue.add(newTask)

    def CreateCopyEntityTask(self, src_entity_id, dest_entity_id):
        #1. Get queue
        #bpQueue = self.GetQueue('background-processing')
        #newTask = google.appengine.api.labs.taskqueue.Task(url='/admin/queue/copyentitytask/', params={'src_entity_id': src_entity_id, 'dest_entity_id': dest_entity_id})
        #bpQueue.add(newTask)
        deferred.defer(self.CopyEntity, src_entity_id, dest_entity_id)

    def CreateCheckEntityForForms(self, entity_id):
        #1. Get queue
        bpQueue = self.GetQueue('background-processing')
        newTask = google.appengine.api.labs.taskqueue.Task(url='/sohoadmin/queue/checkentityforforms/', params={'entity_id': entity_id})
        bpQueue.add(newTask)

    def RunTask(self, dictRequestPost, taskName):
        if taskName == "newusertask":
            user_id = dictRequestPost['id']
            self.ProcessNewSignupUser(user_id)
        if taskName == 'copyentitytask':
            src_entity_id =  int(dictRequestPost['src_entity_id']) #int('735')  #
            dest_entity_id = int(dictRequestPost['dest_entity_id'])  #int('763')  #
            self.CopyEntity(src_entity_id,dest_entity_id)
        if taskName == 'checkentityforforms':
            entity_id =  int(dictRequestPost['entity_id']) #int('735')  #
            CreateBasicApplicationForExistingEntity(entity_id)            
        return None

    def ProcessNewSignupUser(self, id):
        self.EmailNewUserWithWelcomeEmail(id)

    def CopyEntity(self, src_entity_id, dest_entity_id):
        CreateTemplateFromEntity(src_entity_id,dest_entity_id)
        
    def EmailNewUserWithWelcomeEmail(self, id):
        #1. Create email message
        signupUser = about.helpers.ServerSignup().Get(id)
        toEmail = signupUser.signup_user.email()
        subject = "Welcome to Soho Scheduler"
        body = """
            Welcome to Soho Scheduler. 
            
            Soho Scheduler is an online appointment scheduling tool focused on the needs of small businesses.
            
            We offer a personalized service and can help with any question or enhancement ideas you may have.  If you need to get in contact to discuss
            the application feel free to contact us at business@sohoappspot.com.

            We appreciate your interest and look forward to working with you in the near future.

            Regards
            The Soho Scheduler Team
            www.sohoappspot.com
        """

        #2. Mark as sent

        #3. Send email
        mailHelper = SohoMailHelper(toEmail=toEmail, strSubject=subject, strMessageBody=body)
        mailHelper.send()

        return None
