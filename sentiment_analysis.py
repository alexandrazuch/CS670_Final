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
    result = re.sub('embed', '', result)
    return result

# print(remove_punctuation("Hello, [you-are-cool]!"))

sw = stopwords.words('english')

# create dictionary of each song
def string_of_lyrics(lines):
    string = ""
    lyrics = False
    found_song = False
    for line in lines:
        if line == 'LYRICSSTART\n':  # start looking at lyrics at 'LYRICSSTART'
            # print("Found song!")
            lyrics = True
            found_song = True
            continue
        if line == 'LYRICSEND\n':  # stop looking at lyrics at 'LYRICSEND'
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
                        # print(string)
                        string += remove_punctuation(w) + ' '
    return string


f_pos = open("positive_lyrics.txt", "r", encoding="utf8")
f_neu = open("neutral_lyrics.txt", "r", encoding="utf8")
f_neg = open("negative_lyrics.txt", "r", encoding="utf8")

pos_lines = f_pos.readlines()
neu_lines = f_neu.readlines()
neg_lines = f_neg.readlines()

'''
SENTIMENT ANALYSIS
'''
pos_string = string_of_lyrics(pos_lines)
neu_string = string_of_lyrics(neu_lines)
neg_string = string_of_lyrics(neg_lines)

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

print('POSITIVE')
print(sia.polarity_scores(pos_string))
print('\n\nNEUTRAL')
print(sia.polarity_scores(neu_string))
print('\n\nNEGATIVE')
print(sia.polarity_scores(neg_string))

