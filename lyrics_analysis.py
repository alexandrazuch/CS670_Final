import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string

# https://blog.enterprisedna.co/python-remove-punctuation-from-string/#:~:text=To%20remove%20punctuation%20from%20a,new%20string%20excluding%20punctuation%20marks.
def remove_punctuation(input_string):  
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)
    # Apply the translation table to the input string
    result = input_string.translate(translator)
    result = re.sub('[0-9]Embed', '', result)
    result = re.sub('Embed', '', result)
    return result

# print(remove_punctuation("Hello, [you-are-cool]!"))

sw = stopwords.words('english')

# create dictionary of each song
def dict_of_songs(lines, dict):
    song_lyrics = []
    lyrics = False
    found_song = False
    i = 0
    for line in lines:
        if line == 'LYRICSSTART\n':  # start looking at lyrics at 'LYRICSSTART'
            i = i+1
            # print("Found song!")
            lyrics = True
            found_song = True
            continue
        if line == 'LYRICSEND\n':  # stop looking at lyrics at 'LYRICSEND'
            dict[i] = song_lyrics
            song_lyrics = []
            lyrics = False
            continue
        if lyrics:
            if found_song:  # don't include the translations information in second row of lyrics
                found_song = False
                continue
            for word in line.split():
                new_word = word.lower()
                for w in new_word.split('-'):
                    if not (('[' in w) or (']' in w) or (w in sw)):
                        song_lyrics.append(remove_punctuation(w))

'''
LYRIC FREQUENCY DISTRIBUTION BASED ON VALENCE SCORES
CHECK divide_songs.py
'''

f_pos = open("positive_lyrics.txt", "r", encoding="utf8")
f_neu = open("neutral_lyrics.txt", "r", encoding="utf8")
f_neg = open("negative_lyrics.txt", "r", encoding="utf8")

pos_lines = f_pos.readlines()
neu_lines = f_neu.readlines()
neg_lines = f_neg.readlines()

pos_dict = {}
neu_dict = {}
neg_dict = {}

dict_of_songs(pos_lines, pos_dict)
dict_of_songs(neu_lines, neu_dict)
dict_of_songs(neg_lines, neg_dict)

# print(pos_dict)

pos_lyrics = []
neu_lyrics = []
neg_lyrics = []
for key in pos_dict:
    pos_lyrics = pos_lyrics + pos_dict[key]
for key in neu_dict:
    neu_lyrics = neu_lyrics + neu_dict[key]
for key in neg_dict:
    neg_lyrics = neg_lyrics + neg_dict[key]

pos_fdist = nltk.FreqDist(pos_lyrics)
neu_fdist = nltk.FreqDist(neu_lyrics)
neg_fdist = nltk.FreqDist(neg_lyrics)

print('POSITIVE')
print(pos_fdist.most_common(50))
print('\n\nNEUTRAL')
print(neu_fdist.most_common(50))
print('\n\nNEGATIVE')
print(neg_fdist.most_common(50))