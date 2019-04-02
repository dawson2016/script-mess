#!/bin/bash
#当前端口
file=/etc/sysconfig/iptables
num=`cat ${file} |grep -v "\-1"|grep "PREROUTING"|sed '1d'|awk '{print $10}'|wc -l`
old=`cat ${file}|grep -v "\-1"|grep "PREROUTING"|sed '1d'|awk '{print $10}'`
unum=`sort -k2n $file|grep -v "\-1"|grep "PREROUTING"|sed '1d'|awk '{print $10}'|uniq|wc -l`
#前一次生成的端口组成数组
oldp=()
c=0
for i in $old
do
oldp[${c}]=${i}
let c++
done
#生成随机端口
function rand(){  
        min=$1  
        max=$(($2-$min+1))  
        num=$(date +%s%N)  
        echo $(($num%$max+$min))
        return 0
}
#新生成的端口组成数组并进行替换
        newp=()
        b=0
        for a in $(seq 1 ${num})
        do
        rnd=$(rand 20000 60000)
        newp[${b}]=${rnd}
        let b++
        done
length=0
for i in ${oldp[*]}
do
sed -i "s/${oldp[$length]}/${newp[$length]}/g" $file &>/dev/null
let length++
done
#判断端口是否有重复,如果有继续使用上次生成的端口
if [ ${num} -eq ${unum} ];then
    MAIL
else
    python /root/mail.py "New iptables rules Port repeat" "Not changed"
    sed -i "s/${newp[$length]}/${oldp[$length]}/g" $file &>/dev/null
fi
function MAIL()
{
/etc/init.d/iptables reload && /etc/init.d/iptables save
#生成端口列表
echo "<meta charset="utf-8"><pre>" > /hskj/openresty/nginx/html/portlist.html
echo -e "规则生成时间: `date`   6小时后更新" >> /hskj/openresty/nginx/html/portlist.html
python scan_rules.py >> /hskj/openresty/nginx/html/portlist.html
#生成泛微专用端口列表
echo >/hskj/openresty/nginx/html/fanwei.html && echo "<meta charset=utf-8><h1>" >>/hskj/openresty/nginx/html/fanwei.html && for i in `cat /etc/sysconfig/iptables|grep '泛微'|awk -F [' ']+ '{print $14,$10}'`; do echo $i >>/hskj/openresty/nginx/html/fanwei.html; done
echo "</h1>">>/hskj/openresty/nginx/html/fanwei.html
if [ $? -ne 0 ];then
    python /root/mail.py "New iptables rules Execution fail" "`cat /hskj/openresty/nginx/html/portlist.html |sed 1,4d|grep -v \<\/pre\> |awk '{print $4,$5,$8,$9,$10,$11,$12}'`"
else
    python /root/mail.py "New iptables rules Execution success" "`cat /hskj/openresty/nginx/html/portlist.html |sed 1,4d|grep -v \<\/pre\> |awk '{print $4,$5,$8,$9,$10,$11,$12}'`"
fi
return 0
}
MAIL
