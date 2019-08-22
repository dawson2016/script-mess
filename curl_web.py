#!/usr/bin/env python3
#coding:utf-8
import urllib
import urllib.request
import re
def getHtml(url):
    req = urllib.request.Request(url,headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
})
    page=urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    return html
def getlink(html):
    reg = "：(?:\w+\-){1,3}\w+"
    reg1 = ".*"
    linkre = re.compile(reg)
    linklist = linkre.findall(html)
    return linklist         
html = getHtml("http://www.bidnews.cn/caigou/zhaobiao-2276652.html")
print (getlink(html))
#print (len(getlink(html)))

1024aa66942f3a1af317e25aa5c4a7a3
lizhijie
http://ad.smsadmin.cn/index.html
