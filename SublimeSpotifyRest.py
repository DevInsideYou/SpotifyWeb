import sublime
import sublime_plugin

from .src.spotify.SettingsManager import SettingsManager
from .src.spotify.Spotify import Spotify

from .src.sublime.SettingsManager import SettingsManager as SublimeSettingsManager

sublime_settings_manager = SublimeSettingsManager("SublimeSpotifyRest.sublime-settings")

settings_manager = SettingsManager(
  reader_writer = sublime_settings_manager
)

def plugin_loaded():
  sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

  def run_main_loop():
    Spotify(
      side_effect = print
    ).run_main_loop(settings_manager)

  run_main_loop()

class Sublime_spotify_toggleCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    settings_manager.toggle()

    if settings_manager.is_enabled():
      sublime_settings_manager.display_message("Spotify enabled. Play a song and it will be shown here.")
    else:
      sublime_settings_manager.display_message("Spotify disabled.")

class Sublime_spotify_rest_settingsCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    sublime_settings_manager.open_settings_window()
