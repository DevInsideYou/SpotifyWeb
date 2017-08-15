import os
import sys

import sublime
import unittest

sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(__file__),
      "../src/sublime"
    )
  )
)

from Window import Window

class TestWindow(unittest.TestCase):
  def test_if_nothing_is_set_get_status_should_yield_an_empty_string(self):
    self.__assert(expected = "")

  def test_if_something_is_set_get_status_should_yield_something(self):
    self.__assert(expected = "something")

  def __assert(self, expected):
    self.__window.subscribe(self.__view)
    self.__window.set_status_bar_message(expected)

    self.assertEqual(self.__actual(), expected)

    self.__window.unsubscribe(self.__view)

    # no view subscriptions
    self.__window.set_status_bar_message("something else")

    # so it should still be "something" and not "something else"
    self.assertEqual(self.__actual(), expected)

  def __actual(self):
    return self.__view.get_status(self.__test_key)

  def setUp(self):
    self.__test_key = "testKey"
    self.__view = sublime.active_window().new_file()

    settings = sublime.load_settings("Preferences.sublime-settings")
    settings.set("close_windows_when_empty", False)

    self.__window = Window(self.__test_key)

  def tearDown(self):
    self.__window.set_status_bar_message("")

    if self.__view:
      self.__view.set_scratch(True)
      self.__view.window().focus_view(self.__view)
      self.__view.window().run_command("close_file")
