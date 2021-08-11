from flask import Flask, render_template, request, jsonify, redirect, session
from pymongo import MongoClient
from os import urandom
import utils

app = Flask(__name__)
# app.secret_key = urandom(24)
app.secret_key = 'yes'

client = MongoClient('mongodb://localhost:27017/')
db = client.hifzTracker
userCollection = db.users

@app.route('/')
def index():
    if 'loggedIn' in session:
        return render_template('index.html', user=session['user'], quote=utils.getRandomQuote())
    else: 
        return redirect('/login')



# LOGIN/LOGOUT/REGISTER ENDPOINTS

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        form = request.form
        username = form['username'].strip()
        passwordHash = form['password'].strip()

        user = userCollection.find_one({
            'username': username,
            'passwordHash': passwordHash
        })

        if user:
            print(user)
            # successful log in
            session['loggedIn'] = True
            session['user'] = {
                'name': user['name'],
                'username': user['username']
            }
            # session['userDetails'] = user['userDetails']

            return redirect('/')
        else:
            # login failed
            return jsonify({'Error': 'Login Details incorrect. Please try again'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        form = request.form

        username = form['username']
        passwordHash = form['password']
        name = form['name']


        doesUsernameExist = userCollection.find_one({"username": username})
        if doesUsernameExist:
            return jsonify({"Error": "this username already exists. please try again"})
        else:
            # Username doesnt exist
            userDetails = {
                'username': username,
                'passwordHash': passwordHash,
                'name': name
            }
            userCollection.insert_one(userDetails)
        
            return redirect('/login')