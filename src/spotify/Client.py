class Client:
  def __init__(self, client_id, client_secret, redirect_port):
    self.redirect_port = redirect_port

  def get_oauth2_url(self):
    return None

  def get_cached_token(self):
    return None

  def get_fresh_token(self, spotify_redirect_response):
    return None

  def currently_playing_track_name(self, token):
    return None
