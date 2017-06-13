# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from google.appengine.ext import db, ndb
import logging

class user(db.Model):
    """Sub model for representing an author."""
    username = db.StringProperty(indexed=False)
    password = db.StringProperty(indexed=False)


app = Flask(__name__)
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('registerform.html')

@app.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    try:
        logging.info(uname)
        q = user.all()
        logging.info(q)
        for u in q.run(limit=2):
            logging(u.username + ' ' + u.password)
        return render_template('loginform.html?msg=wrongname', username=uname)
    except:
        logging.info("error occur")
        u = user()
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
