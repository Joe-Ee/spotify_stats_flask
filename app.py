
#so this will be like my lasts spotify app but there will be flask and versin control and CD/CI
#when you upload it to vs code with a new branch it will automatically run tests to make sure things work
#there will be a database where a user can press the current song and then say "Yo this is good or not and it saves it for them"
#yeah just try to make it like it would be in software engineering.
#------------------------------------------------------------------------------------------------------------------------------------------                            _       
 #(_)                          | |      
 # _ _ __ ___  _ __   ___  _ __| |_ ___ 
 #| | '_ ` _ \| '_ \ / _ \| '__| __/ __|
 #| | | | | | | |_) | (_) | |  | |_\__ \
 #|_|_| |_| |_| .__/ \___/|_|   \__|___/
 #           | |                       
 #           |_|     
from flask import Flask, abort, redirect, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from urllib.request import urlopen
import spotipy.util as util
import random
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
#                                          __ _                       _   _             
#     /\                                  / _(_)                     | | (_)            
#    /  \   _ __  _ __     ___ ___  _ __ | |_ _  __ _ _   _ _ __ __ _| |_ _  ___  _ __  
#   / /\ \ | '_ \| '_ \   / __/ _ \| '_ \|  _| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \ 
#  / ____ \| |_) | |_) | | (_| (_) | | | | | | | (_| | |_| | | | (_| | |_| | (_) | | | |
# /_/    \_\ .__/| .__/   \___\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|
#          | |   | |                             __/ |                                  (keys and things)
#          |_|   |_|                            |___/                                   

SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET'] 
SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI'] 

SPOTIPY_CLIENT_ID = SpotifyClientCredentials(client_id= SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager = SPOTIPY_CLIENT_ID)
auth_manager = SpotifyClientCredentials()
scope = "user-library-read"

#----------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)

@app.get('/')
def index():

    scope = 'user-read-currently-playing'#deals with user premissions, reads the currently playing song information
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    #set default values
    layout = "Nothing is playing"
    imLink = ""
    #dictionary about currently playing song
    music = sp.current_user_playing_track()

    #if the dictionary is None then there is no song playinga nd just put int eh defaults. 
    if music != None:
            #image link from dictionary
        imLink = music["item"]["album"]["images"][0]["url"]

            #get the songname and artist name and format it
        songName = music["item"]["name"]
        artistName = music["item"]["artists"][0]["name"]
        layout = songName + " by " + artistName
    
    
#get to0tal time left in a song. Not used because if a song is skipped the timer is still going for the last song so it doesn't really work
        progress = music['progress_ms']
        total = music['item']['duration_ms']
        timeLeft = (total - progress)/1000

    print(music['progress_ms'])
    print(music['item']['duration_ms'])
    return render_template('playing.html', photo = imLink, info = layout, secs = 30)

def topAllTime(length, page):
#try to replace this with the type of thing you did for the top one.
    bop = ""
    results = sp.current_user_top_tracks(time_range = length, limit = 50)
    while results:
        for idx, val in enumerate(results['items']):
            
            iterableThing = val['album']
            print(iterableThing)
            bop = bop+  "                "+ val['artists'][0]['name']+ " – "+ val['name'] + "\n"
        if results['next']:#if there is a next then keep going
            results = sp.next(results)
        else:#if not then stop
            results = None
    
    print(bop)


@app.get("/MostPlayedSongs")
def mostPlayedSongs():
    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))    

    length = "short_term" #short_term, medium_term, long_term
    songs = sp.current_user_top_tracks(time_range = length, limit = 50)
    #base for 1 thing. You need to either put all values in array and then pass in or do something else. This is how you access stuff though. 
    ranges =   [ sp.current_user_top_tracks(time_range = "short_term", limit = 50), sp.current_user_top_tracks(time_range = "medium_term", limit = 50), sp.current_user_top_tracks(time_range = "long_term", limit = 50)]
    print(ranges[1]['items'][0]['album']['images'][2]['url'])


    return render_template("MostPlayedSong.html", songs = ranges)
    
@app.get("/MostPlayedArtists")
def mostPlayedArtist():
    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    ranges =   [ sp.current_user_top_artists(time_range = "short_term", limit = 50), sp.current_user_top_artists(time_range = "medium_term", limit = 50), sp.current_user_top_artists(time_range = "long_term", limit = 50)]
    print(ranges[0]['items'][0]['name'])
    print(ranges[0]['items'][0]['images'][2]['url'])
    print(ranges[0]['items'][0]['popularity'])
    return render_template("MostPlayedartist.html", artists = ranges)

if __name__ == '__main__':
    app.run()


@app.get("/SavedSongs")
def savedSongs():
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))    

    songsOrTracks = sp.current_user_saved_tracks(limit = 50)

    print(songsOrTracks['items'][0]['track']['external_urls']['spotify'])
    return render_template("SavedSongs.html", songs = songsOrTracks['items'])

@app.get("/SavedAlbums")
def savedAlbum():
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    albums = sp.current_user_saved_albums(limit = 50)


    return render_template("SavedAlbums.html", albums = albums, sp = sp)