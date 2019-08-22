#!/usr/bin/env python 
#-*-encoding:utf-8-*-
import xlsxwriter
import time
file_list=[['name1','1','1','1','1','1','1','1','1','1'],['name2','3','2','2','2','2','2','2','2','2'],['name3','3','3','3','3','3','3','3','3','3']]
#主机以及WEB监控项ID写在字典里
date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
with xlsxwriter.Workbook('getexcel_test.xlsx') as workbook:
#定义excel单元格以及字体格式
    date_format=workbook.add_format({'num_format':'hh:mm:ss'})
    okcolor_format=workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','bg_color':'98FB98'})
    errcolor_format=workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter','bg_color':'CD2626'})
    merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
    per_format = workbook.add_format({'num_format': '0.00%'})
    num_format = workbook.add_format({'num_format': '#,##0.00'})
    bold=workbook.add_format({'bold':True})
#开始编写web工作表
    worksheet = workbook.add_worksheet('class-1')
    worksheet.set_column('A:M', 13)
    worksheet.set_row(0,30)
    worksheet.set_row(1,20)
    worksheet.merge_range('A1:N1', date_time+u'class-n', merge_format)
    worksheet.write('A2',u'name', merge_format)
    worksheet.write('B2',u'chn', merge_format)
    worksheet.write('C2',u'mat', merge_format)
    worksheet.write('D2',u'eng', merge_format)
    worksheet.write('E2',u'his', merge_format)
    worksheet.write('F2',u'geo', merge_format)
    worksheet.write('G2',u'pol', merge_format)
    worksheet.write('H2',u'phy', merge_format)
    worksheet.write('I2',u'che', merge_format)
    worksheet.write('J2',u'bio', merge_format)
    worksheet.write('K2',u'sumgoal', merge_format)
    worksheet.write('L2',u'avgoal', merge_format)
    worksheet.write('M2',u'test_rank', merge_format)
    worksheet.write('N2',u'other', merge_format)
    worksheet.write('A'+str(len(file_list)+4),u'section1', merge_format)
    worksheet.write('A'+str(len(file_list)+5),u'section2', merge_format)
    worksheet.write('A'+str(len(file_list)+6),u'section3', merge_format)
    worksheet.write('A'+str(len(file_list)+7),u'section4', merge_format)
    worksheet.write('A'+str(len(file_list)+8),u'section5', merge_format)
    worksheet.write('A'+str(len(file_list)+10),u'passper', merge_format)
#从数组取值
    for i in range(len(file_list[0])):
        data=[]
        for j in range(len(file_list)):
            if i!=0:
                data.append(int(file_list[j][i]))
            else:
                data.append(file_list[j][i])
        worksheet.write_column(chr(65+i)+'3',data)
        if i>=1:
            interv1='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',"<=100",'+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=90")'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+4),interv1)
            interv2='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',"<90",'+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=80")'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+5),interv2)
            interv3='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',"<80",'+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=70")'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+6),interv3)
            interv4='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',"<70",'+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=60")'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+7),interv4)
            interv5='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',"<=60",'+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=0")'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+8),interv5)
            passper='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+',">=60")/COUNT('+chr(65+i)+'3:'+chr(65+i)+str(len(file_list)+3)+')'
            worksheet.write_formula(chr(65+i)+str(len(file_list)+10),passper,per_format)
           
    for k in range(len(file_list)):
        sum1='K'+str(k+3)
        sum2='=SUM(B'+str(k+3)+':'+'J'+str(k+3)+')'
        ave1='L'+str(k+3)
        ave2='=AVERAGE(B'+str(k+3)+':'+'J'+str(k+3)+')'
        ran1='M'+str(k+3)
        ran2='=_xlfn.RANK.EQ(L'+str(k+3)+','+'L3'+':'+'L'+str(len(file_list)+3)+')'
        worksheet.write_formula(sum1,sum2)
        worksheet.write_formula(ave1,ave2,num_format)
        worksheet.write_formula(ran1,ran2)
   
workbook.close()
