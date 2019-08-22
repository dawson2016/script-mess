#!/usr/bin/env python
#coding=utf-8
import sys
from prettytable import PrettyTable
while 1:
    flag=0
    try:
        salary=input('请输入您的工资:  ')
    except Exception,e:
        print '输入有误'
        flag=1
    if flag==1:
        continue
    else:
        break
print '\033[31;1m%s\033[0m' % '欢迎进入电子商城'
l1=['1','MP3',500,999]
l2=['2','相机',1000,999]
l3=['3','手机',3000,999]
l4=['4','电脑',4000,999]
def list():
    x = PrettyTable(["ID","商品", "价格", "库存" ])
    x.add_row(l1)
    x.add_row(l2)
    x.add_row(l3)
    x.add_row(l4)
    print x
menu={'1':l1,'2':l2,'3':l3,'4':l4}
choiceid=[]
pay=[]
def  paylist():
    x = PrettyTable(["商品", "价格", "数量"])
    for i in pay: 
        x.add_row(i)
    print x
while 1:
    list()
    while 1:
        action=raw_input('(s):购物,(q):退出,(c):继续 请选择: ')
        if action=='s' or action=='c':
            break
        elif  action=='q':
            sys.exit()
        else:
            print '请输入你的选择: '
            continue
    try:
        choice=raw_input('请输入购买物品的ID ：')
        number=input('请输入您要购买的件数：')
    except Exception,e:
        print '输入有误'
    if choice in menu.keys() and number<=menu[choice][3]:
        print '您将要购买的商品是%s件%s,总共花费%s元'%(number,menu[choice][1],menu[choice][2]*number)
    else:
        print'您的输入有误，请重新输入商品ID以及购买件数'
        continue
    confirm=raw_input('确认付款请按y,否则请按n；你的选择是: ')
    if confirm=='y':
        salary-=menu[choice][2]*number
        if salary <0:
            print '你的余额不足,支付失败! 请重新选择或者退出'
        else:
            print '已添加到已购物品清单'
            menu[choice][3]-=number
            choiceid.append(menu[choice][1])
            choiceid.append(menu[choice][2])
            choiceid.append(number)
            pay.insert(0,choiceid)
            choiceid=[]
            paylist()
            print '您的余额是%s'%salary
        if salary==0:
            print '您已无力购买任何物品，系统自动退出!'
            sys.exit()
    else:
        continue
