#!/bin/bash
##written by dawson @2016.03.24
#***********************************调用微信接口凭证和网址*****************
CropID=wxeb265293e3ccb970
Secret=CJzowyfno3-r75dwe0dAgMZONS5eq5DhZxQLg6SQoGMMZ4nG0x0yL3dHxzOpr3Z6
GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CropID&corpsecret=$Secret"
Gtoken=`/usr/bin/curl -s -G $GURL | awk -F \" '{print$4}'`
URL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$Gtoken"
#***********************************针对cpu和mysql特殊情况更改变量*****************
#echo $3 | grep cpu | grep PROBLEM  &>/dev/null && cpu1=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '1p'`  && cpu2=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '2p'` && cpu3=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '3p'` && i=,占用cpu前三进程: && a=$i$cpu1,$cpu2,$cpu3 && a=`echo $a | sed -e 's/[[:space:]][[:space:]]*/负载/g'` 
#echo $3 | grep mysql | grep PROBLEM  &>/dev/null && b=,正在自动重启mysql服务....如果没有收到OK信息请登陆服务器查看  
#Content=$3$a$b
##***************************************从数据库获取graphid****************************
Content=$3
/usr/bin/curl -s --data-ascii  '{ "touser": "@all", "toparty": " @all ","msgtype": "text","agentid": "0","text": {"content": "'$Content'"},"safe":"0"}' $URL
exit
ip=`echo $2|awk -F : '{print $1}'`
item=`echo $2|awk -F : '{print $2}'`
conn_mysql="mysql -uzabbix -pzabbix zabbix"
sql1="select hostid from interface where ip='$ip'"
mya1=`echo "${sql1}"|${conn_mysql} 2>/dev/null`
hostid=`echo $mya1|awk '{print $2}'`
sql2="select itemid from items where hostid=BINARY'$hostid' and name=BINARY'$item'"
mya2=`echo "${sql2}"|${conn_mysql} 2>/dev/null`
itemid=`echo $mya2|awk '{print $2}'`
sql3="select graphid from graphs_items where itemid='$itemid'"
gphid1=`echo "${sql3}"|${conn_mysql} 2>/dev/null`
gphid2=`echo $gphid1|awk '{print $2}'`
#echo  $gphid2 >>/tmp/test
#exit
##**************************************下载图片到指定目录****************************
curl -so /tmp/$itemid.png http://192.168.1.15/zabbix/chart2.php?graphid=$gphid2
##**************************************上传图片获得mediaid****************************
MEDIA_ID=`curl -s -F "access_token=$Gtoken" -F "type=image" -F "media=@/tmp/$itemid.png"  https://qyapi.weixin.qq.com/cgi-bin/media/upload?|awk -F [:,\"]+ '{print $5}'`
##***************************************发送消息和图片3秒后删除图片****************************
Content=$3
#echo $MEDIA_ID>>/tmp/alert
/usr/bin/curl -s --data-ascii  '{ "touser": "@all", "toparty": " @all ","msgtype": "text","agentid": "0","text": {"content": "'$Content'"},"safe":"0"}' $URL
/usr/bin/curl -d '{ "touser": "@all", "toparty": " @all ","msgtype": "image","agentid": "0","image": {"media_id": "'$MEDIA_ID'","safe":"0"}' $URL
sleep 3
rm -rf /tmp/$itemid.png
