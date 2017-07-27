# -*- coding:utf-8 -*-
import webapp2
import urllib2
import urllib
import time
import json
import cookielib
from google.appengine.ext import ndb
import logging
Debug = True
INFO = 'info'

class info(ndb.Model):
    """Sub model for representing an info."""
    uid = ndb.StringProperty()
    sid = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def update_uid(uid):
        try:
            info_ = info.query_info().fetch(1)[0]
            logging.info('info.query_info().fetch(1) ')
            info_.uid = uid
            logging.info('info_.uid = uid')
            info_.put()
        except Exception as e:
            logging.error(e)
            info_ = info(parent=ndb.Key("INFO", INFO or "*notitle*"))
            info_.uid = uid
            info_.sid = 'none'
            info_.put()

    @staticmethod
    def update_sid(sid):
        try:
            info_ = info.query_info().fetch(1)[0]
            info_.sid = sid
            info_.put()
        except:
            info_ = info(parent=ndb.Key("INFO", INFO or "*notitle*"))
            info_.sid = sid
            info_.uid = 'none'
            info_.put()
            logging.info('sid create success')

    @classmethod
    def query_info(cls):
        ancestor_key = ndb.Key('INFO', INFO or "*notitle*")
        return cls.query(ancestor=ancestor_key).order(-cls.date)

    @staticmethod
    def get_uid_sid():
        info_ = info.query_info().fetch(1)[0]
        return info_.uid, info_.sid

class Upload(webapp2.RedirectHandler):
    def get(self):
        get = self.request.GET
        success_info = ''
        try:
            uid = get['uid']
            logging.info('update uid ' + uid)
            info.update_uid(uid)
            success_info += 'update uid success'
            logging.info('update uid success')
        except:
            pass
        try:
            sid = get['sid']
            info.update_sid(sid)
            success_info += 'update sid success'
            logging.info('update sid success')
        except:
            pass
        self.response.write(success_info)


class GXQDaily(webapp2.RedirectHandler):

    def get(self):
        domain = "http://jolintutor.herokuapp.com"
        req = urllib2.Request(domain)
        reponse = urllib2.urlopen(req)
        self.response.write(reponse.read())
        # self.sid = self.get_gxq_sid()
        # file = self.gxq_gold() + "\n " + self.gxq_ice()
        # self.response.write(file)


    def gxq_gold(self):
        if self.sid is None:
            self.sid = self.get_gxq_sid()
        # gold cron
        domain = "http://fjwebs.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': self.sid,
            'version': '1.1.5',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(domain + url, para)
        reponse = urllib2.urlopen(req)
        file = reponse.read()
        json_ = json.loads(file, encoding='utf-8')
        return json_['msg'].encode('utf-8')

    def gxq_ice(self):
        if self.sid is None:
            self.sid = self.get_gxq_sid()
        # ice cron
        domain = "http://appweb.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': self.sid,
            'version': '5.4.0',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(url=domain + url, data=para)
        reponse = urllib2.urlopen(req)
        file = reponse.read()
        json_ = json.loads(file, encoding='utf-8')
        json_['msg'] = json_['msg'].encode('utf-8')
        return json_['msg']

    # def yooli(self):
    #     # yooli.com cron
    #     domain = "http://app.yooli.com/"
    #     url = "app3.0/core/add/user/sign+points"
    #     para = {
    #         'sign': 'true',
    #         'ui': '2311358',
    #         'tm': str(int(time.time())),
    #         'nc': '3540a6',
    #         'di': '05c07a213fd11bd2d20064fb97ed8940',
    #         'mt': '3',
    #         'v': '200705',
    #         'ost': '20',
    #         'channelId': '%E5%BA%94%E7%94%A8%E5%AE%9D%C2%B7%E8%85%BE%E8%AE%AF%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0',
    #         'sid': '417',
    #         'dn': 'HUAWEI+HUAWEI+GRA-TL00',
    #         'sh': '1794',
    #         'sw': '1080',
    #         'ss': '3.0',
    #         'osv': '5.0.1+android-29of40',
    #         'si': '40023142896f816b3714cc3441b621e7e530a45b'
    #     }
    #     para = urllib.urlencode(para)
    #     req = urllib2.Request(url=domain + url, data=para)
    #     reponse = urllib2.urlopen(req)
    #     file = reponse.read()
    #     return file

    def get_gxq_sid(self):
        # uid, sid = info.get_uid_sid()
        # return sid
        return "7d92e135fc60b2d2ded78aed06ad1cfa"

    def ssccat_login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'),
            ('Origin', 'https://www.ssccat.tk')
        ]
        urllib2.install_opener(opener)
        domain = "https://www.ssccat.tk"
        url = "/auth/login"
        para = {
            'email': '734880901@qq.com',
            'passwd': '1%distance'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(url=domain + url, data=para)
        urllib2.urlopen(req)
        sign_url = '/user/checkin'
        req = urllib2.Request(url=domain + sign_url)
        req.add_header('Referer', 'https://www.ssccat.tk/user')
        req.add_header('X-Requested-With:', 'XMLHttpRequest')
        req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
        response = urllib2.urlopen(domain + sign_url)
        print response.read()


app = webapp2.WSGIApplication([('/daily', GXQDaily), ('/upload', Upload)], debug=True)

if Debug:
    from paste import httpserver
    def main():
        httpserver.serve(app, host='127.0.0.1', port='8081')

    if __name__ == '__main__':
        main()
