import appcode.baseclass
from google.appengine.api import mail

class SohoMailHelper():
    def __init__(self, fromEmail=None, toEmail=None, strSubject=None, strMessageBody=None):
        self.FromEmail = fromEmail
        self.ToEmail = toEmail
        self.Subject = strSubject
        self.MessageBody = strMessageBody
        self.mail_send_rule = self.GetGParam('mail_send_rule')
        self.test_mail_account = self.GetGParam('test_mail_account')

    def GetGParam(self, strKey):
        return appcode.baseclass.GlobalHelper().GetGParam(strKey)

    def send(self):
        if not mail.is_email_valid(self.ToEmail):
            return False

        if self.FromEmail is None:
            mail_send_from_email = self.GetGParam('mail_send_from_email')
            self.FromEmail = mail_send_from_email

        if self.mail_send_rule == "live":
            mail.send_mail(sender=self.FromEmail, to=self.ToEmail,subject=self.Subject, body=self.MessageBody)
            return True

        if self.mail_send_rule == "test":
            test_subject = "[%s] %s" % (self.ToEmail, self.Subject)
            mail.send_mail(sender=self.FromEmail,to=self.test_mail_account, subject=test_subject, body=self.MessageBody)
            return True

        return True