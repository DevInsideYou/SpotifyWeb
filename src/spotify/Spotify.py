class Spotify:
  def __init__(self, side_effect):
    self.__side_effect = side_effect

  def run_once(self, client, send_oauth2_request, get_redirect_response):
    def run_once():
      def side_effect_current_track_name_using_cached_token():
        side_effect_current_track_name(
          token = client.get_cached_token(),
          fallback = authenticate_to_get_fresh_token
        )

      def side_effect_current_track_name(token, fallback):
        if(token):
          try_side_effect_current_track_name(token)
        else:
          fallback()

      def try_side_effect_current_track_name(valid_token):
        try:
          self.__side_effect(client.currently_playing_track_name(valid_token))
        except Exception as e:
          self.__side_effect(e)

      def authenticate_to_get_fresh_token():
        get_redirect_response(
          send_oauth2_request = send_oauth2_request,
          oauth2_url = client.get_oauth2_url(),
          redirect_port = client.redirect_port,
          handle = side_effect_current_track_name_using_fresh_token,
          available_duration_for_login_in_seconds = 60
        )

      def side_effect_current_track_name_using_fresh_token(spotify_redirect_response):
        try:
          side_effect_current_track_name(
            token = client.get_fresh_token(spotify_redirect_response),
            fallback = side_effect_error
          )
        except:
          side_effect_error()

      def side_effect_error():
        self.__side_effect(
          "Couldn't get authorization token from Spotify. "
          "Another tab should have opened in your browser for you to try to login again. "
          "Please restart Sublime if the tab did not open."
        )

      side_effect_current_track_name_using_cached_token()

    run_once()
