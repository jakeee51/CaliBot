class Server(object):
  __slots__ = ("name", "server", "verify", "general")
  def __init__(self, name, server, verify, general):
    self.name = name
    self.server = server
    self.verify = verify
    self.general = general

brothers = Server("brothas", 630888887375364126, 688625250832744449, 631090067963772931)
sisters = Server("sistas", 0, 0, 0)
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
