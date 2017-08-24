import random
import sys

import unittest

SettingsManagerModule = sys.modules["SpotifyWeb.src.spotify.SettingsManager"]

SettingsManager = SettingsManagerModule.SettingsManager

class TestSettingsManager(unittest.TestCase):
  def test_redirect_port_should_default_to_8080_if_load_settings_raises_an_exception(self):
    self.__test_default_redirect_port(lambda key: self.__raiseException())

  def test_redirect_port_should_default_to_8080_if_it_is_not_specified(self):
    self.__test_default_redirect_port(lambda key: None)

  def test_redirect_port_should_default_to_8080_if_it_is_not_int(self):
    self.__test_default_redirect_port(lambda key: "not int")

  def test_redirect_port_should_default_to_8080_if_input_is_less_than_1024(self):
    minimum = 1024

    self.__test_default_redirect_port(lambda key: minimum - 1)
    self.__test_default_redirect_port(lambda key: random.randint(-123456789, minimum - 1))

  def test_redirect_port_should_default_to_8080_if_input_is_greater_than_65535(self):
    maximum = 65535

    self.__test_default_redirect_port(lambda key: maximum + 1)
    self.__test_default_redirect_port(lambda key: random.randint(maximum + 1, 123456789))

  def test_redirect_port_should_be_a_valid_integer_between_1024_and_65535(self):
    minimum = 1024
    maximum = 65535

    self.__test_valid_redirect_port(minimum)
    self.__test_valid_redirect_port(maximum)
    self.__test_valid_redirect_port(random.randint(minimum, maximum))

  def test_refresh_interval_in_seconds_should_default_to_5_if_load_settings_raises_an_exception(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: self.__raiseException())

  def test_refresh_interval_in_seconds_should_default_to_5_if_it_is_not_specified(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: None)

  def test_refresh_interval_in_seconds_should_default_to_5_if_it_is_not_int(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: "not int")

  def test_refresh_interval_in_seconds_should_default_to_5_if_input_is_less_than_2(self):
    minimum = 2

    self.__test_default_refresh_interval_in_seconds(lambda key: minimum - 1)
    self.__test_default_refresh_interval_in_seconds(lambda key: random.randint(-123456789, minimum - 1))

  def test_refresh_interval_in_seconds_should_default_to_5_if_input_is_greater_than_15(self):
    maximum = 15

    self.__test_default_refresh_interval_in_seconds(lambda key: maximum + 1)
    self.__test_default_refresh_interval_in_seconds(lambda key: random.randint(maximum + 1, 123456789))

  def test_refresh_interval_in_seconds_should_be_a_valid_integer_between_2_and_15(self):
    minimum = 2
    maximum = 15

    self.__test_valid_refresh_interval_in_seconds(minimum)
    self.__test_valid_refresh_interval_in_seconds(maximum)
    self.__test_valid_refresh_interval_in_seconds(random.randint(minimum, maximum))

  def test_is_enabled_should_default_to_False_if_load_settings_raises_an_exception(self):
    self.__test_default_is_enabled(lambda key: self.__raiseException())

  def test_is_enabled_should_default_to_False_if_it_is_not_specified(self):
    self.__test_default_is_enabled(lambda key: None)

  def test_is_enabled_should_default_to_False_if_input_is_not_bool(self):
    self.__test_default_is_enabled(lambda key: "not bool")

  def test_is_enabled_should_be_a_valid_bool(self):
    self.__test_valid_is_enabled(True)
    self.__test_valid_is_enabled(False)

  def test_client_id_should_raise_an_exception_if_it_is_not_specified(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: None))
    expected = "Please specify SpotifyWeb_string_client_id in Preferences -> Package Settings -> SpotifyWeb -> Settings"

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_id()

  def test_client_id_should_raise_an_exception_if_it_is_empty(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: ""))
    expected = "Please specify SpotifyWeb_string_client_id in Preferences -> Package Settings -> SpotifyWeb -> Settings"

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_id()

  def test_client_id_should_raise_an_exception_if_it_is_not_string(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: 1337))
    expected = "Expected SpotifyWeb_string_client_id to be of {}, but was {}".format(type(""), type(1337))

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_id()

  def test_valid_client_id(self):
    expected = "some key"
    manager = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    actual = manager.client_id()
    self.assertEqual(actual, expected)

  def test_client_secret_should_raise_an_exception_if_it_is_not_specified(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: None))
    expected = "Please specify SpotifyWeb_string_client_secret in Preferences -> Package Settings -> SpotifyWeb -> Settings"

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_secret()

  def test_client_secret_should_raise_an_exception_if_it_is_empty(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: ""))
    expected = "Please specify SpotifyWeb_string_client_secret in Preferences -> Package Settings -> SpotifyWeb -> Settings"

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_secret()

  def test_client_secret_should_raise_an_exception_if_it_is_not_string(self):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: 1337))
    expected = "Expected SpotifyWeb_string_client_secret to be of {}, but was {}".format(type(""), type(1337))

    with self.assertRaisesRegexp(Exception, expected):
      manager.client_secret()

  def test_valid_client_secret(self):
    expected = "some key"
    manager = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    actual = manager.client_secret()
    self.assertEqual(actual, expected)

  def test_toggle(self):
    actualKey = "SpotifyWeb_bool_is_enabled"
    actualValue = True

    def read(key):
      return actualValue

    def write(key, value):
      nonlocal actualKey
      actualKey = key

      nonlocal actualValue
      actualValue = value

    manager = SettingsManager(FakeReaderWriter(read, write))

    manager.toggle()
    self.assertEqual(actualKey, "SpotifyWeb_bool_is_enabled")
    self.assertEqual(actualValue, False)

    manager.toggle()
    self.assertEqual(actualKey, "SpotifyWeb_bool_is_enabled")
    self.assertEqual(actualValue, True)

  def __raiseException(self):
    raise Exception

  def __test_default_redirect_port(self, load_settings):
    manager = SettingsManager(FakeReaderWriter(read = load_settings))
    actual = manager.redirect_port()
    self.assertEquals(actual, 8080)

  def __test_valid_redirect_port(self, expected):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    actual = manager.redirect_port()
    self.assertEqual(actual, expected)

  def __test_default_refresh_interval_in_seconds(self, load_settings):
    manager = SettingsManager(FakeReaderWriter(read = load_settings))
    actual = manager.refresh_interval_in_seconds()
    self.assertEquals(actual, 5)

  def __test_valid_refresh_interval_in_seconds(self, expected):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    actual = manager.refresh_interval_in_seconds()
    self.assertEqual(actual, expected)

  def __test_default_is_enabled(self, load_settings):
    manager = SettingsManager(FakeReaderWriter(read = load_settings))
    self.__test_is_enabled(manager, False)

  def __test_valid_is_enabled(self, expected):
    manager = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    self.__test_is_enabled(manager, expected)

  def __test_is_enabled(self, manager, expected):
    actual_enabled = manager.is_enabled()
    self.assertEqual(actual_enabled, expected)

    actual_disabled = manager.is_disabled()
    self.assertEqual(actual_disabled, not expected)

class FakeReaderWriter:
  def __init__(self, read, write = None):
    self.__read = read
    self.__write = write

  def read_setting(self, key):
    return self.__read(key)

  def write_setting(self, key, value):
    return self.__write(key, value)
