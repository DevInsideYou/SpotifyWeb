import datetime

class Window:
  def __init__(self, status_bar_key):
    self.__views = {}
    self.__status_bar_key = status_bar_key

  def subscribe(self, view):
    self.__views.setdefault(view.id(), view)

  def unsubscribe(self, view):
    try:
      del self.__views[view.id()]
    except:
      pass

  def set_status_bar_message(self, message):
    # self.__debug_message(message)

    for view in self.__views.values():
      view.set_status(self.__status_bar_key, message)

  def __debug_message(self, message):
    timestamp = "{:%H:%M:%S}".format(datetime.datetime.now())

    print("{}: {}".format(timestamp, message))
