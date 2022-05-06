from app import app
from flask import render_template, url_for

@app.route('/')
def home():
    names = []
    
    return render_template('home.html')

@app.route('/about')
def aboutPage():
    return render_template('about.html')

@app.route('/signup')
def signUp():
    return 
