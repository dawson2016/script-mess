#coding:utf-8
import xlsxwriter
import time
from Tkinter import *
root=Tk()
root.title("自动生成excel小程序  Author:Dawson 16/3/28")
root.geometry('500x400')    
Label(root,text='姓名:',width=10).grid(row=0,column=0)
Label(root,text='语文:').grid(row=1,column=0)
Label(root,text='数学:').grid(row=2,column=0)
Label(root,text='英语:').grid(row=3,column=0)
Label(root,text='历史:').grid(row=4,column=0)
Label(root,text='地理:').grid(row=5,column=0)
Label(root,text='政治:').grid(row=6,column=0)
Label(root,text='物理:').grid(row=7,column=0)
Label(root,text='化学:').grid(row=8,column=0)
Label(root,text='生物:').grid(row=9,column=0)
Label(root,text='*默认将以当前日期为文件名生成.xlsx后缀文件',bg="red").grid(row=11,column=1,padx=10,pady=5)
name=StringVar()
e1=Entry(root,textvariable=name)
e1.grid(row=0,column=1,padx=10,pady=5)
yuwen=StringVar()
e2=Entry(root,textvariable=yuwen)
e2.grid(row=1,column=1,padx=10,pady=5)
shuxue=StringVar()
e3=Entry(root,textvariable=shuxue)
e3.grid(row=2,column=1,padx=10,pady=5)
yingyu=StringVar()
e4=Entry(root,textvariable=yingyu)
e4.grid(row=3,column=1,padx=10,pady=5)
lishi=StringVar()
e5=Entry(root,textvariable=lishi)
e5.grid(row=4,column=1,padx=10,pady=5)
dili=StringVar()
e6=Entry(root,textvariable=dili)
e6.grid(row=5,column=1,padx=10,pady=5)
zhengzhi=StringVar()
e7=Entry(root,textvariable=zhengzhi)
e7.grid(row=6,column=1,padx=10,pady=5)
wuli=StringVar()
e8=Entry(root,textvariable=wuli)
e8.grid(row=7,column=1,padx=10,pady=5)
huaxue=StringVar()
e9=Entry(root,textvariable=huaxue)
e9.grid(row=8,column=1,padx=10,pady=5)
shengwu=StringVar()
e10=Entry(root,textvariable=shengwu)
e10.grid(row=9,column=1,padx=10,pady=5)
a=[]
def show():
    global a
    if name.get()!='':
        a.append([name.get(),yuwen.get(),shuxue.get(),yingyu.get(),lishi.get(),dili.get()\
              ,zhengzhi.get(),wuli.get(),huaxue.get(),shengwu.get()])
    print a
def conti():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    e7.delete(0,END)
    e8.delete(0,END)
    e9.delete(0,END)
    e10.delete(0,END)

Button(root,text='提交输入',width=14,bg="grey",command=show)\
       .grid(row=10,column=0,padx=10,pady=5)
Button(root,text='清空继续',width=10,bg="grey",command=conti)\
       .grid(row=10,column=1,padx=10,pady=5)
def excel():
    workbook = xlsxwriter.Workbook(time.strftime("%Y.%m.%d")+'.xlsx')
    #定义excel单元格以及字体格式
    date_format=workbook.add_format({'num_format':'hh:mm:ss'})
    okcolor_format=workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','bg_color':'98FB98'})
    errcolor_format=workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter','bg_color':'CD2626'})
    merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
    per_format = workbook.add_format({'num_format': '0.00%'})
    num_format = workbook.add_format({'num_format': '#,##0.00'})
    bold=workbook.add_format({'bold':True})
    date_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
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
    worksheet.write('A'+str(len(a)+4),u'section1', merge_format)
    worksheet.write('A'+str(len(a)+5),u'section2', merge_format)
    worksheet.write('A'+str(len(a)+6),u'section3', merge_format)
    worksheet.write('A'+str(len(a)+7),u'section4', merge_format)
    worksheet.write('A'+str(len(a)+8),u'section5', merge_format)
    worksheet.write('A'+str(len(a)+10),u'passper', merge_format)
#从数组取值
    for i in range(len(a[0])):
        data=[]
        for j in range(len(a)):
            if i!=0:
                data.append(int(a[j][i]))
            else:
                data.append(a[j][i])
        worksheet.write_column(chr(65+i)+'3',data)
        if i>=1:
            interv1='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',"<=100",'+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=90")'
            worksheet.write_formula(chr(65+i)+str(len(a)+4),interv1)
            interv2='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',"<90",'+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=80")'
            worksheet.write_formula(chr(65+i)+str(len(a)+5),interv2)
            interv3='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',"<80",'+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=70")'
            worksheet.write_formula(chr(65+i)+str(len(a)+6),interv3)
            interv4='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',"<70",'+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=60")'
            worksheet.write_formula(chr(65+i)+str(len(a)+7),interv4)
            interv5='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',"<=60",'+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=0")'
            worksheet.write_formula(chr(65+i)+str(len(a)+8),interv5)
            passper='=_xlfn.COUNTIFS('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+',">=60")/COUNT('+chr(65+i)+'3:'+chr(65+i)+str(len(a)+3)+')'
            worksheet.write_formula(chr(65+i)+str(len(a)+10),passper,per_format)
           
    for k in range(len(a)):
        sum1='K'+str(k+3)
        sum2='=SUM(B'+str(k+3)+':'+'J'+str(k+3)+')'
        ave1='L'+str(k+3)
        ave2='=AVERAGE(B'+str(k+3)+':'+'J'+str(k+3)+')'
        ran1='M'+str(k+3)
        ran2='=_xlfn.RANK.EQ(L'+str(k+3)+','+'L3'+':'+'L'+str(len(a)+3)+')'
        worksheet.write_formula(sum1,sum2)
        worksheet.write_formula(ave1,ave2,num_format)
        worksheet.write_formula(ran1,ran2)
    workbook.close()

Button(root,text='生成excel',width=10,bg="grey",command=excel)\
       .grid(row=10,column=2,padx=10,pady=5)


root.mainloop()
