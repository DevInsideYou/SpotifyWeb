import sys

import unittest

SpotifyModule = sys.modules["SpotifyWeb.src.spotify.Spotify"]

Spotify = SpotifyModule.Spotify

class TestSpotify(unittest.TestCase):
  def test_if_token_is_cached_side_effect_current_track_name(self):
    class FakeClient:
      def get_cached_token(self):
        return "some fake token"

      def currently_playing_track_name(self, token):
        return "some track name"

    client = FakeClient()

    actual = ""

    def side_effect(message):
      nonlocal actual
      actual = message

    spotify = Spotify(side_effect)

    spotify.run_once(client, send_oauth2_request = None, get_redirect_response = None)
    self.assertEqual(actual, "some track name")

  def test_if_token_is_not_cached_call_the_get_redirect_response_function(self):
    class FakeClient:
      def __init__(self, redirect_port):
        self.redirect_port = redirect_port

      def get_oauth2_url(self):
        return "some url"

      def get_cached_token(self):
        return None

      def get_fresh_token(self, spotify_response_code):
        return "some fake token"

      def currently_playing_track_name(self, token):
        return "some track name"

    client = FakeClient(redirect_port = 1337)

    actual = ""

    def side_effect(message):
      nonlocal actual
      actual = message

    spotify = Spotify(side_effect)

    def send_oauth2_request(oauth2_url):
      self.assertEqual(oauth2_url, "some url")

    def get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds):
      self.assertEqual(oauth2_url, "some url")
      self.assertEqual(redirect_port, 1337)
      self.assertEqual(available_duration_for_login_in_seconds, 60)

      handle("some response")

    spotify.run_once(client, send_oauth2_request, get_redirect_response)
    self.assertEqual(actual, "some track name")

  def test_if_currently_playing_track_name_raises_an_exception_the_message_should_be_delegated_to_the_side_effect_function(self):
    class FakeClient:
      def get_cached_token(self):
        return "some fake token"

      def currently_playing_track_name(self, token):
        raise Exception("exception message")

    client = FakeClient()

    actual = ""

    def side_effect(message):
      nonlocal actual
      actual = message

    spotify = Spotify(side_effect)

    spotify.run_once(client, send_oauth2_request = None, get_redirect_response = None)
    self.assertEqual(actual, "exception message")
