class Waiter(object):
    """A waiter object."""

    def __init__(self, waiter=None, waitee=None, chat=None):
        self.waiter = waiter
        self.waitee = waitee
        self.chat = chat

class Wait(object):
    """Waits for people to appear."""

    def __init__(self):
        self.commands = {"wait": self.wait}
        self.passive = [self._watch]

        self.waitlist = [] #list of Waiter objects

    def _watch(self):
        """passive"""

        if not self.waitlist:
            return

        for waiter in self.waitlist:
            if self.message.FromHandle == waiter.waitee:
                self.skype.SendMessage(waiter.waiter, "User " + waiter.waitee + " has appeared.")
                self.waitlist.remove(waiter)

        #self.chat.SendMessage(self.message.Body)

    def wait(self):
        """active"""

        msg = self.message
        waiter = Waiter(waiter=msg.FromHandle, waitee=msg.Body.split()[1],
                            chat=self.chat)

        self.waitlist.append(waiter)
        self.chat.SendMessage("Understood. I will let you know when they appear.")

Class = Wait
