import lyricsgenius.song
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius

# USE YOUR OWN APOTIFY API CREDENTIALS HERE
cid ='spotify_client_id_credentials'  # client id
secret ='spotify_clieant_secret_credentials'  # client secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# USE YOUR OWN GENIUS API CREDENTIALS HERE
genius = lyricsgenius.Genius('genius_credentials')

top_usa = sp.playlist('spotify:playlist:37i9dQZEVXbLp5XoPON0wI')

def rid_feature(song):
    song_wo_feature = song
    if '(' in song:
        song_wo_feature = ''
        for i in song: 
            if i == '(':
                break
            song_wo_feature += i
    return song_wo_feature.replace('?','').replace('!','').replace('\'','').replace(',','')


# GET SONGS AND THEIR ARTISTS, ADD TO LISTS
track_names = []
artist_names = []
i = 0
for track in (top_usa.get('tracks').get('items')):
    track_names.append(rid_feature(top_usa.get('tracks').get('items')[i].get('track').get('name')))
    artist_names.append(top_usa.get('tracks').get('items')[i].get('track').get('artists')[0].get('name'))  # note this only gets the first artist listed
    i = i+1


# WRITE TO TXT DOC
f = open("test.txt","w", encoding="utf-8")

i = 0
for i, val in enumerate(track_names):
    f.write(top_usa.get('tracks').get('items')[i].get('track').get('name'))
    f.write(' by ')
    f.write(top_usa.get('tracks').get('items')[i].get('track').get('artists')[0].get('name'))
    f.write('\nLYRICSSTART\n')
    song = genius.search_song(track_names[i], artist_names[i])
    f.write(song.lyrics)
    f.write('\nLYRICSEND\n\n\n\n\n')

f.close()
