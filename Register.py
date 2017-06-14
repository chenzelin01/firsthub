# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from google.appengine.ext import ndb
import logging
import cgi

class user(ndb.Model):
    """Sub model for representing an author."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    @classmethod
    def query_user(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

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
    try:
        logging.info('ancestor_key = ndb.Key("USER", uname or "*notitle*")')
        ancestor_key = ndb.Key("USER", uname or "*notitle*")
        logging.info('users = user.query_user(ancestor_key).fetch(20)')
        users = user.query_user(ancestor_key).fetch(1)
        logging.info('for u in users:')
        for u in users:
            logging.info(u.username)
            return render_template('registerform.html', username=uname, msg="wrong")

        logging.info('register new user')
        u = user(parent=ndb.Key("USER", uname or "*notitle*"))
        logging.info('u = user(parent=ndb.Key("USER", uname or "*notitle*"))')
        u.username = uname
        u.password = request.form['password']
        u.put()
        return render_template('loginform.html', username=uname)
    except:
        u = user(parent=ndb.Key("USER", uname or "*notitle*"))
        logging.info('u = user(parent=ndb.Key("USER", uname or "*notitle*"))')
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
    # ancestor_key =
    # u = user.query_user()
    if username == 'admin' and password == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('loginform.html', message='bad username or password', username=username)

if __name__ == '__main__':
    app.run()
