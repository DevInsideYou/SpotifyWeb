class SettingsManager:
  def __init__(self, reader_writer):
    self.__read = reader_writer.read_setting
    self.__write = reader_writer.write_setting

  def redirect_port(self):
    default = 8080

    try:
      return self.__redirect_port(default)
    except:
      return default

  def __redirect_port(self, default):
    actual = self.__read("SublimeSpotifyRest_int_redirect_port")

    if 1024 <= actual <= 65535:
      return actual
    else:
      return default

  def refresh_interval_in_seconds(self):
    default = 5

    try:
      return self.__refresh_interval_in_seconds(default)
    except:
      return default

  def __refresh_interval_in_seconds(self, default):
    actual = self.__read("SublimeSpotifyRest_int_refresh_interval_in_seconds")

    if 1 <= actual <= 15:
      return actual
    else:
      return default

  def is_enabled(self):
    default = False

    try:
      return self.__is_enabled(default)
    except:
      return default

  def __is_enabled(self, default):
    actual = self.__read("SublimeSpotifyRest_bool_is_enabled")

    if not isinstance(actual, bool):
      return default
    else:
      return actual

  def is_disabled(self):
    return not self.is_enabled()

  def toggle(self):
    self.__write("SublimeSpotifyRest_bool_is_enabled", not self.is_enabled())
