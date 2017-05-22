# -*- coding:utf-8 -*-
import webapp2
import urllib2
import urllib
import time
import json
import cookielib
html = """
<!DOCTYPE>
<html>
<head>
<meta id="viewport" name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<meta name="MobileOptimized" content="320"/>
<title>触屏特效,手机网页</title>
<style type="text/css">
    html{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}
    body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,textarea,p,blockquote,th,td,hr,button,article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section {margin:0;padding:0;}
    .dragme{background:#000;width:60px;height:60px; color:#fff; position:absolute; left:40px; top:40px; text-align:center; line-height:60px;}
</style>
<script type="text/javascript" src="https://code.jquery.com/jquery-latest.js"></script>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
</head>
<body>
<div id="moveid" class="dragme">
    lvtao.net
</div>
<script type="text/javascript">
var isdrag=false;
var tx,x,ty,y;
$(function(){
    document.getElementById("moveid").addEventListener('touchstart',touchStart);
    document.getElementById("moveid").addEventListener('touchmove',touchMove);
	document.getElementById("moveid").addEventListener('touchend',function(){
        isdrag = false;
    });
});
function touchStart(e){
   isdrag = true;
   e.preventDefault();
   tx = parseInt($("#moveid").css('left'));
   ty = parseInt($("#moveid").css('top'));
   x = e.touches[0].pageX;
   y = e.touches[0].pageY;
}
function touchMove(e){
  if (isdrag){
   e.preventDefault();
	   var n = tx + e.touches[0].pageX - x;
	   var h = ty + e.touches[0].pageY - y;
	   $("#moveid").css("left",n);
	   $("#moveid").css("top",h);
   }
}
</script>
</body>
</html>
"""
Debug = False
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        get = self.request.GET
        try:
            if len(get) is 0:
                self.response.write(html)
            else:
                self.response.write('You sent ' + get['s'] + ' which was ' + str(len(get['s'])) + ' length.')
        except:
            self.response.write("")

class GXQDaily(webapp2.RedirectHandler):
    def __init__(self):
        self.sid = None

    def get(self):
        self.sid = self.get_gxq_sid()
        file = self.gxq_gold() + self.gxq_ice()
        # file = self.yooli()
        self.response.write(file)

    def gxq_gold(self):
        if self.sid is None:
            self.sid = self.get_gxq_sid()
        # gold cron
        domain = "http://fjwebs.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': self.sid,
            'version': '1.1.0',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(domain + url, para)
        reponse = urllib2.urlopen(req)
        file = reponse.read()
        return file

    def gxq_ice(self):
        if self.sid is None:
            self.sid = self.get_gxq_sid()
        # ice cron
        domain = "http://appweb.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': self.sid,
            'version': '5.0.0',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(url=domain + url, data=para)
        reponse = urllib2.urlopen(req)
        file = reponse.read()
        return file
    def yooli(self):
        # yooli.com cron
        domain = "http://app.yooli.com/"
        url = "app3.0/core/add/user/sign+points"
        para = {
            'sign': 'true',
            'ui': '2311358',
            'tm': str(int(time.time())),
            'nc': '3540a6',
            'di': '05c07a213fd11bd2d20064fb97ed8940',
            'mt': '3',
            'v': '200705',
            'ost': '20',
            'channelId': '%E5%BA%94%E7%94%A8%E5%AE%9D%C2%B7%E8%85%BE%E8%AE%AF%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0',
            'sid': '417',
            'dn': 'HUAWEI+HUAWEI+GRA-TL00',
            'sh': '1794',
            'sw': '1080',
            'ss': '3.0',
            'osv': '5.0.1+android-29of40',
            'si': '40023142896f816b3714cc3441b621e7e530a45b'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(url=domain + url, data=para)
        reponse = urllib2.urlopen(req)
        file = reponse.read()
        return file

    def get_gxq_sid(self):
        domain = "https://passport.jinfuzi.com"
        url = "/service/login"
        para = {
            "account": "18819461475",
            "c_business": '2',
            "c_channel": 'fj0update',
            "c_identity": '53148d584290a7d5364e189882c648d2',
            "c_mmodel": 'HUAWEI GRA-TL00',
            "c_network": 'wifi',
            "c_platform": '2',
            "c_sysVer": '5.0.1',
            "c_version": '1.1.0',
            "password": '1995023czl!!',
            "sign": '49e04a8f86e1e97791dd26620de3ef89',
            "type": '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(url=domain + url, data=para)
        reponse = urllib2.urlopen(req)
        file = json.load(reponse)
        return file['res']['data']['sid']

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


app = webapp2.WSGIApplication([('/', HelloWebapp2), ('/daily', GXQDaily)], debug=True)

if Debug:
    from paste import httpserver
    def main():
        httpserver.serve(app, host='127.0.0.1', port='8080')

    if __name__ == '__main__':
        GXQDaily().ssccat_login()
