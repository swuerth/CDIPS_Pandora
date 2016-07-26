from flask import Flask,render_template,request,redirect
app = Flask(__name__)

import pandas as pd
import datetime
import numpy as np
from scipy import spatial

nreturn = 10 #number of similar songs to return
filename = 'response.txt'  #file to store user answers to questions

app.vars={}
app.artist={}
app.track={}
app.date={}
app.lyricsim={} 
app.sentiment={} 
app.lexdiv={}  

app.question1={}
app.question1['What is your favorite decade for music?']= \
('1950s','1960s','1970s', '1980s', '1990s', '2000s', '2010s')

app.question2={}
app.question2['What is your favorite song or artist?']=('Song','Artist')

app.nquestion1=len(app.question1)
app.nquestion2=len(app.question2)

app.question1_answered = 0
app.question2_answered = 0

@app.route('/index',methods=['GET', 'POST'])
def index():
	app.question1_answered = 0
	app.question2_answered = 0
	nquestion1=app.nquestion1
	if request.method == 'GET':
		return render_template('welcome.html',num=nquestion1)
	else:
        #request was a POST
		#f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'w')
		f = open(filename,'w')
		f.close()
 		return redirect('/main')

@app.route('/main')
def main():
#	if len(app.questions)==0 and len(app.questions2)==0: 
	if app.question1_answered > 0 and app.question2_answered > 0: 
		which_way = song_check()  ##function to check for song in database##
		if(which_way == 1):
			find_similar()   ##function to find similar songs##
			return render_template('result.html', input_artist=app.vars['artist_name'],\
		                       input_song=app.vars['song_name'], \
		                       input_date=app.vars['date'], \
		                       input_sent = app.vars['sentiment'], \
		                       input_lex = app.vars['lexdiv'], artist=app.artist, \
		                       track=app.track, date=app.date, lyricsim=app.lyricsim, \
		                       sentiment=app.sentiment, lexdiv=app.lexdiv)
		if(which_way == 2):  #found no MATCHES
			return render_template('tryagain.html')
		if(which_way == 3):  #got an artist, now need to list their songs
			return redirect('/pickasong')
		if(which_way == 4):  #found multiples songs with that title
			return redirect('/disambiguate')
			
#	elif len(app.questions)==1: 
	elif app.question1_answered == 0:
		return redirect('/next')
	else:
		return redirect('/next2')		

	
################################################################
## IMPORTANT: I have separated /next INTO GET AND POST
## You can also do this in one function, with If and Else
## The attribute that contains GET and POST is: request.method
#################################################################

@app.route('/next',methods=['GET', 'POST'])
def next(): #remember the function name does not need to match th eURL
	if request.method == 'GET':
		app.vars['song_or_artist'] = ''
		app.vars['song_name'] = ''
		app.vars['artist_name'] = ''
		app.question1_answered = 0
		app.question2_answered = 0
		#for clarity (temp variables)
		n = app.nquestion1 - len(app.question1) + 1
		q = app.question1.keys()[0] #python indexes at 0
		#this will return the answers corresponding to q
		a1, a2, a3, a4, a5, a6, a7 = app.question1.values()[0]
		#save the current questions key
		app.currentq = q
		return render_template('layout.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3,\
		                       ans4=a4,ans5=a5,ans6=a6,ans7=a7)
	else:    #request was a POST
		#Remove question from dictionary
		#if(len(app.questions)>0): del app.questions[app.currentq]
		app.question1_answered = app.question1_answered+1
	return redirect('/main')
 
 
@app.route('/next2',methods=['GET', 'POST'])
def next2(): #remember the function name does not need to match th eURL
	if request.method == 'GET':
		app.vars['song_or_artist'] = ''
		app.vars['song_name'] = ''
		app.vars['artist_name'] = ''
		app.question2_answered = app.question2_answered+0
		#for clarity (temp variables)
		n2 = app.nquestion2 - len(app.question2) + 1
		q2 = app.question2.keys()[0] #python indexes at 0
		#this will return the answers corresponding to q
		a1, a2= app.question2.values()[0] 
		#save the current questions key
		app.currentq2 = q2
		return render_template('layout2.html',num=n2,question=q2,ans1=a1,ans2=a2)
	else:    #request was a POST
		#Remove question from dictionary
		#if(len(app.questions2)>0): del app.questions2[app.currentq2]
		app.question2_answered = app.question2_answered+1
		app.vars['song_name'] = request.form['song_name']
		app.vars['artist_name'] = request.form['artist_name']
		app.vars['song_or_artist'] = request.form['answer_from_layout2']
	return redirect('/main')

 
@app.route('/pickasong',methods=['GET', 'POST'])
def pickasong(): #remember the function name does not need to match th eURL
	if request.method == 'GET':
		return render_template('pickasong.html',song_list=app.song_list)
	else:    #request was a POST
		app.vars['song_or_artist'] = 'Both'
		app.vars['song_name'] = app.song_list[np.int(request.form['song_pick'])]
 	return redirect('/main')
 
 
@app.route('/disambiguate',methods=['GET', 'POST'])
def disambiguate(): #remember the function name does not need to match th eURL
	if request.method == 'GET':
		return render_template('disambiguate.html', match_song=app.match_song,  \
		                                            match_artist=app.match_artist, \
		                                            match_date = app.match_date)
	else:    #request was a POST
		app.vars['song_or_artist'] = 'Both'
		app.vars['song_name'] = app.match_song[np.int(request.form['artist_pick'])]
		app.vars['artist_name'] = app.match_artist[np.int(request.form['artist_pick'])]
 	return redirect('/main')
 


def song_check():
	
	if(app.vars['song_or_artist'] == 'Both'):
		return(1)	

	#read df from pickle file
	#lyrics_df = pd.read_pickle('CleanedLyricsDF_MaxRank_100')
	lyrics_df = pd.read_pickle('LyricsDF_with_BoW_tdif_sparse')
	
	#read hot100df from pickle file
	#hot100_df = pd.read_pickle('./Billboard100DF_cleaned')

	if(app.vars['song_or_artist'] == 'Artist'):
		artist_i_like = app.vars['artist_name']
		match = lyrics_df[lyrics_df['artist_name']==artist_i_like]

	if(app.vars['song_or_artist'] == 'Song'):
		song_i_like = app.vars['song_name']
		match = lyrics_df[lyrics_df['track_name']==song_i_like]

	if len(match)==1 and app.vars['song_or_artist'] == 'Song':  #Found one matching song!!
		app.vars['artist_name'] = lyrics_df[lyrics_df['track_name']==song_i_like].artist_name.values[0]
		return(1)

	if len(match)==0:  #Found NO matches
		return(2)

	if(app.vars['song_or_artist'] == 'Artist'): #Got an artist, now need to get their songs
		app.song_list={}
		song_list = lyrics_df[lyrics_df['artist_name']==artist_i_like]
		song_list = song_list.reset_index()
		for x in range(len(song_list['track_name'])):
			app.song_list[x] = song_list['track_name'][x]
		return(3)

	if len(match)>0 and app.vars['song_or_artist'] == 'Song':  #Found multiples songs
		app.match_artist = {}
		app.match_song = {}
		app.match_date = {}
		match = lyrics_df[lyrics_df['track_name']==song_i_like]
		match = match.reset_index()
		match['date'] = match['date'].apply(lambda x: x.date())
		for x in range(len(match['track_name'])):
			app.match_song[x] = match['track_name'][x]
			app.match_artist[x] = match['artist_name'][x]
			app.match_date[x] = match['date'][x]
		return(4)
	

def cos_dis(your_song_bow_vec, other_song_bow_vec):
    result = spatial.distance.cosine(your_song_bow_vec, other_song_bow_vec)
    return result

def find_similar():

	#lyrics_df = pd.read_pickle('CleanedLyricsDF_MaxRank_100')
	lyrics_df = pd.read_pickle('LyricsDF_with_BoW_tdif_sparse')
		
	CosDis2 = pd.read_pickle('CosDis_tfidf_reduced')
	CosDis2 = CosDis2.as_matrix()
	
	song_i_like = app.vars['song_name']
	artist_i_like = app.vars['artist_name']

###########test that we are reading the lyrics dataframe and cosine distance dataframe
###########consistently
#	song1 = 'Bohemian Rhapsody'
#	song2 = 'Cool for the Summer'

#	bow1 = lyrics_df[lyrics_df['track_name']==song1].tfidf_array.values[0].toarray()
#	bow2 = lyrics_df[lyrics_df['track_name']==song2].tfidf_array.values[0].toarray()
#	print 'size bag of words vectors = ', np.shape(bow1), ' and ', np.shape(bow2)
#	cos_distance = cos_dis(bow1,bow2)
#	print 'cosine distance between ', song1, ' and ', song2 , ' = '
#	print cos_distance

#	bow1 = lyrics_df[lyrics_df['track_name']==song1].tfidf_array.values[0].toarray()
#	bow2 = lyrics_recent[lyrics_recent['track_name']==song2].tfidf_array.values[0].toarray()
#	print 'size bag of words vectors = ', np.shape(bow1), ' and ', np.shape(bow2)
#	cos_distance = cos_dis(bow1,bow2)
#	print 'cosine distance between ', song1, ' and ', song2 , ' = '
#	print cos_distance

#	index1 = lyrics_df[lyrics_df['track_name']==song1].index
#	index2 = lyrics_recent[lyrics_recent['track_name']==song2].index
	
#	print CosDis2.shape
#	print 'index1 =', index1, 'index2 =', index2
#	print CosDis2[index1, index2]
#################################################	
	
	#get date of inputted song
	input_date=lyrics_df[lyrics_df['track_name']==song_i_like].date.values[0]
	input_date = input_date.astype('datetime64[D]')
	app.vars['date'] = input_date

	#find songs with similar sentiment
	sentiment = lyrics_df[lyrics_df['track_name']==song_i_like].compound_sentiment.values[0]
	lyrics_df['dist1'] = lyrics_df.compound_sentiment.map((lambda x: abs(sentiment - x)))	
	app.vars['sentiment'] = sentiment
	
	#define similarity as diff between your song's lexical diversity & that of other songs
	lex = lyrics_df[lyrics_df['track_name']==song_i_like].lex_diversity.values[0]
	lyrics_df['dist2'] = lyrics_df.lex_diversity.map((lambda x: abs(lex - x)))
	app.vars['lexdiv'] = lex

	pd.options.mode.chained_assignment = None  # default='warn'

	#determine which recent song has most similarity in lyrics
	lyrics_recent = lyrics_df[lyrics_df['date']>datetime.date(2013,1,1)]
	lyrics_recent = lyrics_recent.reset_index()
	del lyrics_recent['index']
	
	my_pick = lyrics_df[lyrics_df['track_name']==song_i_like]
	index1 =  my_pick[my_pick['artist_name']==artist_i_like].index

	lyrics_recent['dist3'] = 2.0
	num_recent_songs = len(lyrics_recent)
	for j in range(num_recent_songs):
		lyrics_recent['dist3'].iloc[j] = CosDis2[index1, j]

 	lyrics_recent['dist_tot'] = lyrics_recent['dist1'] + lyrics_recent['dist2'] + lyrics_recent['dist3']
 	
	#recommend nreturn songs based on lexical diversity
	#result = lyrics_df[lyrics_df['date']>datetime.date(2013,1,1)].sort_values('dist')[:nreturn] 
	result = lyrics_recent.sort_values('dist_tot')[:nreturn]
 	result = result.reset_index()
 
 	result['date'] = result['date'].apply(lambda x: x.date())
 
 	for x in range(0,nreturn):
 		app.artist[x] = result['artist_name'][x]
 		app.track[x] =  result['track_name'][x]
 		app.date[x] =   result['date'][x]
 		app.lyricsim[x] = 1-result['dist3'][x]
 		app.sentiment[x] =   result['compound_sentiment'][x]
 		app.lexdiv[x] =  result['lex_diversity'][x]


 
if __name__ == "__main__":
	app.run(port=33507)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
