### Week 1

### Notes from meeting with team

#### To Do: Acquire Billboard Top 100 Data
> How far back should we look?
>> Goes back to 08-09-1958, eventually we'd like to get as long of a time series as possible

> How frequently should we sample?
>> Weekly if it's not too much data, monthly if it is

#### Once we have the Billboard data: 
> Search MusixMatch for the lyrics for those songs
> Search EchoNest for audio features

#### Create single database with all 3 (Billboard + Lyrics + EchoNest)
> Store as Pandas DataFrame?
> Key to join on : spotifyID probably. This should work for Joining Hot100 and EchoNest (TBD for sure). It should also work for adding the lyrics data (we may have to find the lyrics using other info such as song name and artist name, but then we can add the spotify id from the hot100 list to the lyrics database, and it will be a mutual key)
