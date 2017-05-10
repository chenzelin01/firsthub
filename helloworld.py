# -*- coding:utf-8 -*-
import webapp2
import gensim
from paste import httpserver

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

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        get = self.request.GET
        try:
            if len(get) is 0:
                self.response.write(html)
            else:
                # self.response.write('You sent ' + get['s'] + ' which was ' + str(len(get['s'])) + ' length.')
                words = compute_sim(get['s'])
                if words is None:
                    self.response.write("the word " + get['s'] + " does not conclude in the data set")
                else:
                    self.response.write("the similar word of " + get['s'] + " is \n" + words)
        except:
            self.response.write("")
def compute_sim(word):
    try:
        m = gensim.models.Word2Vec.load('model')
        words = m.most_similar_cosmul(word)
    except KeyError:
        words = None
    return words

app = webapp2.WSGIApplication([('/', HelloWebapp2)], debug=True)

def main():
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
