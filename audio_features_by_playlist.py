import lyricsgenius.song
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius

# USE YOUR OWN SPOFITY API CREDENTIALS HERE
cid ='2c0b10097189464099a83b04369468da'  # client id
secret ='4da7dce8af804fc791c294051f3948e3'  # client secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# USE YOUR OWN GENIUS API CREDENTIALS HERE
genius = lyricsgenius.Genius('XnSTkisZQcNClsYoKSfP9olERtqBU8-1_5ZyVS_3lmIFZXjJWZcdxdM6-pHEeVGn')

top_usa = sp.playlist('spotify:playlist:37i9dQZEVXbLp5XoPON0wI')  # test playlist
bourgeoisieses = sp.track('spotify:track:056bKm6W5j9QodOftRznUV')  # test track

def rid_feature(song):
    song_wo_feature = song
    if '(' in song:
        song_wo_feature = ''
        for i in song: 
            if i == '(':
                break
            song_wo_feature += i
    return song_wo_feature.replace('?','').replace('!','').replace('\'','').replace(',','')

def audio_features_str(track_uri):
    final_string = ''
    final_string += 'DANCEABILITY = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('danceability'))
    final_string += '\nENERGY = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('energy'))
    final_string += '\nLOUDNESS = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('loudness'))
    final_string += '\nSPEECHINESS = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('speechiness'))
    final_string += '\nACOUSTICNESS = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('acousticness'))
    final_string += '\nLIVENESS = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('liveness'))
    return final_string


# GET SONG NAMES, ARTISTS, URI -> ADD TO LISTS
track_names = []
artist_names = []
track_uris = []
i = 0
for track in (top_usa.get('tracks').get('items')):
    track_names.append(rid_feature(top_usa.get('tracks').get('items')[i].get('track').get('name')))
    artist_names.append(top_usa.get('tracks').get('items')[i].get('track').get('artists')[0].get('name'))  # note this only gets the first artist listed
    track_uris.append(top_usa.get('tracks').get('items')[i].get('track').get('uri'))
    i = i+1

# WRITE TO TXT DOC
f = open("test2.txt","w", encoding="utf-8")

i = 0
for i, val in enumerate(track_names):
    f.write(top_usa.get('tracks').get('items')[i].get('track').get('name'))
    f.write(' by ')
    f.write(artist_names[i])
    f.write('\nAUDIO FEATURES\n')
    f.write(audio_features_str(track_uris[i]))
    f.write('\nDONE\n\n\n\n')

f.close()

