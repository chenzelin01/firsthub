# -*- coding:utf-8 -*-
import webapp2
from paste import httpserver
import urllib2
import urllib
import time
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
Debug = True
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
    def get(self):
        file = self.gxq_gold() + self.gxq_ice()
        # file = self.yooli()
        if Debug:
            self.response.write(file)

    def gxq_gold(self):
        # gold cron
        domain = "http://fjwebs.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': 'cb8c17b1f4a24b2a13bc7f74b67522ea',
            'version': '1.1.0',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(domain + url, para)
        reponse = urllib2.urlopen(req)
        if Debug:
            file = reponse.read()
            return file

    def gxq_ice(self):
        # ice cron
        domain = "http://appweb.gxq168.com"
        url = "/act/sign/signup"
        para = {
            'uid': '2222799943',
            'sid': 'd0298051f48f40f65bdc481fa88f7b3e',
            'version': '5.0.0',
            'type': '1'
        }
        para = urllib.urlencode(para)
        req = urllib2.Request(domain + url, para)
        reponse = urllib2.urlopen(req)
        if Debug:
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
        req = urllib2.Request(domain + url, para)
        reponse = urllib2.urlopen(req)
        if Debug:
            file = reponse.read()
            return file
app = webapp2.WSGIApplication([('/', HelloWebapp2), ('/daily', GXQDaily)], debug=True)

if Debug:
    def main():
        httpserver.serve(app, host='127.0.0.1', port='8080')

    if __name__ == '__main__':
        main()
