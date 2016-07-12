"""
Example of searching the musixmatch dataset for "Hotline Bling"

Note that only 30% of lyrics are returned, and they 
include the line "This Lyrics is NOT for Commercial use."
Remember to not include that in any NLP!
Also, the lyrics have newline characters \n.

Run as 'python musixmatchExample.py' in the Terminal. 
"""

from musixmatch.track import TracksCollection
from musixmatch.lyrics import Lyrics
import pdb
import pandas as pd 

#my personal API key. Get your own at the MusixMatch developer site (see the instructions)
apikey = "f8a009fe01e53de1e8a1388e60812ef5" 

#Search data set 
collection = TracksCollection.fromSearch(q_track="Hotline Bling", apikey = apikey)

#Results - track names - all have the same name
tracknames = [t['track_name'] for t in collection]
print 'Track names: ', tracknames

#Results - artist names - notice only one of them is Drake
artists = [t['artist_name'] for t in collection]
print 'Artist: ', artists

#Track IDs
track_id = [t['track_id'] for t in collection]
 
#find the track ID corresponding to the Drake version 
drake_track_id = track_id[artists == 'Drake']

#return lyrics
lyrics = Lyrics(track_id = drake_track_id, apikey = apikey)

print "Keys in Lyrics object: ", lyrics.keys()

print "Lyrics: ", lyrics['lyrics_body']


#Write a subset of the columns to a Pandas object 
cols = ['lyrics_id', 'has_lyrics', 'artist_name', 'track_spotify_id']
subset = pd.DataFrame.from_dict(collection)[cols].set_index('track_spotify_id')

#dump pandas object to a database
subset.to_csv('musixmatch_data.csv')
