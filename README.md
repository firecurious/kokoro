# Kokoro #
Run the bot using
`$cd kokoro`
`$python kokoro.py`

A couple of things are hard-coded. I'm sorry. I'm working on it.

When you first run the bot, Skype will ask if Skype4Py can connect to it. If you want to give the bot its own Skype account, run the bot's account as your primary instance of Skype, and run your account as a secondary instance. You can run a second instance on Ubuntu by running `$skype --secondary` in the terminal.

The bot checks for unread messages every second.

# Plugins #

Stick plugins into the plugins directory. Load plugins for the first time by saying !load to the bot on Skype. This will put the plugin name into `plugins.csv`, and the bot will then load it when it starts up.

Each plugin is a `.py` file in the plugins folder. The plugin must contain a class, and have a Class variable referring to that class. In `__init__` in that class, there is a self.commands dictionary containing key: value pairs of command_name: method for active commands, and a self.passive list for passive commands.

Active commands are commands you can use by typing `!command` at the bot on Skype. Passive commands are methods that will run every time the bot sees a message.

Look at the `wait` plugin for an example of how to write a plugin using both active and passive commands.

Each plugin class is passed the values of `skype` (the Skype instance) when loaded, and `chat` (current chat) and `message` (current message) whenever the bot looks at an unread message. You can use these variables to interact with the Skype instance, the current chat, and the current message.

Stick plugins into the plugins directory. Load plugins for the first time by saying !load to the bot on Skype.