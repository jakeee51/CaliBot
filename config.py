class Server(object):
   #__slots__ = ("name", "wait", "general")
   def __init__(self, name, wait, general, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general

__bro_options = {}
__sis_options = {}
SERVER_ID = 630888887375364126
VERIFY_ID = 688625250832744449
brothers = Server("Brother", 748745649746477086, 631090067963772931)
sisters = Server("Sister", 748761869480624158, 748762901531066458)
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
