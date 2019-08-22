#!/usr/bin/env python
#coding:utf-8
#realtime time log
import time
import redis
import json
import urllib2
import re
import subprocess
rc = redis.Redis(host='192.168.10.4',port=6379,password='redis123456')
regex = re.compile(r'\\(?![/u"])')
def pat(text):
    sub="/"
    sub1="ggWeb"
    sub2="home"
    sub3="login"
    sub4="news"
    sub5="aboutus"
    sub6="memberinfo"
    sub7="search" 
    if text=="/":
        return u'主页'
    elif re.findall(sub1,text)!=[]:
        return u'招标公告'
    elif re.findall(sub2,text)!=[]:
        return u'首页'
    elif re.findall(sub3,text)!=[]:
        return u'登陆'
    elif re.findall(sub4,text)!=[]:
        return u'新闻咨询'
    elif re.findall(sub5,text)!=[]:
        return u'关于平台'
    elif re.findall(sub6,text)!=[]:
        return u'会员须知'
    elif re.findall(sub7,text)!=[]:
        return u'搜索'
    else:
        return u'其他'
def sinaip(ip):
        url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip='+ip
        postdata = urllib2.urlopen(url).read()
        jsondata = json.loads(postdata)
        if jsondata['ret'] != -1:
            city = jsondata['city']
            if jsondata['city']=="":
		city=u'未知'
        else:
            city=u'北京' 
        return  city
def baiduip(ip):
        url='http://api.map.baidu.com/location/ip?ak=25GZBvp4LQ4feQ3HASGDtZv8pu8Br8hj&ip='+ip
        postdata = urllib2.urlopen(url).read()
        jsondata = json.loads(postdata)
        info = []
        if jsondata[u'status']==0 and jsondata[u'content'][u'address_detail'][u'city'][:-1]!='':
        	province=jsondata[u'address'].split('|')[1]
                city=jsondata[u'content'][u'address_detail'][u'city']
                if len(city)<=4:
        	    city=city[:-1]
                else:
                    city=city[:2]
        	isp=jsondata[u'address'].split('|')[4]
                if isp == 'UNICOM':
                	isp=u'联通'
                elif isp == 'CHINANET':
			isp=u'电信'
                elif isp == 'ALIBABA':
			isp=u'阿里巴巴'
                elif isp == 'TENCENT':
			isp=u'腾讯网络'
                elif isp == 'CMNET':
			isp=u'移动'
                elif isp == 'OTHER':
			isp=u'其他'
        	info.extend([province,city,isp])
        	return info
	else:
		return [u'\u5c71\u897f', u'\u592a\u539f', u'\u8054\u901a']
def aliip(ip):
    if ip=='202.99.212.204':
        return [u'\u5c71\u897f\u7701', u'\u592a\u539f', u'\u8054\u901a']
    else:
        url='http://ip.taobao.com/service/getIpInfo.php?ip='+ip   
        postdata = urllib2.urlopen(url).read()
        jsondata = json.loads(postdata)
        info = []
        if jsondata['code'] == 0 or jsondata['data']['city'][:-1]!=u'':
            region = jsondata['data']['region']
            info.extend([province,city,isp])
            return info
	else:
            return [u'\u5c71\u897f', u'\u592a\u539f', u'\u8054\u901a']

f1 = open("/usr/local/nginx/logs/access.log", "r")
popen = subprocess.Popen('cat /usr/local/nginx/logs/access.log|egrep -iv \'\"cookie\": \"\"|\"cookie\": \"-\"|spider|202.99.212.204|home!getTZ.action\'|wc -l', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
count=int(popen.stdout.readline().strip())
print count 
popen1 = subprocess.Popen('tail -f /usr/local/nginx/logs/access.log', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#popen1 = subprocess.Popen('tail -f /usr/local/nginx/logs/access.log|egrep -iv \'\"cookie\": \"\"|\"cookie\": \"-\"|spider|home!getTZ.action\'', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
while True:
    line=popen1.stdout.readline().strip()
    if line:
        #print line
        line = regex.sub(r"\\\\",line)
        line=json.loads(line)
        count+=1
        line["count"]=count
        #print baiduip(line["ipaddr"]),pat(line["url"]),line["count"]
        rc.publish("fm110",[baiduip(line["ipaddr"]),pat(line["url"]),line["count"]])
