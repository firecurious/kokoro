class Channel(object):
    """Skype channel stuff."""

    def __init__(self):
        self.commands = {"newchat": self.make_chat}
        self.passive = []      

    def make_chat(self):
        """active"""

        text = self.message.Body.split("!newchat ")[1]
        people = text.split()

        chat = self.skype.CreateChatWith(*people)
        chat.SendMessage("Welcome, humans!")

Class = Channel
