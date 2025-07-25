import spotipy
from spotipy.oauth2 import SpotifyOAuth




# Scope required to read liked songs and modify playlists
SCOPE = 'user-library-read playlist-modify-private playlist-modify-public'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Get current user's ID
user_id = sp.me()['id']

# Name of the playlist to create/update
playlist_name = 'Recent 40 Liked Songs'

# Function to get or create the playlist
def get_or_create_playlist(sp, user_id, playlist_name):
    # Get user's playlists
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']
    
    # Create a new playlist if it doesn't exist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    return playlist['id']

# Function to get the most recent 40 liked songs
def get_recent_liked_songs(sp, limit=40):
    results = sp.current_user_saved_tracks(limit=limit)
    track_ids = [item['track']['id'] for item in results['items']]
    return track_ids

# Main logic
if __name__ == '__main__':
    # Get or create the playlist
    playlist_id = get_or_create_playlist(sp, user_id, playlist_name)
    
    # Get the most recent 40 liked songs
    recent_liked_songs = get_recent_liked_songs(sp, limit=40)
    
    # Clear the existing playlist
    sp.playlist_replace_items(playlist_id, recent_liked_songs)

    print(f'Updated playlist "{playlist_name}" with the most recent 40 liked songs.')