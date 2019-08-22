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
    worksheet = workbook.add_worksheet()
    data = a
    for i in range(len(data[0])):
        col=[]
        for j in range(len(data)):
            col.append(data[j][i])
        worksheet.write_column(chr(65+i)+'1',col)
    workbook.close()

Button(root,text='生成excel',width=10,bg="grey",command=excel)\
       .grid(row=10,column=2,padx=10,pady=5)


root.mainloop()
