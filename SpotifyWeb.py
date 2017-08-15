import sublime
import sublime_plugin

from .src.spotify.SettingsManager import SettingsManager
from .src.spotify.Spotify import Spotify

from .src.sublime.SettingsManager import SettingsManager as SublimeSettingsManager
from .src.sublime.Window import Window

window = Window(
  status_bar_key = "SpotifyWeb"
)

sublime_settings_manager = SublimeSettingsManager(
  settings_file_name = "SpotifyWeb.sublime-settings"
)

settings_manager = SettingsManager(
  reader_writer = sublime_settings_manager
)

def plugin_loaded():
  window.set_status_bar_message("")

  window.subscribe(sublime.active_window().active_view())

  open_settings_window_if_credentials_are_not_set()

  def run_main_loop():
    Spotify(
      side_effect = window.set_status_bar_message
    ).run_main_loop(settings_manager)

  '''
    When sublime starts up and the plugin is enabled,
    the server should start on a different thread,
    so that sublime doesn't hang until the circuit breaker kicks in
  '''
  sublime.set_timeout_async(run_main_loop, 5000)

def open_settings_window_if_credentials_are_not_set():
  if settings_manager.are_credentials_at_least_partially_empty_or_none():
    sublime_settings_manager.open_settings_window()

class SpotifyWeb(sublime_plugin.EventListener):
  def on_activated(self, view):
    window.subscribe(view)

  def on_close(self, view):
    window.unsubscribe(view)

class Spotify_web_toggleCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    settings_manager.toggle()

    if settings_manager.is_enabled():
      sublime_settings_manager.display_message("SpotifyWeb enabled. Play a song and it will be shown here.")
    else:
      sublime_settings_manager.display_message("SpotifyWeb disabled.")

class Spotify_web_settingsCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    sublime_settings_manager.open_settings_window()
