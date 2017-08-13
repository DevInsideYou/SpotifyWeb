import sublime

class SettingsManager:
  def __init__(self, settings_file_name):
    self.__settings_file_name = settings_file_name

  def read_setting(self, key):
    return self.__load_settings().get(key)

  def set_setting(self, key, value):
    self.__load_settings().set(key, value)

  def write_setting(self, key, value):
    self.set_setting(key, value)
    self.__save_settings()

  def __load_settings(self):
    return sublime.load_settings(self.__settings_file_name)

  def __save_settings(self):
    sublime.save_settings(self.__settings_file_name)

  def open_settings_window(self):
    sublime.run_command("new_window")

    settings_window = sublime.active_window()

    left_right_group = {
      "cols": [0.0, 0.5, 1.0],
      "rows": [0.0, 1.0],
      "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
    }

    settings_window.set_layout(left_right_group) # the left group is focused by default

    packages = settings_window.extract_variables()["packages"]

    settings_window.open_file("{}/SpotifyWeb/{}".format(packages, self.__settings_file_name))

    settings_window.focus_group(1) # focus the right group

    settings_window.open_file("{}/User/{}".format(packages, self.__settings_file_name))

  def display_message(self, message):
    sublime.active_window().status_message(message)
