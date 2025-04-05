import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Your Spotify App credentials
CLIENT_ID = "7e96667b625548f88b3ae7ea6fb13481"
CLIENT_SECRET = "55583bca92a842b9b9bb79200a1f9f04"
REDIRECT_URI = "http://localhost:8080"
SCOPE = "user-read-playback-state user-modify-playback-state"

# Custom auth manager that gives you the URL
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=False  # prevents trying to launch a browser
)

# Get the authorization URL and print it
auth_url = auth_manager.get_authorize_url()
print("\n🔗 Open this URL in a browser to authorize:")
print(auth_url)

# Wait for user to complete the login in a real browser
print("\n🕒 Waiting for authorization...")
token_info = auth_manager.get_access_token(as_dict=False)

# Now use the token
sp = spotipy.Spotify(auth=token_info)
me = sp.me()
print(f"\n✅ Authenticated as: {me['display_name']}")
