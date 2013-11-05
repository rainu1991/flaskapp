import psycopg2
from functools import wraps
from flask import Flask, render_template, request, flash
from flask import *
from functools import wraps
from time import *
import database
                                        
 
app = Flask(__name__)                                         #Create an instance of this class 

app.config.from_object(__name__)
 
app.secret_key = 'development key' 



@app.route('/')                                               # maps the URL / to a Python function home
def home():
  	
  return render_template('home.html')



@app.route('/view')                                       #maps the URL /view to a python function view
def view():
	con = psycopg2.connect(database='rainu') 
  	cur = con.cursor()	
	cur.execute("SELECT id,title, text, comment, time FROM post ORDER BY id DESC")
	posts = [dict(id=row[0],title=row[1], text=row[2], comment=row[3], time=row[4]) for row in cur.fetchall()]	
	con.commit()
	con.close()
	return render_template('comment.html',posts=posts)	
  


def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return test(*args, **kwargs)
    else:
      flash('You need to login first.')
      return redirect(url_for('log'))
  return wrap

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect (url_for('log'))

@app.route('/hello')
@login_required
def hello():
  con = psycopg2.connect(database='rainu') 
  return render_template('post.html')


@app.route('/log', methods=['GET', 'POST'])             #login form validation function
def log():
  error = None
  if request.method == 'POST':
    if request.form['username'] != 'rainu' or request.form['password'] != '1234':
      error = 'Invalid Entry. Please try again'
    else:
      session['logged_in'] = True
      return redirect(url_for('hello'))
  return render_template('log1.html', error=error)
 

@app.route('/post',methods=['POST'])                         #Function for posting data into database
def add_entry():
	con = psycopg2.connect(database='rainu')    
	cur = con.cursor()
	cur.execute('INSERT INTO post (title, text, time) VALUES (%s, %s, %s)',[request.form['title'],request.form['text'],strftime("%d %b %Y ", gmtime())])
	con.commit()
	con.close()
	return redirect(url_for('show_entries'))

@app.route('/post')                                           #Retrieve data from database
def show_entries():
	con = psycopg2.connect(database='rainu') 
	cur = con.cursor() 
	cur.execute('SELECT id,title, text FROM post ORDER BY id DESC')
	posts = [dict(id=row[0],title=row[1], text=row[2]) for row in cur.fetchall()]
	con.close()
	return render_template('post.html',posts=posts)

@app.route('/pos',methods=['POST'])                         #Function for adding comment into database                  
def add_data():
	p=request.form['id']
	print p
	con = psycopg2.connect(database='rainu') 
	cur = con.cursor()
	cur.execute("SELECT comment FROM post WHERE id=%s",[p])
	comments=[cur.fetchall()]	
	print comments
	if comments[0][0][0] == None:
		cur.execute('UPDATE post SET comment=%s WHERE id=%s',[request.form['comments'],request.form['id']])
	else:
		cur.execute('UPDATE post SET comment=%s WHERE id=%s',[request.form['comments']+'\n'+comments[0][0][0],request.form['id']])	
		


	cur = con.cursor()	
	cur.execute("SELECT id,title, text, comment, time FROM post ORDER BY id DESC")
	posts = [dict(id=row[0],title=row[1], text=row[2], comment=row[3], time=row[4]) for row in cur.fetchall()]	
	con.commit()
	con.close()
	return render_template('comment.html',posts=posts)
	


if __name__ == '__main__':
  app.run(debug=True)                                         #run() function to run our Server.
