#!/bin/bash
#Author:Dawson
#Desc:Jenkins CI Script
set -e
ERR='unknow error'
ERRCODE=1
STOPCOUNT=0
STARTCOUNT=0
BACKUPVERSION=$(date "+%Y%m%d%H%M%S")
declare -A SERVERLIST
declare -A RUNWAYLIST
declare -A HARBOR_NAMELIST
SERVERLIST=(["wisdomtest"]=192.168.0.29 ["dubboxtest"]=192.168.0.30  ["learntest"]=192.168.0.31 ["saastest1"]=192.168.0.41 ["saastest2"]=192.168.0.49 ["livewbl"]=192.168.0.47 ["cimwbl"]=192.168.0.40 ["apollo"]=192.168.0.38 ["wisdomwbl"]=192.168.0.44 ["resourcewbl"]=192.168.0.44 ["cimwbl"]=192.168.0.40 ["wisdompre"]=192.168.0.45 ["learnwbl"]=192.168.0.46 ["ucwbl"]=192.168.0.48 ["passportwbl"]=192.168.0.48 ["liveyc"]=192.168.0.54 ["cimyc"]=192.168.0.54 ["learnyc"]=192.168.0.52 ["wisdomyc"]=192.168.0.97  ["wisdomkx"]=192.168.32.11 ["uckx"]=192.168.32.9  ["livekx"]=192.168.32.10 ["gzls"]=192.168.0.61 ["ys"]=192.168.0.42 ["yn"]=192.168.0.67 ["gz"]=192.168.0.68 ["sc"]=192.168.0.69 ["gx"]=192.168.0.70 ["slave"]=192.168.0.24 ["zhanhui1"]=192.168.0.72 ["zhanhui2"]=192.168.0.72 ["k8s1"]=192.168.32.12 ["jkyzc"]=192.168.0.53) 
RUNWAYLIST=( ["deploy"]=docker_playbook ["deploy_bak"]=docker_bak_playbook)
SERVER=${SERVERLIST[${NODE}]}
echo ${SERVER}
RUNWAY=${RUNWAYLIST[${RUNMODE}]}
echo ${RUNWAY}
MYSPACE=${WORKSPACE}/dockertmp
print_start(){
let STARTCOUNT+=1
echo "===============================步骤${STARTCOUNT}:${1} 开始 ==================================="
}
print_stop(){
let STOPCOUNT+=1
echo "*******************************步骤${STOPCOUNT}:${1} 完成 *************************************"
}
clean_old(){
	print_start '清除临时目录' 
	[  ! -d  dockertmp ] && mkdir dockertmp || ( rm -rf dockertmp && mkdir dockertmp );
	MYSPACE=${WORKSPACE}/dockertmp
	print_stop '清除临时目录' 
}
create_pkg(){
	clean_old
	print_start 'Maven打包'
	if [ -e ${WORKSPACE}/pom.xml -a -e ${WORKSPACE}/scripts/build_pro.sh ];then
		echo 'use build.sh'
	elif [ -e ${WORKSPACE}/pom.xml -a ! -e ${WORKSPACE}/scripts/build_pro.sh ];then
		echo 'use mvn'
                if [ ! -n "${MVN}" ];then
                    /usr/maven/bin/mvn clean install -Dmaven.test.skip=true -U && print_stop 'Maven打包' || echo 'Maven打包失败,请检查代>码！！'
                else
                    /usr/maven/bin/mvn clean install -D skip.test=true -P ${MVN}
                fi
        else  
		echo '未找到pom文件,确认是否需要maven打包'
		exit ${ERRCODE}
	fi 
}
find_copy_pkg(){
	clean_old
	print_start '匹配包名'
	PKGNAME=$(find . -maxdepth 3 -iname *${KEYWORDS}*.*ar)
	echo $PKGNAME
	if [ ! -n "${PKGNAME}" ];then 
		echo 'svn目录不存在jar包/未找到包匹配,退出'
		exit ${ERRCODE}
	fi
	for name in ${PKGNAME};do
		echo ${name##*/}
	done
	PKGCOUNT=$(find . -maxdepth 3 -iname *${KEYWORDS}*.*ar -print0|xargs -0 ls -l|wc -l)
	if [ "${PKGCOUNT:-10}" -gt 1 ];then 
		echo "有${PKGCOUNT:-10}个包匹配,请写入足以匹配唯一包名的关键字,勾选清除上次构建目录重试"
		exit ${ERRCODE}
	elif [ "${PKGCOUNT:-0}" -lt 1 ];then 
		echo "未找到包匹配,请确认关键字"
	else 
		echo "已找到匹配包名"
		print_stop '匹配包名'
	fi  
	print_start '拷贝jar包到临时工作目录'
	SUFFIX=${PKGNAME:0-3}
	#PREFIX=$(echo ${PKGNAME##*/}|sed 's/-[0-9]\.[0-9]-.*//'|sed 's/-v[0-9]//'|cut -d'.' -f1)
	PREFIX=$(echo ${PKGNAME##*/}|sed 's/-[0-9].*//'|sed 's/-v[0-9]//'|cut -d'.' -f1)
	[[ "${PKGNAME}" =~ "wisdom-platform" ]] && LANPORT=81	
	[[ "${PKGNAME}" =~ "wisdom-cms" ]] && LANPORT=82
	#[[ "${PKGNAME}" =~ "resource" ]] && LANPORT=83
	[[  "${PKGNAME}" =~ "live-web" || "${PKGNAME}" =~ "autonomic-learn" || "${PKGNAME}" =~ "live-admin" ]] && VOLUMN="-v /data/upload/:/upload/" 
	[[ "${PKGNAME}" =~ "cim-web"  ]] && VOLUMN="-v /data/upload/cim/:/upload/" 
	echo ${PKGNAME}
	echo ${PREFIX}
	echo ${SUFFIX}
	cp -f ${PKGNAME} ${MYSPACE}/${PREFIX}.${SUFFIX}
	print_stop '拷贝jar包到临时工作目录'
        if [ ${HARBOR_NAME} == "saas" ];then
        HARBOR_NAME=yc
        fi
        if [ ${HARBOR_NAME} == "wbl" ];then
            echo "wbl线上业务正在迁移k8s,如需上线请与管理员联系!!!"
            exit 1
        fi 
        if [ ${HARBOR_NAME} == "yc" ] || [ ${HARBOR_NAME} == "kx" ];then
        wget -qO- --post-data  "proname=${PREFIX}&proenv=${HARBOR_NAME}&action=reset" "https://cmdb.hseduyun.net/auditapi/"
        echo "------------------${HARBOR_NAME} ${PREFIX}上线需要审批--------------------------"
        echo "等待审核中..."
        for i in {1..20}
        do
        CODE=`wget -qO-  "https://cmdb.hseduyun.net/auditapi/?proname=${PREFIX}&proenv=${HARBOR_NAME}"`
        sleep 10
        if [ ${CODE} == "null" ];then
        echo "------------------${HARBOR_NAME} ${PREFIX}未加入工单流程暂时关闭--------------------------" 
        exit 1
        fi
        if [ ${CODE} -eq 0 ];then
        echo "------------------${HARBOR_NAME} ${PREFIX}工单审批未通过--------------------------" 
        exit 1
        fi
        if [ ${CODE} -eq 1 ];then 
        echo "------------------${HARBOR_NAME} ${PREFIX}工单审批已通过,开始部署--------------------------"
        break
        fi
        done
        if [ ${CODE} -eq 2 ];then
        echo "------------------${HARBOR_NAME} ${PREFIX}工单审批超时--------------------------" 
        exit 1
        fi
        else
        continue
        fi
}
#万柏林、运城线上环境上线审批
docker_file(){
	print_start 'DockerFile编写'
	QUOT="\""
	APP=${PREFIX}.${SUFFIX}
	if [ "${CONFIG}" -a "${CLUSTER}" -a "${DENV}" ];then
		OPT1=${QUOT}-Denv=${DENV}${QUOT},${QUOT}-Dapollo.cluster=${CLUSTER}${QUOT},
		OPT2="CMD [${QUOT}--spring.profiles.active=${CONFIG}${QUOT}]"
		echo ${OPT1}
	elif [ "${CONFIG}" -a ! "${CLUSTER}" ];then
		OPT2="CMD [${QUOT}--spring.profiles.active=${CONFIG}${QUOT}]"
		echo ${OPT2}
	elif [ "${CONFIG}" -a  "${CLUSTER}" ];then
		OPT1=${QUOT}-Denv=${CONFIG}${QUOT},${QUOT}-Dapollo.cluster=${CLUSTER}${QUOT},
		echo ${OPT2}
	else
		echo 'Use Default Entrypoint'
	fi
	cd ${MYSPACE}
	cat > Dockerfile <<EOF
FROM harbor.hseduyun.net/hs/jdk-1.8.0:v3
MAINTAINER dawson_2014@163.com
COPY ${APP} /mnt/${APP}
VOLUME /logs
WORKDIR /mnt
ENTRYPOINT ["java", "-jar",${OPT1}${QUOT}${APP}${QUOT}]
#ENTRYPOINT ["java","-Xms2000m","-Xmx2000m","-Xss256k","-jar",${OPT1}${QUOT}${APP}${QUOT}]
${OPT2}
EOF
	print_stop 'DockerFile编写'
}
docker_image(){
	cd ${MYSPACE}
	#动态匹配docker
	print_start 'DockerImage打包'
	PREFIX=`echo ${PREFIX} | tr 'A-Z' 'a-z'`
	docker build -t ${PREFIX}  .
	print_stop 'DockerImage打包'
	print_start 'DockerImage推送私有仓库'
	#docker tag -f ${PREFIX} harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX} 
	docker tag  ${PREFIX} harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX} &>/dev/null || docker tag -f ${PREFIX} harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX} 
	docker push harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX}
	print_stop 'DockerImage推送私有仓库'
}
docker_playbook(){
	print_start 'run.yml编写'
	NETWORK="--net=host"
	if [ "${LANPORT:-100}"  -lt 90 ];then
		let WANPORT=${LANPORT}*100
		NETWORK="-p ${WANPORT}:${LANPORT}"
		echo "docker 网络模式:${NETWORK}";
		echo "容器挂载情况 ${VOLUMN:-null}"
	else
		echo "docker 网络模式:${NETWORK}";
		echo "容器挂载情况 ${VOLUMN:-null}"
	fi
cat > run.yml <<EOF
- hosts: ${SERVER}
  gather_facts: false
  tasks:
    - name: 'pull 镜像'
      command: docker pull harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX}
    - name: 'stop 容器'
      command: docker stop ${PREFIX}
      ignore_errors: yes
    - name: 'delete 容器'
      command: docker rm ${PREFIX}
      ignore_errors: yes
    - name: 'run 容器'
      command: docker run -d ${NETWORK} ${VOLUMN} --name ${PREFIX} --restart=always harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX}
EOF
	print_stop 'run.yml编写'
}

docker_bak_playbook(){
	print_start 'run.yml编写'
	NETWORK="--net=host"
	if [ "${LANPORT:-100}"  -lt 90 ];then
		let WANPORT=${LANPORT}*100
		NETWORK="-p ${WANPORT}:${LANPORT}"
		echo "docker 网络模式:${NETWORK}";
		echo "容器挂载情况 ${VOLUMN:-null}"
	else
		echo "docker 网络模式:${NETWORK}";
		echo "容器挂载情况 ${VOLUMN:-null}"
	fi
cat > run.yml <<EOF
- hosts: ${SERVER}
  gather_facts: false
  tasks:
    - name: 'backup 容器'
      command: docker rename ${PREFIX} ${PREFIX}.${BACKUPVERSION}
      ignore_errors: yes
    - name: 'stop 容器'
      command: docker stop ${PREFIX}.${BACKUPVERSION}
      ignore_errors: yes
    - name: 'pull 镜像'
      command: docker pull harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX}
    - name: 'run 容器'
      command: docker run -d ${NETWORK} ${VOLUMN}  --name ${PREFIX} --restart=always harbor.hseduyun.net/${HARBOR_NAME}/${PREFIX}
EOF
	print_stop 'run.yml编写'
}
run_playbook(){
	${RUNWAYLIST[${RUNMODE}]}
	print_start '执行yml部署文件 部署'
	ansible-playbook run.yml	
	print_stop '执行yml部署文件 部署'
}

OLD_IFS="$IFS"
IFS=","
for i in ${RUN_PARA};do
	$i
done
IFS="$OLD_IFS"
