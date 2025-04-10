#!/usr/bin/env python3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import http.server
import socketserver
import urllib.parse

#CLIENT CREDENTIALS
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "user-read-playback-state,user-modify-playback-state"

#Authentication
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope=SCOPE)

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Check URL 'code' parameter
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in query_components:
            code = query_components["code"][0]
            print(f"Authorization code received: {code}")
            try:
                token_info = sp_oauth.get_access_token(code, as_dict=True)
                access_token = token_info["access_token"]
                print(f"Access Token: {access_token}")
                # Respond to browser
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authorization successful! You can now close this window.")
            except Exception as e:
                print(f"Error obtaining token: {e}")
                self.send_error(400, f"Error obtaining token: {e}")
        else:
            self.send_error(400, "No authorization code found in the URL.")

def run_server():
    handler = OAuthHandler
    with socketserver.TCPServer(("localhost", 8080), handler) as httpd:
        print("Serving at port 8080...")
        httpd.handle_request()  # handle requesr then exit

def main():
    auth_url = sp_oauth.get_authorize_url()
    print("Please navigate to this URL to authenticate:")
    print(auth_url)
    run_server()

if __name__ == "__main__":
    main()
