import os
import random
import sys

import unittest

sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(__file__),
      "../src/spotify"
    )
  )
)

from SettingsManager import SettingsManager

class TestSettingsManager(unittest.TestCase):
  def test_refresh_interval_in_seconds_should_default_to_5_if_load_settings_raises_an_exception(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: self.__throw_up())

  def test_refresh_interval_in_seconds_should_default_to_5_if_it_is_not_specified(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: None)

  def test_refresh_interval_in_seconds_should_default_to_5_if_it_is_not_int(self):
    self.__test_default_refresh_interval_in_seconds(lambda key: "not int")

  def test_refresh_interval_in_seconds_should_default_to_5_if_input_is_less_than_1(self):
    minimum = 1

    self.__test_default_refresh_interval_in_seconds(lambda key: minimum - 1)
    self.__test_default_refresh_interval_in_seconds(lambda key: random.randint(-123456789, minimum - 1))

  def test_refresh_interval_in_seconds_should_default_to_5_if_input_is_greater_than_15(self):
    maximum = 15

    self.__test_default_refresh_interval_in_seconds(lambda key: maximum + 1)
    self.__test_default_refresh_interval_in_seconds(lambda key: random.randint(maximum + 1, 123456789))

  def test_refresh_interval_in_seconds_should_be_a_valid_integer_between_1_and_15(self):
    minimum = 1
    maximum = 15

    self.__test_valid_refresh_interval_in_seconds(minimum)
    self.__test_valid_refresh_interval_in_seconds(maximum)
    self.__test_valid_refresh_interval_in_seconds(random.randint(minimum, maximum))

  def test_is_enabled_should_default_to_False_if_load_settings_raises_an_exception(self):
    self.__test_default_is_enabled(lambda key: self.__throw_up())

  def test_is_enabled_should_default_to_False_if_it_is_not_specified(self):
    self.__test_default_is_enabled(lambda key: None)

  def test_is_enabled_should_default_to_False_if_input_is_not_bool(self):
    self.__test_default_is_enabled(lambda key: "bool")

  def test_is_enabled_should_be_a_valid_bool(self):
    self.__test_valid_is_enabled(True)
    self.__test_valid_is_enabled(False)

  def __throw_up(self):
    raise Exception

  def __test_default_refresh_interval_in_seconds(self, load_settings):
    loader = SettingsManager(FakeReaderWriter(read = load_settings))
    actual = loader.refresh_interval_in_seconds()
    self.assertEquals(actual, 5)

  def __test_valid_refresh_interval_in_seconds(self, expected):
    loader = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    actual = loader.refresh_interval_in_seconds()
    self.assertEqual(actual, expected)

  def __test_default_is_enabled(self, load_settings):
    loader = SettingsManager(FakeReaderWriter(read = load_settings))
    self.__test_is_enabled(loader, False)

  def __test_valid_is_enabled(self, expected):
    loader = SettingsManager(FakeReaderWriter(read = lambda key: expected))
    self.__test_is_enabled(loader, expected)

  def __test_is_enabled(self, loader, expected):
    actual_enabled = loader.is_enabled()
    self.assertEqual(actual_enabled, expected)

    actual_disabled = loader.is_disabled()
    self.assertEqual(actual_disabled, not expected)

class FakeReaderWriter:
  def __init__(self, read, write = None):
    self.__read = read
    self.__write = write

  def read_setting(self, key):
    return self.__read(key)

  def write_setting(self, key, value):
    return self.__write(key, value)
