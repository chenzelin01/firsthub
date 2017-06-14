# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from google.appengine.ext import ndb
import logging
import cgi

user_key = ndb.Key('user', 'default_user')
class user(ndb.Model):
    """Sub model for representing an author."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)

app = Flask(__name__)
@app.route('/0EDF3EDF5FBD4245C736DDF0FE76570E.txt', methods=['GET'])
def ssl():
    txt = 'D4C362234370B6C59CD1524336BCF1EC23D406B7\ncomodoca.com'
    return txt

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('registerform.html')

@app.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    logging.info(uname)
    # q = ndb.gql("SELECT * FROM user WHERE ANCESTOR IS :1 ORDER BY date DESC LIMIT 10", user_key)
    q = ndb.gql("SELECT * FROM user WHERE ANCESTOR IS :1", user_key)
    # q = user.query(user.username == 'zelin')
    # logging.info(q)
    # raise TypeError
    for u in q:
        logging(u.username)
        if u.username == uname:
            return render_template('registerform.html', username=uname, msg="wrong")
    u = user(parent=user_key)
    u.username = uname
    u.password = request.form['password']
    u.put()
    return render_template('loginform.html', username=uname)

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
