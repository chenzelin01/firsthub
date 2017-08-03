# -*- coding:utf-8 -*-

import urllib2, urllib
import httplib
import json
import chardet
import urlparse

API_KEY = 'AIzaSyAxCWOPF557vOj6_l5y0XWgdAWj5Gy_e-w'
Search_ID = '010323387921619221884:8rxddssqigi'
prototype = 'https://'
domain = 'www.googleapis.com'
# domain = 'www.google.com'
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
          'Accept': 'application/json, text/javascript, */*; q=0.01'}

def query(q_string, proxy='127.0.0.1:1080'):
    url = str.format('/customsearch/v1?q={0}&cx={1}&fields={2}&key={3}',
                     urllib.quote(q_string),
                     urllib.quote(Search_ID),
                     urllib.quote('items(title, snippet)'),
                     urllib.quote(API_KEY))
    resp_page1 = download(prototype + domain + url, proxy=proxy)
    url = str.format('/customsearch/v1?q={0}&cx={1}&fields={2}&key={3}&start={4}',
                     urllib.quote(q_string),
                     urllib.quote(Search_ID),
                     urllib.quote('items(title, snippet)'),
                     urllib.quote(API_KEY),
                     '10')
    resp_page2 = download(prototype + domain + url, proxy=proxy)
    resp_jsons = []
    resp_jsons.append(json.loads(resp_page1.replace('\n', ''), encoding='utf-8'))
    resp_jsons.append(json.loads(resp_page2.replace('\n', ''), encoding='utf-8'))

    def iter_items(response_jsons):
        for resp_json in resp_jsons:
            for item in resp_json['items']:
                yield item['title'], item['snippet']

    ret_list = list(iter_items(resp_jsons))
    return json.dumps(ret_list)

def download(url, params=None, user_agent='wswp', proxy=None, num_retries=2):
    print 'Downloading: ', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, data=params, headers=headers)
    # request.get_method = lambda: 'GET'
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
        # charset = chardet.detect(html)['encoding']
        # if charset == 'GB2312' or charset == 'gb2312':
        #     html = html.decode('GBK').encode('GB18030')
        # else:
        #     html = html.decode(charset).encode('GB18030')
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
        if num_retries > 0:
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # recursively retry 5xx HTTP errors
                    return download(url, user_agent, proxy, num_retries - 1)
    return html

if __name__=='__main__':
    print query('sysu')


