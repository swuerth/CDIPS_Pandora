"""
Example of using the Spotify API through the spotipy python wrapper to return EchoNest musical features.
Run as 'python echonestExample.py' in the Terminal. 

"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pdb
import pandas as pd 

#these are MY API keys; get your own by registering for the Spotify API. 
#You'll probably each need to get your own since there are rate limits per key. 
client_id = '8c02bbb6dde64b128f6e39357e6b4cbf'
client_secret='36c765629d254655b8e32ce4b1e60615'

#seems to do an OR search on search terms, so just q='hotline bling drake' will return plenty of items. 

#intialize
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#search by artist and title. Can also search just by artist or just by title or just by album. 
results = sp.search(q='track:Hotline Bling artist:Drake', limit = 20, type = 'track')

#parse results. All these are identical. 
tids = []
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
    #also show the artist object if you want
    for j, k in enumerate(t['artists']):
        print 'artist ', j, ':', k['name']
    tids.append(t['uri'])
features = sp.audio_features(tids)
print(json.dumps(features, indent=4))

#another example, using the spotify IDs returned by Billboard (see BillboardExample.py)
spotifyID = u'1UfBAJfmofTffrae5ls6DA'
oneTrack = sp.track(spotifyID)
audio = sp.audio_features([spotifyID])

#load features data to a pandas DataFrame
features_df = pd.DataFrame.from_dict(features) 

#write features data to csv 
features_df.to_csv('spotifyFeaturesData.csv')