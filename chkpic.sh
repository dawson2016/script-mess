#!/bin/bash
cd /home/bitbid/tomcat_Bitbid/webapps/bidding/upload/ZONE_IMG
for i in `ls`
do
cd $i
   for j in `ls`
   do
   file $j |grep ASCII
   if [ $? == 0 ]
      then
      echo $i,$j
   fi
   done
cd ..
done






