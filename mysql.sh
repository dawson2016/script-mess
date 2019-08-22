#!/bin/bash
for i in `ls`
do
echo 'import',$i 
mysql -uroot -p123456 -e "source $i"
done
