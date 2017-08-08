from threading import Timer
import os
import sys
import urllib.request

import unittest

sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(__file__),
      "../src/spotify"
    )
  )
)

from Server import Server

class TestServer(unittest.TestCase):
  def test_roundtrip(self):
    oauth2_url = "some url"
    redirect_port = 1337

    def send_http_request_to_self():
      urllib.request.urlopen("http://localhost:{}/".format(str(redirect_port))).read()

    def send_oauth2_request(url):
      self.assertEqual(url, oauth2_url)

      Timer(2, send_http_request_to_self).start()

    def handle(redirect_response):
      self.asserEqual(redirect_response, "http://localhost:1337")

    Server.get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds = 5)

  def test_circuit_breaker(self):
    oauth2_url = "some url"
    redirect_port = 1337

    def send_oauth2_request(url):
      self.assertEqual(url, oauth2_url)
      # don't do anything

    def handle(redirect_response):
      self.asserEqual(redirect_response, "http://localhost:1337")

    Server.get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds = 2)
