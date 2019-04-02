#!/usr/bin/env python
#coding=utf-8
#author:dawson
import subprocess
import socket
import re
from prettytable import PrettyTable
localip=socket.gethostbyname(socket.gethostname())
def checkip(ip):  
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False
def maxport():
    cat = subprocess.Popen(["cat","/etc/sysconfig/iptables"],stdout=subprocess.PIPE)
    grep = subprocess.Popen(["grep","-i","PREROUTING"],stdin=cat.stdout,stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk","-F","[' ',:]+","{print $10,$14,$15}"],stdin=grep.stdout,stdout=subprocess.PIPE)
    output = awk.communicate()[0].strip()
    return int(output.split('\n')[-1].split(' ')[0])+1
    #return int(i.split(' ')[0])+1
class Make_iptables(object):
    def __init__(self,lanip,relate):
        self.lanip = lanip
        self.relate = relate
    @staticmethod
    def looktable():
        cat = subprocess.Popen(["cat","/etc/sysconfig/iptables"],stdout=subprocess.PIPE)
        grep = subprocess.Popen(["grep","-i","PREROUTING"],stdin=cat.stdout,stdout=subprocess.PIPE)
        awk = subprocess.Popen(["awk","-F","[' ',:]+","{print $10,$14,$15}"],stdin=grep.stdout,stdout=subprocess.PIPE)
        output = awk.communicate()[0].strip()
        x = PrettyTable(["外网IP","外网端口","对应关系", "内网IP", "内网端口"])
        x.reversesort = True
        x.align["外网端口"] = "l"
        for i in output.split('\n'):
            x.add_row(['180.76.142.13',i.split(' ')[0],'<<-->>',i.split(' ')[1],i.split(' ')[2]])
        print(x)
    def pnat(self):
        l=[]
        for i in self.relate:
            prerouting_cmd = 'iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport '+ i[1]+' -j DNAT --to-destination '+self.lanip+':'+i[0]
            postrouting_cmd = 'iptables -t nat -A POSTROUTING -d '+self.lanip+'/32'+' -p tcp -m tcp --dport '+i[0]+' -j SNAT --to-source '+localip
            l.append([prerouting_cmd,postrouting_cmd])
        return l
    def check_port(self):
        for i in self.relate:
            str_spc='"'+'dport '+str(i[1])+' -j '+'"'
            ret = subprocess.call('cat /etc/sysconfig/iptables |grep --color '+str_spc,shell=True)
            if ret == 0:
                print '\033[31;1m%s\033[0m'%('外网端口'+str(i[1])+'已使用,以上是已使用记录,请重新执行 ！')
                exit()
            else:
                print '\033[31;1m%s\033[0m' % ('外网端口'+str(i[1])+'检查通过，可以使用！')
    def iptables_overview(self):
        for i in range(len(self.relate)):
            print '规则预览 :'+self.pnat()[i][0]
            print '规则预览 :'+self.pnat()[i][1]
        confirm = raw_input('确认执行 防火墙规则？y/n ')
        if confirm == 'y':
            for i in range(len(self.relate)):
                ret = subprocess.call(self.pnat()[i][0],shell=True)
                ret1 = subprocess.call(self.pnat()[i][1],shell=True)
                if ret == 0 and ret1 == 0:
                    print '\033[31;1m%s\033[0m' % ('第'+str(i+1)+'组执行成功 ！！')
        else:
            print '已退出 ！！' 
        save = raw_input('是否立即保存防火墙规则？y/n ')
        if save == 'y':
            ret = subprocess.call('service iptables save',shell=True)
            if ret == 0 :
                print '\033[31;1m%s\033[0m' % '保存成功 ！！'
        else:
            print '\033[31;1m%s\033[0m' % '未保存 ！！'
if __name__=='__main__':
    Make_iptables.looktable()
    print '\033[31;92m%s\033[0m' % ('防火墙nat规则生成脚本，当前主机IP:'+localip+',目前暂只支持nat端口转发功能')
    ip=raw_input('请输入要映射的内网IP地址,可只写ip地址最后一位，默认同当前主机一个网段: ')
    if checkip(ip):
        lanip=ip
    elif int(ip):
        lanip='192.168.0.'+ip
    else:
        print '地址错误请重新输入'
    lanport=raw_input('请输入要映射的内网IP地址的端口,多个使用逗号分隔: ')
    wanport=raw_input('请输入要映射出去的外网端口,多个使用逗号分隔: ['+str(maxport())+']')   
    if not wanport:
        wanport=str(maxport())
    relate=zip(lanport.split(','),wanport.split(','))
    for i in relate:
        print '\033[31;92m%s\033[0m' %('端口映射关系为: x.x.x.x:%s'%i[1]+'<<-->>'+lanip+':'+i[0])
    p=Make_iptables(lanip,relate)
    p.pnat()
    p.check_port()
    p.iptables_overview()
