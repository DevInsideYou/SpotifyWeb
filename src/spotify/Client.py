import logging
import os
import sys

from ...lib.spotipy import client as SpotipyClient
from ...lib.spotipy import oauth2 as SpotipyOauth2

class Client:
  def __init__(self, client_id, client_secret, redirect_port):
    logging.getLogger("requests").setLevel(logging.WARNING)

    self.redirect_port = redirect_port

    self.__oauth2 = SpotipyOauth2.SpotifyOAuth(
      client_id,
      client_secret,
      redirect_uri = "http://localhost:" + str(redirect_port),
      scope = "user-read-currently-playing",
      cache_path = os.path.abspath(
        os.path.join(
          os.path.dirname(__file__),
          "../../../.spotifyweb-cached-token"
        )
      )
    )

  def get_oauth2_url(self):
    return self.__oauth2.get_authorize_url()

  def get_cached_token(self):
    return self.__extracted_token(
      self.__oauth2.get_cached_token()
    )

  def get_fresh_token(self, spotify_redirect_response):
    return self.__extracted_token(
      self.__oauth2.get_access_token(
        self.__oauth2.parse_response_code(spotify_redirect_response)
      )
    )

  def __extracted_token(self, token_response):
    if token_response:
      return token_response["access_token"]
    else:
      None

  def currently_playing_track(self, token, settings_manager):
    def render_title_and_artist_or_show(title, artist_or_show_name):
      if settings_manager.should_display_title_before_artist():
        return title + " - " + artist_or_show_name
      else:
        return artist_or_show_name + " - " + title

    def render_artists(artists):
      number_of_artists = len(artists)

      if number_of_artists == 1:
        return artists[0]["name"]
      elif not settings_manager.should_display_every_artist_name():
        return "Various Artists"
      else:
        artist_name = ""

        for index, artist in enumerate(artists):
          artist_name += artist["name"]

          if number_of_artists == (index + 1):
            continue
          else:
            artist_name += ", "

        return artist_name

    def render_item(item):
      if item is None:
        return ""
      else:
        title = item["name"]

        if item["type"] == "episode":
          return render_title_and_artist_or_show(title, item["show"]["name"])
        else:
          return render_title_and_artist_or_show(title, render_artists(item["artists"]))

    def currently_playing_track(track):
      if track is None:
        return ""
      elif track["is_playing"]:
        return render_item(track["item"])
      else:
        return ""

    return currently_playing_track(
      track = self.__get_current_track(token)
    )

  def __get_current_track(self, token):
    return self.__get(
      token,
      "https://api.spotify.com/v1/me/player/currently-playing",
      {
        "additional_types": "episode,track"
      }
    )

  def __get(self, token, url, args=None):
    return SpotipyClient.Spotify(auth = token)._get(url, args)
