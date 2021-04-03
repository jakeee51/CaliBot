class Server(object):
   #__slots__ = ("name", "wait", "general")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

class StaticMsg(object):
   __slots__ = ("channel", "message", "reaction")
   def __init__(self, channel, message, reaction):
      self.channel = channel
      self.message = message
      self.reaction = reaction

__bro_options = {"role_select": 756318101880176752}
__sis_options = {"role_select": 750886997874311179,
                 "among_us": 771840748042584124}

brothers = Server("Brother", 748745649746477086,
                  631090067963772931, 687402472586870849,
                  **__bro_options)
sisters = Server("Sister", 748761869480624158,
                 748762901531066458, 748764105686384650,
                 **__sis_options)

SERVER_ID = 630888887375364126
VERIFY_ID = 688625250832744449
'''
- Create 'Muslim' role or w/e you wanna call the role that
  every sister gets to officially join
- Create #verify chat
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chat
- Make @everyone role only able to talk in #verify chat
'''
