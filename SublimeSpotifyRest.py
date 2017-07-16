import sublime
import sublime_plugin

from .src.sublime.SettingsManager import SettingsManager as SublimeSettingsManager

sublime_settings_manager = SublimeSettingsManager("SublimeSpotifyRest.sublime-settings")

def plugin_loaded():
  sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

class Sublime_spotify_rest_settingsCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    sublime_settings_manager.open_settings_window()
