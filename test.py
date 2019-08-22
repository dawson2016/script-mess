#!/usr/bin/env python
import threading
import Queue
import socket
import sys
q = Queue.Queue(maxsize = 0)
lock = threading.RLock()
a=[]
ip=sys.argv[1]
para=sys.argv[2]
paralis=para.split('-')
def port_test(x):  
        global count 
        portcon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portcon.settimeout(1)
        try:
            portcon.connect((ip,int(x))) 
            pass
        except Exception:
            lock.acquire()
            a.append(x)
            lock.release()
            portcon.close()
for i in paralis:
    t =threading.Thread(target=port_test,args=(i,))
    t.start()
t.join()
if a!=[]:
    print str(len(a))+' port failed : '+str(a)
else:
    print 'all ports ok'
