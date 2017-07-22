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

  def test_refresh_interval_in_seconds_should_default_to_5_if_it_is_not_set(self):
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

  def __test_default_refresh_interval_in_seconds(self, load_settings):
    loader = SettingsManager(FakeReaderWriter(read = load_settings))
    actual = loader.refresh_interval_in_seconds()
    self.assertEquals(actual, 5)

  def __throw_up(self):
    raise Exception

class FakeReaderWriter:
  def __init__(self, read, write = None):
    self.__read = read
    self.__write = write

  def read_setting(self, key):
    return self.__read(key)

  def write_setting(self, key, value):
    return self.__write(key, value)
