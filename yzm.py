#!/usr/bin/env python
#coding:utf-8
import requests
import time
import json
import random
url='http://www.yqgbpx.cn:81/Scorm12.svc/LMSCommit'
headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}
cookies={"ASP.NET_SessionId":"uyomaapuhy2wdqwe2zgx30zz","InitilizeParam":"kehuId=200&yhId=1018187&kechengId=100021&op=10&shichang=125&xuexizhuangtai=0&lesson_location=&url=index.htm&host=www.yqgbpx.cn&ziyuanleixingid=10","currentState":"lastErrorCode=0&bInitilized=1&bCommitted=0","currentdata":"kehuid=200&student_id=1018187&student_name=&kechengid=100021&scoid=&session_time=00:00:01&lesson_location=704&lesson_status=incomplete&entry=ab-initio&scoreraw=&exit=&credit=no-credit&total_time=0:0:0&lesson_mode=normal&xuexizhuangtai=0&Totaltime=0","currentdata1":""}
lgdata={"obj":{"KehuId":"200","Yhid":"1018187","KechengId":"100021","Scoid":"","session_time":"00:01:00","Lesson_location":"704","Lesson_status":"incomplete","Entry":"ab-initio","Scoreraw":"","Lesson_mode":"normal","Exit":"","Suspend_data":"","Totaltime":"0"}}
count = 0
def px(mytime):
    session_time="00:00:"+str(mytime)
    if mytime==60:
	    session_time="00:01:00"
    lgdata={"obj":{"KehuId":"200","Yhid":"1018187","KechengId":"100089","Scoid":"","session_time":session_time,"Lesson_location":"704","Lesson_status":"incomplete","Entry":"ab-initio","Scoreraw":"","Lesson_mode":"normal","Exit":"","Suspend_data":"","Totaltime":"0"}}
    r = requests.post(url,cookies=cookies,headers=headers,data=json.dumps(lgdata))
    print r.content
while True:
    mytime=random.randint(20, 60)
    time.sleep(mytime)
    count+=mytime
    px(mytime)
    print count
    if count>=7200:
        break
