### Week 1

### Tuesday July 12, Claire + Team, Google Hangout

#### Next meeting: Google Hangout again 10am Friday July 15

#### Plans/tasks for database:
> Get everything in Pandas DataFrame, we can use pickle.dump() to save everything
>> Elena and Ed : Work on getting lots of EchoNest data stored nicely in a DF

>> Steph: Work on getting lots of lyrics data

#### Other plans/tasks:
> Athena: Learn flask for making web apps. It will be cool to have a web app no matter what we end up presenting. Either for a recommender or for displaying different visualizations (e.g., input feature like danceability and output a pretty time series of that feature)

#### Once we have the database ready we can start:
> NLP on lyrics

> Reporoducing EchoNest findings from http://blog.echonest.com/post/70299217721/7-decades-7-musical-evolutions as a sanity check

> Removing trends and exploring seasonality

> Unsupervised recommendations -- we dont have user data so we have to use similarities between songs/artists to recommend things. In industry such a product would be tested with AB testing, but we arent able to do that in our context. 
 


### Monday July 11, Team Meeting 401 McCone

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
