# CDIPS\_Pandora
## CDIPS Summer Data Science Workshop
### Project Description:
### Evolution of Music (Claire Dorman @ Pandora):  
> In my project, students will explore the evolution of hit music through time series analysis of the Billboard chart archives. There are a few different paths the project could take, depending on the interests of the students. For instance, they could use natural language processing on the lyrics of the top-charting songs, using pre-processed lyrics from the MusixMatch dataset, to understand how listeners' musical mood preferences change over the course of a year. Alternatively, they could explore how the stability of the Hot 100 list has changed over the last decade. As on-demand streaming has replaced album sales and social media ensures that ever-larger communities become quickly aware of the same popular culture trends, do our favorite tracks remain so for a longer or shorter period of time than, say, 10 years ago? In either project, students could also explore musicological tags from the EchoNest dataset to identify any musical features that are exceptionally stable or variable over time.

### Note from swuerth:
### MXM\_Explore notebook was made just to get started doing something during pre-workshop week
### Next step is to follow the instructions in the evolution_of_music.docx

### For the MXM\_Explore notebook, swuerth did the following:
> Downloaded data from http://labrosa.ee.columbia.edu/millionsong/musixmatch#getting
> Stored the test and train text files in a directory called "mxm\_data"
> mxm\_data should be in the CDIPS\_Pandora directory (this repository)
> The files used are mxm\_dataset\_test.txt   mxm\_dataset\_train.txt
> They are preprocessed lyrics, stored as Bag of Words vectors for each song
> The vectors are stored in sparse format as word\_index:word\_count 
> Where word\_index ranges from 1 to 5000 as only the 5000 most common words are counted
