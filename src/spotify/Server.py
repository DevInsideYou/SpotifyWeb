from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Timer
import os
import urllib.request

class Server:
  @staticmethod
  def get_redirect_response(send_oauth2_request, oauth2_url, redirect_port, handle, available_duration_for_login_in_seconds):
    def get_redirect_response():
      server = start_up_server(SpotifyRedirectURIHandler())
      send_oauth2_request(oauth2_url)
      block_thread_until_spotify_responds(server)
      shut_down_server(server)

    def start_up_server(handler):
      return HTTPServer(('', redirect_port), handler)

    def SpotifyRedirectURIHandler():
      class SpotifyRedirectURIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()

          handle(self.path)

          html = open(self.__html_location(), "r").read()

          self.wfile.write(bytes(html, "utf8"))

          return

        def __html_location(self):
          return os.path.abspath(
              os.path.join(
                os.path.dirname(__file__),
                "../../resources/index.html"
              )
            )

      return SpotifyRedirectURIHandler

    def block_thread_until_spotify_responds(server):
      circuit_breaker = Timer(available_duration_for_login_in_seconds, send_http_request_to_self)
      circuit_breaker.start()
      server.handle_request() # blocking happens here
      circuit_breaker.cancel()

    def send_http_request_to_self():
      try:
        urllib.request.urlopen("http://localhost:{}/".format(str(redirect_port))).read()
      except:
        pass

    def shut_down_server(server):
      server.socket.close()

    get_redirect_response()
