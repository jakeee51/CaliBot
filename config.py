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
__sis_options = {"role_select": 750886997874311179}

brothers = Server("Brother", 748745649746477086,
                  631090067963772931, 687402472586870849,
                  **__bro_options)
sisters = Server("Sister", 748761869480624158,
                 748762901531066458, 748764105686384650,
                 **__sis_options)

role_selection_s = (sisters.role_select, [StaticMsg(sisters.role_select,
                            "**Peer Mentee** :woman_with_headscarf:",
                            "\U0001f9d5"),
                  StaticMsg(sisters.role_select,
                            "**Senior** :older_woman:",
                            "\N{OLDER WOMAN}"),
                  StaticMsg(sisters.role_select,
                            "**Junior** :woman:",
                            "\N{WOMAN}"),
                  StaticMsg(sisters.role_select,
                            "**Sophmore** :girl:",
                            "\N{GIRL}"),
                  StaticMsg(sisters.role_select,
                            "**Freshmen** :baby:",
                            "\N{BABY}")])

role_selection_b = (brothers.role_select, [StaticMsg(brothers.role_select,
                            "**MATH Review** :straight_ruler:",
                            "\N{STRAIGHT RULER}"),
				  StaticMsg(brothers.role_select,
                            "**CS Review** :computer:",
                            "\N{DESKTOP COMPUTER}"),
                  StaticMsg(brothers.role_select,
                            "**PHYS Review** :atom:",
                            "\N{ATOM SYMBOL}"),
                  StaticMsg(brothers.role_select,
                            "**CHEM Review** :test_tube:",
                            "\N{TEST TUBE}")])

CONST_MSG = [role_selection_s, role_selection_b]
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
