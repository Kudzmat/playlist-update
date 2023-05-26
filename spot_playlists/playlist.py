from datetime import date
from forms import PlaylistForm
from app import app
from flask import render_template, url_for, redirect, session
from dotenv import load_dotenv
import os
import spotipy

from spotipy.oauth2 import SpotifyOAuth

load_dotenv()  # load the environment variables

# storing environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_USER_ID = os.getenv('SPOTIFY_USER_ID')

# scope for authorization
SCOPE = "user-library-read user-top-read playlist-modify-public user-follow-read user-library-read " \
        "playlist-read-private playlist-modify-private "


# home page route for filling form
@app.route('/', methods=["GET", "POST"])
def try_playlist():
    form = PlaylistForm()  # instantiating a new form
    artist_list = []  # this empty list will hold all the artists entered

    if form.validate_on_submit():
        # getting the entered artists and appending them to the list
        artist1 = form.artist1.data
        artist_list.append(artist1)

        artist2 = form.artist2.data
        artist_list.append(artist2)

        artist3 = form.artist3.data
        artist_list.append(artist3)

        artist4 = form.artist4.data
        artist_list.append(artist4)

        artist5 = form.artist5.data
        artist_list.append(artist5)

        session['artist_list'] = artist_list  # saving artist list to use for next route

        return redirect(url_for('playlist'))  # redirect to playlist route

    return render_template('index.html', form=form)


# route which will take you to playlist page
@app.route('/playlist', methods=["GET", "POST"])
def playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                                   username=SPOTIFY_USER_ID, redirect_uri=SPOTIFY_REDIRECT_URI))

    # getting my playlist
    playlist_id = '138EKhzuYuww8DKcRC69ox'

    # getting today's date
    current_date = (date.today()).strftime('%m-%d-%Y')

    # saving playlist name with today's date
    playlist_name = f'Vibe Check -> {current_date}'

    artists_ids = []  # spotify's recommended artist IDs will be added to this list
    tracks = []  # the recommended tracks will be added to this list
    artist_list = session['artist_list']  # calling the artist list from the previous route
    print(artist_list)

    # not necessary, but checking to see we get the right playlist
    playlists = sp.user_playlists(user=SPOTIFY_USER_ID)  # all playlists
    for item in playlists['items']:
        print(item['name'])
        print(item['id'])

    # putting artist ids in a list
    for artist in artist_list:
        name_result = sp.search(artist, limit=1, type='artist', market='US')
        artist_info = name_result['artists']['items'][0]  # get artist ID
        artist_id = artist_info['id']
        artists_ids.append(artist_id)

    # getting 5 song recommendation and appending them to the tracks list
    result = sp.recommendations(seed_artists=artists_ids, limit=5, country='US')
    for item in result['tracks']:
        tracks.append(item['uri'])  # track['uri']

    sp.playlist_add_items(playlist_id=playlist_id, items=[song for song in tracks])  # adding songs
    sp.playlist_change_details(name=playlist_name, playlist_id=playlist_id)  # updating the playlist name with last updated date

    return redirect('https://open.spotify.com/playlist/138EKhzuYuww8DKcRC69ox')  # takes you to playlist page

