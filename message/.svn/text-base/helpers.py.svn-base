from appcode.dataserver import *
import message.helpers


class HelperUserMessage():
    def ProcessMessages(self, user):
        #1. Get User Messages That Are Set
        usermessages = None
        usermessages = self.GetUserMessages()

        #2. Get User Messages required
        messages_required = None
        messages_required = self.GetShowNowMessages()

        #3. Loop through messages_required and check they are all in User Messages
        for reqmes in messages_required:
            messagesFound = message.helpers.HelperUserMessage().GetUserMessageByUserAndMessage(reqmes,  user)
            totalMessages = messagesFound.count()
            if totalMessages == 0:
                ServerUserMessage().CreateUserMessageFromMessage(reqmes, user)

    def GetShowNowMessages(self):
        #1. Get Messages Already Seen
        messages = None
        messages = message.models.Message.gql("Where show_now = True")
        return messages

    def CreateMessage(self, message_mnemonic, message_title, message_description, message_href,  tab_name, message_class):
        newMessage = Message(
                                    message_mnemonic = message_mnemonic,
                                    message_title = message_title,
                                    message_description = message_description,
                                    message_href = message_href,
                                    message_class = message_class,
                                    tab_name = tab_name
                            )
        newMessage.put()

    def GetUserMessagesByTab(self, tab_name):
        #1. Get Messages Already Seen
        usermessages = None
        usermessages = message.models.UserMessage.gql("Where owner = :1 and tab_name = :2 ", users.get_current_user(), tab_name)
        return usermessages

    def GetUserMessages(self):
        #1. Get Messages Already Seen
        usermessages = None
        usermessages = message.models.UserMessage.gql("Where owner = :1", users.get_current_user())
        return usermessages

    def GetUserMessagesByTabForDisplay(self, tab_name):
        #1. Get Messages Already Seen
        usermessages = None
        usermessages = message.models.UserMessage.gql("Where user_has_seen = False and owner = :1 and tab_name = :2 ", users.get_current_user(), tab_name)
        return usermessages

    def GetUserMessageByUserAndMessage(self, parentMessage, ownerUser):
        #1. Get Messages Already Seen
        usermessages = None
        usermessages = message.models.UserMessage.gql("Where owner = :1 and message_reference = :2",  ownerUser,  parentMessage)
        return usermessages

    def CreateUserMessageFromMessage(self, message, user):
        newUserMessage = UserMessage()
        newUserMessage.owner = user
        newUserMessage.message_title = message.message_title
        newUserMessage.message_description = message.message_description
        newUserMessage.message_href = message.message_href
        newUserMessage.message_class = message.message_class
        newUserMessage.tab_name = message.tab_name
        newUserMessage.message_reference = message
        newUserMessage.put()

    def getUserMessage(self,  message_id):
        um = None
        try:
            um = UserMessage.get(db.Key.from_path(UserMessage.kind(), int(message_id)))
        except:
            um = None
        return um

    def MarkMessageAsRead(self, message_id):
        um = self.getUserMessage(message_id)
        thisUser = users.get_current_user()
        if um.owner == thisUser:
            um.user_has_seen = True
            um.user_read_date = datetime.datetime.today()
            um.put()
