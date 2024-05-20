import lyricsgenius.song
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius

# USE YOUR OWN APOTIFY API CREDENTIALS HERE
cid ='xxx'  # client id
secret ='xxx'  # client secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# USE YOUR OWN GENIUS API CREDENTIALS HERE
genius = lyricsgenius.Genius('xxx')

top_usa = sp.playlist('spotify:playlist:37i9dQZEVXbLp5XoPON0wI')  # test playlist
# top_usa = sp.playlist('spotify:playlist:49G54i94nAqUUsa57pHG4f')  # music mix

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
    final_string += '\nSPEECHINESS = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('speechiness'))
    final_string += '\nVALENCE = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('valence'))
    final_string += '\nPOPULARITY = ' + str((sp.audio_features(tracks=[track_uri]))[0].get('popularity'))
    return final_string

track_names = []
artist_names = []
track_uris = []
i = 0
for track in (top_usa.get('tracks').get('items')):
    track_names.append(rid_feature(top_usa.get('tracks').get('items')[i].get('track').get('name')))
    artist_names.append(top_usa.get('tracks').get('items')[i].get('track').get('artists')[0].get('name'))  # note this only gets the first artist listed
    track_uris.append(top_usa.get('tracks').get('items')[i].get('track').get('uri'))
    i = i+1

f_positive = open("positive_lyrics.txt","w", encoding="utf-8")
f_neutral = open("neutral_lyrics.txt","w", encoding="utf-8")
f_negative = open("negative_lyrics.txt","w", encoding="utf-8")

for i, uri in enumerate(track_uris):
    if (sp.audio_features(tracks=[uri]))[0].get('valence') > 0.66:
        f_positive.write(track_names[i] + ' by ' + artist_names[i])
        f_positive.write('\nLYRICSSTART\n')
        song = genius.search_song(track_names[i], artist_names[i])
        if not (song == None):
            f_positive.write(song.lyrics)
        f_positive.write('\nLYRICSEND\n\n\n\n\n')

    elif (sp.audio_features(tracks=[uri]))[0].get('valence') < 0.33:
        f_negative.write(track_names[i] + ' by ' + artist_names[i])
        f_negative.write('\nLYRICSSTART\n')
        song = genius.search_song(track_names[i], artist_names[i])
        if not (song == None):
            f_negative.write(song.lyrics)
        f_negative.write('\nLYRICSEND\n\n\n\n\n')
    
    else: 
        f_neutral.write(track_names[i] + ' by ' + artist_names[i])
        f_neutral.write('\nLYRICSSTART\n')
        song = genius.search_song(track_names[i], artist_names[i])
        if not (song == None):
            f_neutral.write(song.lyrics)
        f_neutral.write('\nLYRICSEND\n\n\n\n\n')

f_positive.close()
f_neutral.close()
f_negative.close()