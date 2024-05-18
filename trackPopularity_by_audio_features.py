import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import pandas as pd

# USE YOUR OWN SPOTIFY API CREDENTIALS HERE
cid = 'b54a724d7918433a9d08dbf949efa8b5'  # client id
secret = '24bfc5c1076a4f41b915e892193f2003'  # client secret

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# USE YOUR OWN GENIUS API CREDENTIALS HERE
genius = lyricsgenius.Genius("KZElVnrSm_yoMEinuiMULRoBG6JOF6fAxpQvYz7KXmFJaffQPCRGpTwnzCX9Y")

top_usa = sp.playlist('spotify:playlist:37i9dQZEVXbLp5XoPON0wI')  # test playlist

def rid_feature(song):
    song_wo_feature = song
    if '(' in song:
        song_wo_feature = ''
        for char in song:
            if char == '(':
                break
            song_wo_feature += char
    return song_wo_feature.replace('?', '').replace('!', '').replace('\'', '').replace(',', '')

def audio_features_str(track_uri):
    attempts = 0
    while attempts < 3:  # Retry up to 3 times
        try:
            features = sp.audio_features(tracks=[track_uri])[0]
            danceability = features.get('danceability')
            speechiness = features.get('speechiness')
            valence = features.get('valence')
            
            # Fetch track details to get popularity
            track_details = sp.track(track_uri)
            popularity = track_details.get('popularity')

            final_string = f"""
            DANCEABILITY = {danceability}
            SPEECHINESS = {speechiness}
            VALENCE = {valence}
            POPULARITY = {popularity}
            """
            return final_string, danceability, speechiness, valence, popularity
        except spotipy.client.SpotifyException as e:
            if e.http_status == 429:  # Too Many Requests
                time.sleep(2 ** attempts)  # Exponential backoff
                attempts += 1
            else:
                raise  # Reraise other exceptions

    raise Exception("Max retries exceeded. Failed to fetch audio features.")

# GET SONG NAMES, ARTISTS, URI -> ADD TO LISTS
track_names = []
artist_names = []
track_uris = []

for item in top_usa['tracks']['items']:
    track = item['track']
    track_names.append(rid_feature(track['name']))
    artist_names.append(track['artists'][0]['name'])  # note this only gets the first artist listed
    track_uris.append(track['uri'])

# Initialize lists to store feature values and popularity
danceability_list = []
speechiness_list = []
valence_list = []
popularity_list = []

# WRITE TO TXT DOC
with open("test3.txt", "w", encoding="utf-8") as f:
    for i, val in enumerate(track_names):
        f.write(track_names[i])
        f.write(' by ')
        f.write(artist_names[i])
        f.write('\nAUDIO FEATURES\n')
        audio_features, danceability, speechiness, valence, popularity = audio_features_str(track_uris[i])
        f.write(audio_features)
        f.write('\nDONE\n\n\n\n')
        
        # Append features and popularity to lists
        danceability_list.append(danceability)
        speechiness_list.append(speechiness)
        valence_list.append(valence)
        popularity_list.append(popularity)

# Create a DataFrame to calculate averages
data = {
    'Danceability': danceability_list,
    'Speechiness': speechiness_list,
    'Valence': valence_list,
    'Popularity': popularity_list
}

df = pd.DataFrame(data)

# Calculate average values based on popularity ranges
popularity_bins = [0, 33, 66, 100]
labels = ['Low', 'Medium', 'High']
df['PopularityRange'] = pd.cut(df['Popularity'], bins=popularity_bins, labels=labels)

average_values = df.groupby('PopularityRange').mean()

# WRITE AVERAGES TO TXT DOC
with open("averages.txt", "w", encoding="utf-8") as f:
    f.write("Average Values Based on Popularity Range\n")
    f.write(average_values.to_string())

print("Processing complete. Check 'test3.txt' for track details and 'averages.txt' for average values.")
