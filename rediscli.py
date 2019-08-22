#!/usr/bin/env python
#coding:utf-8
#realtime time log
import redis
rc = redis.Redis(host='127.0.0.1',port=6379,password='redis123456') 
ps = rc.pubsub() 
ps.subscribe(['fm110']) 
for item in ps.listen(): 
    if item['type'] == 'message': 
        print item['data']

