#!/bin/bash
to_email_address="$1"               # 收件人Email地址，zabbix传入的第一个参数
message_subject_utf8="$2"           # 邮件标题，zabbix传入的第二个参数
message_body_utf8="$3"              # 邮件内容，zabbix传入的第三个参数
message_subject_gb2312=`iconv -t GB2312 -f UTF-8 << EOF
$message_subject_utf8 
EOF`
[ $? -eq 0 ] && message_subject="$message_subject_gb2312" || message_subject="$message_subject_utf8"
message_body_gb2312=`iconv -t GB2312 -f UTF-8 << EOF 
$message_body_utf8 
EOF`
[ $? -eq 0 ] && message_body="$message_body_gb2312" || message_body="$message_body_utf8"
echo $3 | grep cpuload  &>/dev/null 
[ $? -eq 0 ] && cpu_max1=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '1p'`  && cpu_max2=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '2p'`&& cpu_max3=`ps aux | grep -v ^'USER' | sort -rn -k3 | awk '{print $1"\t"$3}' | head -3 | sed  -n '3p'`|| cpu_max=''
echo "$message_body" "$cpu_max1" "$cpu_max2" "$cpu_max3"| mail -s "$message_subject" $1
