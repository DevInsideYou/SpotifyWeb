class SettingsManager:
  def __init__(self, reader_writer):
    self.__read = reader_writer.read_setting
    self.__write = reader_writer.write_setting

  def client_id(self):
    return self.__read_credential(key = "SpotifyWeb_string_client_id")

  def client_secret(self):
    return self.__read_credential(key = "SpotifyWeb_string_client_secret")

  def __read_credential(self, key):
    actual = self.__read(key)

    if(actual is None or actual == ""):
      raise Exception(self.__key_missing(key))
    elif (not isinstance(actual, str)):
      raise Exception(self.__key_is_of_unexpected_type(key, type(""), type(actual)))
    else:
      return actual

  def __key_missing(self, key):
    return "Please specify {} in Preferences -> Package Settings -> SpotifyWeb -> Settings".format(key)

  def __key_is_of_unexpected_type(self, key, expected_type, actual_type):
    return "Expected {} to be of {}, but was {}".format(key, expected_type, actual_type)

  def redirect_port(self):
    default = 8080

    try:
      return self.__redirect_port(default)
    except:
      return default

  def __redirect_port(self, default):
    actual = self.__read("SpotifyWeb_int_redirect_port")

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
    actual = self.__read("SpotifyWeb_int_refresh_interval_in_seconds")

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
    actual = self.__read("SpotifyWeb_bool_is_enabled")

    if not isinstance(actual, bool):
      return default
    else:
      return actual

  def is_disabled(self):
    return not self.is_enabled()

  def toggle(self):
    self.__write("SpotifyWeb_bool_is_enabled", not self.is_enabled())
