# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, request, redirect, session, url_for
from flask import request
from flask_pymongo import PyMongo



# -- Initialization section --
# from app import app
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:tXRmkwfSApoqtgTK@cluster0.urxps.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    session['username'] = 'Erin'
    collection = mongo.db.music
    music = collection.find({})
    return render_template('template.html', music = music)


# ADD SONGS

@app.route('/add')
def add():
    # define a variable for the collection you want to connect to
    music = mongo.db.music
    # use some method on that variable to add/find/delete data
    music.insert({"song":"Fly Me to the Moon", "artist":"Frank Sinatra", "description":"Iconic"})
    # return a message to the user (or pass data to a template)
    print('Song added')
    return render_template('template.html')


# SHOW A LIST OF ALL SONG TITLES

@app.route('/songs', methods={'GET', 'POST'})

# def songs():
#     if request.method == 'POST':
#         title = request.form['title']
#         artist = request.form['artist']
#         description = request.form['description']
    
#         collection = mongo.db.music
#         collection.insert({"song":title, "artist":artist, "description":description})
#         print('song added')
#         # return render_template('songs.html', music = music)
#         return redirect(url_for('index'))
#     else:
#        return render_template('songs.html')

def songs():
    if request.method == 'GET':
        collection = mongo.db.music
        music = collection.find({})
        return render_template('songs.html', music = music)
    else:
        title = request.form['title']
        artist = request.form['artist']
        description = request.form['description']
    
        collection = mongo.db.music
        collection.insert({"song":title, "artist":artist, "description":description})
        # return render_template('songs.html', music = music)
        return redirect(url_for('index'))


# @app.route('/new', methods=['POST'])

# def new():
#     if request.method == 'POST':
#         title = request.form['title']
#         artist = request.form['artist']
#         description = request.form['description']

#SIGN UP
@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('songs'))
        return 'That username already exists! Try logging in.'
    else: 
        return render_template('signup.html')

#LOGIN

@app.route('/login', methods=['POST', 'GET'])

def login():
    if request.method == 'POST':    
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('songs'))
                
            return 'Invalid username/password combination'
    
    else:
        return render_template('login.html')

@app.route('/logout')

def logout():
    return redirect(url_for('index'))

# ADVANCED: A FORM TO COLLECT USER-SUBMITTED SONGS




# DOUBLE-ADVANCED: SHOW ARTIST PAGE




# TRIPLE-ADVANCED: SHOW SONG PAGE
