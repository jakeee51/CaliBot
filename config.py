class Server(object):
  __slots__ = ("server", "verify", "general")
  def __init__(self, server, verify, general):
    self.server = server
    self.verify = verify
    self.general = general

brothers = Server(630888887375364126, 688625250832744449, 631090067963772931)
##sisters = Server(0, 0, 0)
