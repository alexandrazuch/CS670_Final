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

# top_usa = sp.playlist('spotify:playlist:37i9dQZEVXbLp5XoPON0wI')  # test playlist
top_usa = sp.playlist('spotify:playlist:49G54i94nAqUUsa57pHG4f')  # music mix

def rid_feature(song):
    song_wo_feature = song
    if '(' in song:
        song_wo_feature = ''
        for i in song: 
            if i == '(':
                break
            song_wo_feature += i
    return song_wo_feature.replace('?','').replace('!','').replace('\'','').replace(',','')

track_names = []
artist_names = []
track_uris = []
track_popularity = []
i = 0
for track in (top_usa.get('tracks').get('items')):
    track_names.append(rid_feature(top_usa.get('tracks').get('items')[i].get('track').get('name')))
    artist_names.append(top_usa.get('tracks').get('items')[i].get('track').get('artists')[0].get('name'))  # note this only gets the first artist listed
    track_uris.append(top_usa.get('tracks').get('items')[i].get('track').get('uri'))
    track_popularity.append(top_usa.get('tracks').get('items')[i].get('track').get('popularity'))
    i = i+1

pos_tot = 0
pos_num = 0
neu_tot = 0
neu_num = 0
neg_tot = 0
neg_num = 0

for i, uri in enumerate(track_uris):
    if (sp.audio_features(tracks=[uri]))[0].get('speechiness') > 0.66:
        pos_num += 1
        pos_tot += (sp.audio_features(tracks=[uri]))[0].get('speechiness')
    elif (sp.audio_features(tracks=[uri]))[0].get('speechiness') < 0.33:
        neg_num += 1
        neg_tot += (sp.audio_features(tracks=[uri]))[0].get('speechiness')
    else: 
        neu_num += 1
        neu_tot += (sp.audio_features(tracks=[uri]))[0].get('speechiness')

# print("POSITIVE AVERAGE: ", pos_tot/pos_num)
# print("NEUTRAL AVERAGE: ", neu_tot/neu_num)
# print("NEGATIVE AVERAGE: ", neg_tot/neg_num)

# tot_pop = 0
# num_pop = 0
# for i2, pop in enumerate(track_popularity):
#     num_pop += 1
#     tot_pop += pop

# print("AVERAGE POPULARITY: ", (tot_pop/num_pop))


tot_pos_pop = 0
pos_pop = 0
tot_neu_pop = 0
neu_pop = 0
tot_neg_pop = 0
neg_pop = 0
for i2, pop in enumerate(track_popularity):
    if (sp.audio_features(tracks=[track_uris[i2]]))[0].get('speechiness') > 0.66:
        pos_pop += 1
        tot_pos_pop += pop
    elif (sp.audio_features(tracks=[track_uris[i2]]))[0].get('speechiness') < 0.33:
        neg_pop += 1
        tot_neg_pop += pop
    else: 
        neu_pop += 1
        tot_neu_pop += pop

# print(track_popularity)

if neg_pop > 0:
    print("NEGATIVE AVERAGE POPULARITY: ", tot_neg_pop/neg_pop)
if neu_pop > 0:
    print("NEUTRAL AVERAGE POPULARITY: ", tot_neu_pop/neu_pop)
if pos_pop > 0:
    print("POSITIVE AVERAGE POPULARITY: ", tot_pos_pop/pos_pop)
