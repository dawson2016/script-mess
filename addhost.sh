#!/bin/sh

wget -O ${1} https://cmdb.hseduyun.net/ingscan/?ns=${1}

if [ "${1}" == "yc" ];then
sed -i "s/[]|[|{|}|,|\"]/ /g;s/${1} :/192.168.0.13/g" ${1} && sed -i "s/^[ \t]*//g" ${1} && cat ${1} >> /etc/hosts
elif [ "${1}" == "wbl" ];then
sed -i "s/[]|[|{|}|,|\"]/ /g;s/${1} :/192.168.0.43/g" ${1} && sed -i "s/^[ \t]*//g" ${1} && cat ${1} >> /etc/hosts
else
sed -i "s/[]|[|{|}|,|\"]/ /g;s/${1} :/192.168.0.19/g" ${1} && sed -i "s/^[ \t]*//g" ${1} && cat ${1} >> /etc/hosts
fi
exec ${2}
