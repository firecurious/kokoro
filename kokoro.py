import Skype4Py
import time
import importlib
import traceback
import csv

skype = Skype4Py.Skype()
skype.Attach()

class Command(object):

    def __init__(self, name=None, method=None, plugin=None, plugin_name=None):
        self.name = name #name of command (string)
        self.method = method #the method the command uses (method)
        self.plugin = plugin #the associated plugin object (object)
        self.plugin_name = plugin_name #name of the plugin (string)

class Bot(object):
    """Pluggable Skype bot that interacts with P2P chats."""

    def __init__(self, bot_name):
        """Takes a string."""

        self.name = bot_name
        self.plugins = {} #plugin_name: object
        self.commands = [] #list of active command_objects
        self.passive = [] #list of passive command_objects

        self._load_plugins()

    def _load_plugins(self):
        """Loads all plugins in plugins.csv."""

        with open("plugins.csv", 'r') as f:
            plugins = [line[0] for line in csv.reader(f)]

            for plugin in plugins:
                self._load(plugin)
                print "loading", plugin + "..."

    def _see_chats(self):
        """Returns a list of P2P chats, aka the only kind Skype4Py can use."""
        return [c for c in skype.Chats if c.Topic]

    def _update_plugins(self):
        """Writes a list of keys from self.plugins to plugins.csv."""

        with open("plugins.csv", 'w') as f:
            data = [[p] for p in self.plugins]
            writer = csv.writer(f)

            writer.writerows(data) 

    def _load(self, plugin_name):
        """Loads a plugin and the commands from that plugin by sticking them
        into the commands and plugins dictionaries.

        Takes the string name of a plugin.
        """

        i = importlib.import_module("plugins.%s" %plugin_name).Class()

        if plugin_name not in self.plugins:
            self.plugins[plugin_name] = i
            plugin = self.plugins[plugin_name]
            plugin.skype = skype
        else:
            return "The specified plugin is already loaded. To reload it, restart me."

        for command in i.commands:
            if command not in self.commands:
                command_obj = Command(name=command,
                                        method=i.commands[command],
                                        plugin=plugin,
                                        plugin_name=plugin_name
                                        )
                self.commands.append(command_obj)

            else:
                return "Plugin not loaded. Conflict with '%s'." %command

        for command in i.passive:
            command_obj = Command(name="passive command",
                                    method=command,
                                    plugin=plugin,
                                    plugin_name=plugin_name
                                    )

            self.passive.append(command_obj)

        self._update_plugins()

        return "Loaded."

    def _reply(self, chat, message):
        """Takes a chat object and a message object. Reads the message, then
        determines what should be done with it based on plugin commands.
        """

        message.MarkAsSeen()

        body = message.Body
        handle = message.FromHandle

        #print message.Chat.Topic, "-", handle, body

        if "!load" in body:
            msg = self._load(body.split()[1])
            chat.SendMessage(msg)

        for command in self.commands:
            if body.startswith("!" + command.name):
                plugin = command.plugin

                plugin.message = message
                plugin.chat = chat

                command.method()

        for command in self.passive:
            command.plugin.chat = chat
            command.plugin.message = message
            command.method()

    def live(self):
        """Makes the bot read unread messages every second."""

        while True:
            #run _reply on each unread message in P2P chats bot is present in
            for message in [c for c in skype.MissedMessages]:
                try:
                    self._reply(message.Chat, message)

                #handle exceptions so the bot talks about them instead of crashing
                except Exception, e:
                    message.Chat.SendMessage("ERROR: " + str(e))
                    traceback.print_exc()

            time.sleep(1)

kokoro = Bot("Kokoro")
kokoro.live()
