#!/usr/bin/env python
#coding:utf-8
import top.api
import sys
import json
req=top.api.AlibabaAliqinFcSmsNumSendRequest()
appkey='23354326'
secret='b84cb77a7f188db7a8edffa3a65b030d'
#data=str(sys.argv[3]).split(',')
data=['221-204-173-163problem','外网防火墙','0','0','0','net down','不通']
para={'status':data[0],'name':data[1],'host':data[2],'ip':data[3],'date':data[4],'item':data[5],'value':data[6]}
req.set_app_info(top.appinfo(appkey,secret)) 
req.extend="123456"
req.sms_type="normal"
req.sms_free_sign_name="比比网络"
req.sms_param=json.dumps(para)
req.rec_num="13633445821,13834694519,13111077788,18634356784,13934572752"
#req.rec_num="13633445821"
req.sms_template_code="SMS_8901531"
try:
    resp= req.getResponse()
    print(resp)
except Exception,e:
    print(e)
