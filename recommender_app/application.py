from flask import Flask,render_template,request,redirect
app = Flask(__name__)

app.vars={}

app.question1={}
app.question1['What is your favorite decade for music?']=('1950s','1960s','1970s', '1980s', '1990s', '2000s', '2010s')

app.question2={}
app.question2['What is your favorite song or artist?']=('Song','Artist')

app.nquestion1=len(app.question1)
app.nquestion2=len(app.question2)

app.question1_answered = 0
app.question2_answered = 0

@app.route('/index',methods=['GET', 'POST'])
def index():
	nquestion1=app.nquestion1
	app.question1_answered = 0
	app.question2_answered = 0
	if request.method == 'GET':
		return render_template('welcome.html',num=nquestion1)
	else:
        #request was a POST
 		return redirect('/main')

@app.route('/main')
def main():
#	if len(app.questions)==0 and len(app.questions2)==0: 
	if app.question1_answered > 0 and app.question2_answered > 0: 
		return render_template('result.html')
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
		app.question1_answered = 0
		#for clarity (temp variables)
		n = app.nquestion1 - len(app.question1) + 1
		q = app.question1.keys()[0] #python indexes at 0
		#this will return the answers corresponding to q
		a1, a2, a3, a4, a5, a6, a7 = app.question1.values()[0]
		#save the current questions key
		app.currentq = q
		return render_template('layout.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3,ans4=a4,ans5=a5,ans6=a6,ans7=a7)
	else:    #request was a POST
		#Remove question from dictionary
		#if(len(app.questions)>0): del app.questions[app.currentq]
		app.question1_answered = app.question1_answered+1
	return redirect('/main')
 
 
@app.route('/next2',methods=['GET', 'POST'])
def next2(): #remember the function name does not need to match th eURL
	if request.method == 'GET':
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
	return redirect('/main')

 
if __name__ == "__main__":
	app.run(debug=True)
