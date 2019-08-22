#!/usr/bin/env python
#coding:utf-8
from __future__ import division
import xlsxwriter
import time
import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
server_info=[
['192.168.1.9',u'内网',u'比比测试',{'items':
{'cpu':['25042','24992','24990','24991'],
'mem':['25008','25033','24995','25034'],
'disk':['25027','25035','25036'],
'net':['24997','24996','25037','25038']}}],
['192.168.1.11',u'内网',u'比比测试c',{'items':
{'cpu':['25043','24935','24936','24934'],
'mem':['24986','25047','24943','25044'],
'disk':['25048','25049','25050'],
'net':['24942','24947','25051','25052']}}],
['192.168.1.13',u'内网',u'邮件服务器',{'items':
{'cpu':['25166','25151','25149','25150'],
'mem':['25157','25160','25154','25161'],
'disk':['25158','25162','25163'],
'net':['25156','25155','25164','25165']}}],
['192.168.1.14',u'内网',u'国企子系统',{'items':
{'cpu':['25148','25133','25131','25132'],
'mem':['25139','25142','25136','25143'],
'disk':['25140','25144','25145'],
'net':['25138','25137','25146','25147']}}],
['192.168.1.15',u'内网',u'监控平台',{'items':
{'cpu':['25094','25079','25077','25078'],
'mem':['25085','25088','25082','25089'],
'disk':['25167','25168','25169'],
'net':['25084','25083','25092','25093']}}],
['192.168.1.16',u'内网',u'SVN服务器',{'items':
{'cpu':['25067','25054','25055','25053'],
'mem':['25065','25071','25060','25068'],
'disk':['25072','25073','25074'],
'net':['25059','25064','25075','25076']}}],
['192.168.1.17',u'内网',u'数据库',{'items':
{'cpu':['25112','25097','25095','25096'],
'mem':['25103','25106','25100','25107'],
'disk':['25170','25171','25172'],
'net':['25102','25101','25110','25111']}}],
['192.168.1.18',u'内网',u'国企平台',{'items':
{'cpu':['25130','25115','25113','25114'],
'mem':['25121','25124','25118','25125'],
'disk':['25173','25174','25175'],
'net':['25120','25119','25128','25129']}}],
['192.168.10.2',u'外网',u'比比c端',{'items':
{'cpu':['25240','25227','25228','25226'],
'mem':['25238','25244','25233','25241'],
'disk':['25245','25246','25247'],
'net':['25232','25237','25248','25249']}}],
['192.168.10.3',u'外网',u'比比正式',{'items':
{'cpu':['25201','24909','24907','24908'],
'mem':['25011','25195','24911','25196'],
'disk':['25194','25197','25198'],
'net':['25199','25200','24917','24916']}}],
['192.168.10.4',u'外网',u'比比备份',{'items':
{'cpu':['25193','25178','25176','25177'],
'mem':['25184','25187','25181','25188'],
'disk':['25185','25189','25190'],
'net':['25183','25182','25191','25192']}}],
['221.204.241.2',u'外网',u'视频会议',{'items':
{'cpu':['25216','25203','25204','25202'],
'mem':['25214','25220','25209','25217'],
'disk':['25221','25222','25223'],
'net':['25208','25213','25224','25225']}}],
['192.168.10.11',u'外网',u'国企门户',{'items':
{'cpu':['25262','25252','25250','25251'],
'mem':['24242','25257','24811','24241'],
'disk':['25255','25257','25259'],
'net':['25254','25253','25260','25261']}}],
['192.168.10.12',u'外网',u'凯宾斯基',{'items':
{'cpu':['25279','25269','25267','25268'],
'mem':['25265','25274','25266','25264'],
'disk':['25272','25275','25276'],
'net':['25271','25270','25277','25278']}}],
['192.168.10.14',u'外网',u'金融运营测试',{'items':
{'cpu':['25296','25286','25284','25285'],
'mem':['25282','25291','25283','25281'],
'disk':['25289','25292','25293'],
'net':['25288','25287','25294','25295']}}],
['192.168.10.15',u'外网',u'邮件服务器',{'items':
{'cpu':['25381','25371','25369','25370'],
'mem':['25367','25376','25368','25366'],
'disk':['25374','25377','25378'],
'net':['25373','25372','25379','25380']}}],
['192.168.10.16',u'外网',u'数据库主',{'items':
{'cpu':['25313','25303','25301','25302'],
'mem':['25299','25308','25300','25298'],
'disk':['25306','25309','25310'],
'net':['25305','25304','25311','25312']}}],
['192.168.10.17',u'外网',u'数据库备',{'items':
{'cpu':['25330','25320','25318','25319'],
'mem':['25316','25325','25317','25315'],
'disk':['25323','25326','25327'],
'net':['25322','25321','25328','25329']}}],
['192.168.10.18',u'外网',u'各子系统',{'items':
{'cpu':['25347','25337','25335','25336'],
'mem':['25333','25342','25334','25332'],
'disk':['25340','25343','25344'],
'net':['25339','25338','25345','25346']}}],
['192.168.10.19',u'外网',u'国企金融运营',{'items':
{'cpu':['25364','25354','25352','25353'],
'mem':['25350','25359','25351','25349'],
'disk':['25357','25360','25361'],
'net':['25356','25355','25362','25363']}}]

]
def datalist(x):
    data=[]
    for i in range(len(x)):
        if x[i] > 1073741824:
            a=x[i]/1024/1024/1024
            b='%.2f' % a
            data.append(str(b)+'GB')
        elif x[i] > 1048576:
            a=x[i]/1024/1024
            b='%.2f' % a
            data.append(str(b)+'MB')
        elif x[i] > 1024:
            a=x[i]/1024
            b='%.2f' % a
            data.append(str(b)+'KB')
        else:
            return x   
    return data 
#主机以及WEB监控项ID写在字典里
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
subtitle=[u"指标", u"平均值" ,u"最小值" ,u"最大值"]
server=['ip',u'位置',u'用途']
cpu=[u'cpu使用率 %',u'cpu1分钟负载',u'cpu5分钟负载',u'cpu15分钟负载']
mem=[u'物理内存使用率 %',u'虚拟内存使用率 %',u'可用物理内存',u'已用物理内存']
disk=[u'工作分区使用率 %',u'工作分区总空间',u'工作分区可用空间','']
net=[u'出速度',u'入速度',u'出流量',u'入流量']
conn = MySQLdb.connect(host='localhost',user='zabbix',passwd='zabbix',db='zabbix')
cur = conn.cursor()
sql1="select value_avg,value_min,value_max from trends where itemid=%s order by clock desc limit 1"
sql2="select value_avg,value_min,value_max from trends_uint where itemid=%s order by clock desc limit 1"
with xlsxwriter.Workbook('server_state.xlsx') as workbook:
#定义excel单元格以及字体格式
    date_format=workbook.add_format({'num_format':'hh:mm:ss'})
    title_format = workbook.add_format({'bold': 1,'border': 1,'font_size':14,'align': 'center','valign': 'vcenter','fg_color': 'gray'})
    subtitle_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
    content_format = workbook.add_format({'border': 1,'align': 'center','valign': 'vcenter'})
    content_format.set_text_wrap()
    content1_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter'})
    content1_format.set_text_wrap()
    bold=workbook.add_format({'bold':True})
    worksheet = workbook.add_worksheet(u'服务器')
    worksheet.set_column('A:A',13)
    worksheet.merge_range('A1:S1', u'服务器性能状况', title_format)
    worksheet.merge_range('A2:C2', u'设备', title_format)
    worksheet.merge_range('D2:G2', u'CPU', title_format)
    worksheet.merge_range('H2:K2', u'内存', title_format)
    worksheet.merge_range('L2:O2', u'磁盘', title_format)
    worksheet.merge_range('P2:S2', u'网络', title_format)
    for i in range(len(server_info)):
        a=3+i*5
        cpuid=1
        for j in server_info[i][3]['items']['cpu']:
                if cur.execute(sql1,j)==0:
                    cur.execute(sql2,j)
                cpulist=datalist(list(cur.fetchall()[0]))
                worksheet.write_row('E'+str(a+cpuid),cpulist,content_format)
                cpuid+=1
        memid=1        
        for j in server_info[i][3]['items']['mem']:
                if cur.execute(sql1,j)==0:
                    cur.execute(sql2,j)
                memlist=datalist(list(cur.fetchall()[0]))
                worksheet.write_row('I'+str(a+memid),memlist,content_format)
                memid+=1
        diskid=1
        for j in server_info[i][3]['items']['disk']:
                if cur.execute(sql1,j)==0:
                    cur.execute(sql2,j)
                disklist=datalist(list(cur.fetchall()[0]))
                worksheet.write_row('M'+str(a+diskid),disklist,content_format)
                diskid+=1
        netid=1
        for j in server_info[i][3]['items']['net']:
                if cur.execute(sql1,j)==0:
                    cur.execute(sql2,j)
                netlist=datalist(list(cur.fetchall()[0]))
                worksheet.write_row('Q'+str(a+netid),netlist,content_format)
                netid+=1
        worksheet.write_row('A'+str(a),server,subtitle_format)
        worksheet.merge_range('A'+str(a+1)+':'+'A'+str(a+4),server_info[i][0],content_format)
        worksheet.merge_range('B'+str(a+1)+':'+'B'+str(a+4),server_info[i][1],content_format)
        worksheet.merge_range('C'+str(a+1)+':'+'C'+str(a+4),server_info[i][2],content_format)
        worksheet.write_row('D'+str(a),subtitle,subtitle_format)
        worksheet.write_row('H'+str(a),subtitle,subtitle_format)
        worksheet.write_row('L'+str(a),subtitle,subtitle_format)
        worksheet.write_row('P'+str(a),subtitle,subtitle_format)
        worksheet.write_column('D'+str(a+1),cpu,content1_format)
        worksheet.write_column('H'+str(a+1),mem,content1_format)
        worksheet.write_column('L'+str(a+1),disk,content1_format)
        worksheet.write_column('P'+str(a+1),net,content1_format)
workbook.close()
