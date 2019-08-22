#!/bin/bash
##written by dawson @2016.01.06
#***********************************调用微信接口凭证和网址*****************
CropID=wxeb265293e3ccb970
Secret=CJzowyfno3-r75dwe0dAgMZONS5eq5DhZxQLg6SQoGMMZ4nG0x0yL3dHxzOpr3Z6
GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CropID&corpsecret=$Secret"
Gtoken=`/usr/bin/curl -s -G $GURL | awk -F \" '{print$4}'`
URL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$Gtoken"
Content=$1
/usr/bin/curl -s --data-ascii  '{ "touser": "@all", "toparty": " @all ","msgtype": "text","agentid": "0","text": {"content": "'$Content'"},"safe":"0"}' $URL
