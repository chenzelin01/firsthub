# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, session, escape
import Config
app = Flask(__name__)
app.secret_key = Config.SECRET_STRING
# app.production = not Config.DEVELOPMENT
# app.debug = app.development = Config.DEVELOPMENT
from google.appengine.ext import ndb
import logging
import json
import urllib
import requests

class user(ndb.Model):
    """Sub model for representing an user."""
    username = ndb.StringProperty()
    password = ndb.StringProperty()

    a_counts = ndb.IntegerProperty()
    b_counts = ndb.IntegerProperty()
    c_counts = ndb.IntegerProperty()
    d_counts = ndb.IntegerProperty()
    e_counts = ndb.IntegerProperty()
    g_counts = ndb.IntegerProperty()

    date = ndb.DateTimeProperty(auto_now_add=True)
    @classmethod
    def query_user(cls, username):
        ancestor_key = ndb.Key('USER', username or "*notitle*")
        return cls.query(ancestor=ancestor_key).order(-cls.date)

    def add_gesture_counts(self, gesture_name):
        logging.info(gesture_name)
        if gesture_name == 'a':
            self.a_counts += 1
        elif gesture_name == 'b':
            self.b_counts += 1
        elif gesture_name == 'c':
            self.c_counts += 1
        elif gesture_name == 'd':
            self.d_counts += 1
        elif gesture_name == 'e':
            self.e_counts += 1
        elif gesture_name == 'g':
            self.g_counts += 1
        self.put()

    @classmethod
    def clean_user_record(cls):
        users = user.query()
        for u in users:
            u.a_counts = 0
            u.b_counts = 0
            u.c_counts = 0
            u.d_counts = 0
            u.e_counts = 0
            u.g_counts = 0
            u.put()

class GestureRecord(ndb.Model):
    """model for representing an gesture record"""
    # the record is a json string with keys: person_name gesture_name and gesture_position
    record = ndb.TextProperty()
    person_name = ndb.StringProperty()
    gesture_name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    @classmethod
    def put_data(cls, person_name, gesture_name, gesture_path):
        record_ = {'person_name': person_name,
                  'gesture_name': gesture_name,
                  'gesture_position': []}
        gesture_position = []
        path_ = json.loads(gesture_path)
        for pos in path_:
            gesture_position.append([float(pos['x']), float(pos['y'])])
        record_['gesture_position'] = gesture_position
        tp_str = json.dumps(record_)
        ancestor_key = ndb.Key('RECORD', 'default_record')
        logging.info('temp_record = GestureRecord(parent=ancestor_key)')
        temp_record = GestureRecord(parent=ancestor_key)
        temp_record.record = tp_str
        temp_record.person_name = person_name
        temp_record.gesture_name = gesture_name
        temp_record.put()

    @classmethod
    def query_record(self, limit=None):
        ancestor_key = ndb.Key('RECORD', 'default_record')
        q = GestureRecord.query(ancestor=ancestor_key).order(-GestureRecord.date)
        if limit is not None:
            return q.fetch(limit)
        else:
            return q

@app.route('/0EDF3EDF5FBD4245C736DDF0FE76570E.txt', methods=['GET'])
def ssl():
    txt = 'D4C362234370B6C59CD1524336BCF1EC23D406B7\ncomodoca.com'
    return txt

@app.route('/.well-known/pki-validation/fileauth.txt')
def ssl2():
    txt = '201706181808515n3q9bu9ao8ksv76am432vecfs8xwl6msc2ytjfoxa3zmc2lo0'
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
        logging.info('users = user.query_user(ancestor_key).fetch(20)')
        users = user.query_user(uname).fetch(1)
        logging.info('for u in users:')
        for u in users:
            logging.info(u.username)
            return render_template('registerform.html', username=uname, msg="wrong")

        logging.info('register new user')
        u = user(parent=ndb.Key("USER", uname or "*notitle*"))
        logging.info('u = user(parent=ndb.Key("USER", uname or "*notitle*"))')
        u.username = uname
        u.password = request.form['password']
        u.a_counts = 0
        u.b_counts = 0
        u.c_counts = 0
        u.d_counts = 0
        u.e_counts = 0
        u.g_counts = 0
        u.put()
        return render_template('loginform.html', username=uname)
    except:
        u = user(parent=ndb.Key("USER", uname or "*notitle*"))
        logging.info('u = user(parent=ndb.Key("USER", uname or "*notitle*"))')
        u.username = uname
        u.password = request.form['password']
        u.a_counts = 0
        u.b_counts = 0
        u.c_counts = 0
        u.d_counts = 0
        u.e_counts = 0
        u.g_counts = 0
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
    users = user.query_user(username)
    logging.info('query_success')
    for u in users:
        if password == u.password:
            # logging.info('before login ' + session['user'])
            session['user'] = username
            logging.info('after login ' + session['user'])
            return render_template('signin-ok.html',
                                   username=username,
                                   a_counts=u.a_counts,
                                   b_counts=u.b_counts,
                                   c_counts=u.c_counts,
                                   d_counts=u.d_counts,
                                   e_counts=u.e_counts,
                                   g_counts=u.g_counts,
                                   check_value='a')
    return render_template('loginform.html', message='wrong username or wrong password', username=username)

@app.route('/submitgesture', methods=['GET'])
def submitgesture_get():
    try:
        person_name = session['user']
        return render_template('loginform.html', message='please login first!', username=person_name)
    except Exception as e:
        logging.info(e)
        return render_template('loginform.html', message='please login first!')

@app.route('/submitgesture', methods=['POST'])
def submitgesture_post():
    try:
        person_name = session['user']
    except Exception as e:
        logging.info(e)
        return 'please login first'
    logging.info('person_name: ' + person_name)
    gesture_name = request.form['gesture_kind']
    gesture_path = request.form['gesture_path']
    logging.info('gesture_name: ' + gesture_name)
    logging.info('len of gesture_path: ' + str(len(gesture_path)))
    # add gesture count to the db
    users = user.query_user(person_name)
    for u in users:
        try:
            if request.form['submit_flag'] == 'true' and len(gesture_path) > 10:
                GestureRecord.put_data(person_name, gesture_name, gesture_path)
                u.add_gesture_counts(gesture_name)
        except:
            # maybe the user just refresh the webpage so nothing submit
            pass
        finally:
            return render_template('signin-ok.html',
                                   username=person_name,
                                   a_counts=u.a_counts,
                                   b_counts=u.b_counts,
                                   c_counts=u.c_counts,
                                   d_counts=u.d_counts,
                                   e_counts=u.e_counts,
                                   g_counts=u.g_counts,
                                   check_value=gesture_name)

@app.route('/querydata', methods=['GET'])
def query_data():
    try:
        args = request.args
        limit = args['limit']
        if limit > 5000:
            limit = 5000
        person_name = session['user']
        if person_name == 'chenzelin':
            gestures = GestureRecord.query_record(limit=limit)
            gs = []
            for g in gestures:
                gs.append(g.record)
                g.key.delete()
            logging.info(len(gs))
            return json.dumps(gs)
        else:
            return 'you are not the admin so can not query the gesture data'
    except Exception as e:
        logging.error(e)
        try:
            return json.dumps(gs)
        except Exception as e:
            return e


@app.route('/cleanrecord', methods=['GET'])
def clean_record():
    try:
        person_name = session['user']
        if person_name == 'chenzelin':
            user.clean_user_record()
            return 'clean success'
        else:
            return 'you are not the admin so can not clean the gesture data'
    except:
        pass
        return '404 somthing wrong happened'

if __name__ == '__main__':
    # logging.info('running main or not')
    app.run('127.0.0.1', port=80)
    # json_str = '[{"x":223.24700927734375,"y":149.74600219726562},{"x":214.79400634765625,"y":144.91500854492188},{"x":211.17098999023438,"y":144.91500854492188},{"x":206.33999633789062,"y":144.91500854492188},{"x":202.71701049804688,"y":144.91500854492188},{"x":200.302001953125,"y":144.91500854492188},{"x":195.47100830078125,"y":144.91500854492188},{"x":190.6409912109375,"y":144.91500854492188},{"x":187.01800537109375,"y":144.91500854492188},{"x":182.18701171875,"y":144.91500854492188},{"x":177.35699462890625,"y":144.91500854492188},{"x":167.69601440429688,"y":149.74600219726562},{"x":164.072998046875,"y":154.57598876953125},{"x":159.24200439453125,"y":164.23699951171875},{"x":155.61898803710938,"y":173.89801025390625},{"x":150.78900146484375,"y":185.97500610351562},{"x":147.16598510742188,"y":193.22100830078125},{"x":143.54299926757812,"y":206.5050048828125},{"x":141.12799072265625,"y":212.54299926757812},{"x":138.71200561523438,"y":217.37298583984375},{"x":136.2969970703125,"y":229.45001220703125},{"x":136.2969970703125,"y":233.072998046875},{"x":136.2969970703125,"y":242.7340087890625},{"x":136.2969970703125,"y":246.35699462890625},{"x":136.2969970703125,"y":251.18701171875},{"x":136.2969970703125,"y":252.39498901367188},{"x":136.2969970703125,"y":254.80999755859375},{"x":136.2969970703125,"y":256.01800537109375},{"x":137.5050048828125,"y":257.2250061035156},{"x":139.92001342773438,"y":257.2250061035156},{"x":147.16598510742188,"y":257.2250061035156},{"x":155.61898803710938,"y":257.2250061035156},{"x":161.65701293945312,"y":257.2250061035156},{"x":170.11099243164062,"y":257.2250061035156},{"x":183.39498901367188,"y":249.98001098632812},{"x":196.67898559570312,"y":241.5260009765625},{"x":209.9630126953125,"y":228.24200439453125},{"x":223.24700927734375,"y":214.9580078125},{"x":232.90802001953125,"y":201.67401123046875},{"x":236.531005859375,"y":194.42800903320312},{"x":242.5689697265625,"y":181.14401245117188},{"x":248.60797119140625,"y":165.44500732421875},{"x":255.85302734375,"y":150.9530029296875},{"x":258.26898193359375,"y":135.25399780273438},{"x":259.47601318359375,"y":130.42300415039062},{"x":258.26898193359375,"y":128.00799560546875},{"x":257.06097412109375,"y":126.79998779296875},{"x":254.64599609375,"y":128.00799560546875},{"x":251.02301025390625,"y":137.66900634765625},{"x":251.02301025390625,"y":143.70700073242188},{"x":248.60797119140625,"y":150.9530029296875},{"x":244.9849853515625,"y":163.02999877929688},{"x":242.5689697265625,"y":175.10598754882812},{"x":242.5689697265625,"y":182.35198974609375},{"x":238.94598388671875,"y":193.22100830078125},{"x":238.94598388671875,"y":201.67401123046875},{"x":238.94598388671875,"y":208.92001342773438},{"x":238.94598388671875,"y":217.37298583984375},{"x":238.94598388671875,"y":225.82699584960938},{"x":238.94598388671875,"y":233.072998046875},{"x":238.94598388671875,"y":241.5260009765625},{"x":238.94598388671875,"y":247.56399536132812},{"x":238.94598388671875,"y":252.39498901367188},{"x":238.94598388671875,"y":257.2250061035156},{"x":242.5689697265625,"y":260.8479919433594},{"x":243.7769775390625,"y":262.0559997558594},{"x":246.1920166015625,"y":264.47100830078125},{"x":251.02301025390625,"y":269.302001953125},{"x":254.64599609375,"y":272.92498779296875},{"x":257.06097412109375,"y":275.3399963378906},{"x":258.26898193359375,"y":275.3399963378906},{"x":261.89202880859375,"y":276.5480041503906},{"x":263.0989990234375,"y":276.5480041503906},{"x":266.72198486328125,"y":280.1709899902344},{"x":267.92999267578125,"y":280.1709899902344},{"x":270.344970703125,"y":280.1709899902344}]'
    # record = {'person_name': 'zelin',
    #           'gesture_name': 'a',
    #           'gesture_position': []}
    # gesture_position = []
    # path_ = json.loads(json_str)
    # for pos in path_:
    #     gesture_position.append([float(pos['x']), float(pos['y'])])
    # record['gesture_position'] = gesture_position
    # logging.info('len of record[\'gesture_position\']' + str(len(record['gesture_position'])))
    # record = json.dumps(record)
    # logging.info("before put record")
    # print record