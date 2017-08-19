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
      cache_path = os.path.join(
        os.path.dirname(__file__),
        "../../.cached-token"
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

  def currently_playing_track_name(self, token):
    def currently_playing_track_name(track):
      if track["is_playing"]:
        return track["item"]["name"]
      else:
        return ""

    return currently_playing_track_name(
      track = self.__get_current_track(token)
    )

  def __get_current_track(self, token):
    return self.__get(token, "https://api.spotify.com/v1/me/player/currently-playing")

  def __get(self, token, url):
    return SpotipyClient.Spotify(auth = token)._get(url)
