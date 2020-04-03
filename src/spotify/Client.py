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
          "../../../.SpotifyWeb-Cached-Token"
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

  def currently_playing_track_name(self, token, settings_manager):
    def currently_playing_track_name(track, settings_manager):
      if track is None:
        return ""
      elif track["is_playing"]:
          if track["item"] is not None:
            item = track["item"]
            if item['type'] == 'episode':
              return self.__returnResponse(item["name"], item['show']['name'], settings_manager)
            else:
              artistName = ""
              if len(item["artists"]) == 1:
                artistName += item["artists"][0]["name"]
              elif settings_manager.show_every_artist_name_instead_of_various_artists():
                for index, artists in enumerate(item["artists"]):
                  artistName += artists["name"] 
                  if len(item["artists"]) == (index + 1):
                    continue
                  else:
                    artistName += ' - '
              else:
                artistName = 'Various Artists'

          return self.__returnResponse(item["name"], artistName, settings_manager)

    return currently_playing_track_name(
      track = self.__get_current_track(token),
      settings_manager = settings_manager
    )

  def __get_current_track(self, token):
    return self.__get(token, "https://api.spotify.com/v1/me/player/currently-playing", {'additional_types': 'episode,track'})

  def __get(self, token, url, args=None):
    return SpotipyClient.Spotify(auth = token)._get(url, args)

  def __returnResponse(self, trackParam, artistParam, settings_manager):
    if settings_manager.music_name_comes_before_artist_name():
      return trackParam + ' - ' + artistParam
    else:
      return artistParam + ' - ' + trackParam
    