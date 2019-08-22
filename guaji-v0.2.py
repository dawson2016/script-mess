#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:dawson
from Tkinter import *
from tkMessageBox import *
import requests
import threading
import time
import json
import random
import base64
import os
from icon import img
reload(sys)
sys.setdefaultencoding( "utf-8" )
wxkc=[]
userlist=[]
def btn_submit():
	#获取信息
	yhm=entry_id.get()
	headers = {'content-type': 'text/json','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}
	cookies={'ASP.NET_SessionId':'ji4zk1yzsv1jwvhubwrewect'}	
	url='http://yqgbpx.cn/yonghu.svc/Login'
	data={"yhm":yhm,"mima":"","yanzhengma":"0683","yanzhengmamd5":"8756026CFC20EA25CB630F95D80C48D9"}
	r = requests.post(url,headers=headers,data=json.dumps(data),cookies=cookies)
	userinfo=json.loads(r.text)['d']
	url1='http://yqgbpx.cn/xuexiindex.svc/SelectYonghuxuexiqingkuang_simple'
	name=userinfo['Xingming']
	dwid=userinfo['DanweiId']
	if dwid!=820:
		showerror("提示：", "对不起,非指定单位用户！！")
		app.destroy()
	data={"yhid":userinfo['Yhid']}
	userlist.append(userinfo['Yhid'])
	userlist.append(userinfo['Yhid'])
	r = requests.post(url1,headers=headers,data=json.dumps(data),cookies=cookies)
	infolist=json.loads(r.text)['d'][0]	
	lbl_kcjd = Label(app, text='姓名: '+name+' 已学习课程数：'+str(infolist["m_Item2"])+' 已学习分钟数：'+str(infolist["m_Item3"])+' 已获得学分数：'+str(infolist["m_Item4"]))
	lbl_kcjd.grid(row=1, column=1)	
	url2='http://yqgbpx.cn/xuexiindex.svc/Selectyonghuxuexikecheng'
	data={"yhid":userinfo['Yhid'],"changshangId":-1,"kechengmc":"","zhujiangren":"","zhuantiId":-1,"pageIndex":1,"pageSize":10}
	r = requests.post(url2,headers=headers,data=json.dumps(data),cookies=cookies)
	s=r.text
	count=0
	for i in json.loads(s)['d']:
		wxkc.append([i["ChangshangkechengId"],i["Shichang"]])
		btn_method = Checkbutton(fm1, variable = v,onvalue=count, text='课程名称: '+str(i["KechengMc"])+' 课程时长: '+str(i["Shichang"])+' 课程ID: '+str(i["ChangshangkechengId"]), command = callCheckbutton)
		btn_method.grid(row=count, column=0, sticky=W, padx=1)
		count+=1

def listen(yhid,kcid,mytime):
	session_time="00:00:"+str(mytime)
	if mytime==60:
		session_time="00:01:00"
	lsurl='http://www.yqgbpx.cn:81/Scorm12.svc/LMSCommit'
	headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}
	lscookies={"ASP.NET_SessionId":"uyomaapuhy2wdqwe2zgx30zz","InitilizeParam":"kehuId=200&yhId=1018187&kechengId=100021&op=10&shichang=125&xuexizhuangtai=0&lesson_location=&url=index.htm&host=www.yqgbpx.cn&ziyuanleixingid=10","currentState":"lastErrorCode=0&bInitilized=1&bCommitted=0","currentdata":"kehuid=200&student_id=1018187&student_name=&kechengid=100021&scoid=&session_time=00:00:01&lesson_location=704&lesson_status=incomplete&entry=ab-initio&scoreraw=&exit=&credit=no-credit&total_time=0:0:0&lesson_mode=normal&xuexizhuangtai=0&Totaltime=0","currentdata1":""}
	lgdata={"obj":{"KehuId":"200","Yhid":yhid,"KechengId":kcid,"Scoid":"","session_time":session_time,"Lesson_location":"704","Lesson_status":"incomplete","Entry":"ab-initio","Scoreraw":"","Lesson_mode":"normal","Exit":"","Suspend_data":"","Totaltime":"0"}}
	r = requests.post(lsurl,cookies=lscookies,headers=headers,data=json.dumps(lgdata))
 		
def gjcore():
	yhid=userlist[0]
	kcid=str(wxkc[v.get()][0])
	count=0
	var.set('正在挂机: ')
	while True:
		mytime=random.randint(20, 60)
		listen(yhid,kcid,mytime)
		time.sleep(mytime)
		count+=mytime
		var.set('已挂机: '+str(count)+' 秒--共计:'+str(count/60)+' 分钟')			
		if count>=int(wxkc[v.get()][1])*60:
			break
	var.set('所选课程已全部听完')
def guaji():
	th=threading.Thread(target=gjcore)
	th.setDaemon(True)
	th.start()	
	
#####创建窗口#####
app = Tk()
app.title("挂机软件v0.2 指定单位免费版  作者 --Dawson")
tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
app.iconbitmap("tmp.ico")
os.remove("tmp.ico")
#####创建控件#####
#第一行 地址
lbl_id = Label(app, text="请输入用户名:")
lbl_id.grid(row=0,sticky=E)
yhid=StringVar()
entry_id = Entry(app,textvariable=yhid)
entry_id.grid(row=0, column=2)
lbl_id = Label(app, text="请输入密码:")
lbl_id.grid(row=0,column=3,sticky=E)
entry_mm = Entry(app,show = '*')
entry_mm.grid(row=0, column=4)
btn_submit = Button(app, text="获取用户及课程信息",command=btn_submit)
btn_submit.grid(row=0, column=5)
#展示课程信息
lbl_kcxx = Label(app, text="个人信息:")
lbl_kcxx.grid(row=1, column=0,sticky=W)

#选择课程
lbl_xzkc = Label(app, text="未学习课程：")
lbl_xzkc.grid(row=2, column=0, sticky=W)
fm1 = Frame()
fm1.grid(row=2, column=1, sticky=W)
v = IntVar()
def callCheckbutton():
    lbl_kclb = Label(app, text='所选课程id为')
    lbl_kclb.grid(row=4, column=0, sticky=W, pady=1, padx=1)
    lbl_kclb = Label(app, text=str(wxkc[v.get()][0]))
    lbl_kclb.grid(row=4, column=1, sticky=W, pady=1, padx=1)
    return v.get()

#挂机按钮
btn_guaji = Button(app, text="开始挂机",command=guaji)
btn_guaji.grid(row=5, column=1, sticky=W, padx=5,pady=10)
lbl_gj = Label(app, text='挂机进度: ')
lbl_gj.grid(row=6, column=0, sticky=W, pady=1, padx=1)	
var=StringVar()
var.set(' ')	
lbl_gjsj = Label(app,textvariable=var)
lbl_gjsj.grid(row=7, column=0, sticky=W, pady=1, padx=1)
lbl_id = Label(app, text="Tip:①请联网使用！一次只展示10条未听课程   ")
lbl_id.grid(row=8 )
lbl_id = Label(app, text="②默认勾选不生效,须选择一个课程            ")
lbl_id.grid(row=9 )
lbl_id = Label(app, text="③界面出现所选课程id后即可挂机             ")
lbl_id.grid(row=10)
lbl_id = Label(app, text="④听完可登陆浏览器确定进度并答题           ")
lbl_id.grid(row=11)
lbl_id = Label(app, text="⑤界面画风请忽略,保证无毒无害,放心使用     ")
lbl_id.grid(row=12)
lbl_id = Label(app, text="⑥低调使用,毕竟非正规,且挂且珍惜           ")
lbl_id.grid(row=13)
lbl_id = Label(app, text="⑦免费版本不开启如自动听课等变态功能       ")
lbl_id.grid(row=14)
app.mainloop()

