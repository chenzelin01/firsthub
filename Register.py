# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from google.appengine.ext import ndb

class user(ndb.Model):
    """Sub model for representing an author."""
    username = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)


app = Flask(__name__)
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('registerform.html')

@app.route('/register', methods=['POST'])
def register():
    u = user()
    u.username = request.form['username']
    u.password = request.form['password']
    u.put()
    return render_template('loginform.html', username='jolin')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('loginform.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('loginform.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('loginform.html', message='bad username or password', username=username)

if __name__ == '__main__':
    app.run()
