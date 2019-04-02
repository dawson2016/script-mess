#!/usr/bin/env groovy
def projectProperties = [
		[$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', numToKeepStr: '15']],
		parameters([
		choice(
		name: 'TIPS',
		choices: '参数跟以往记录一样的可直接回放',
	 ),
	 stringParam(name: 'SVN_URL', defaultValue: '', description: '请输入完整svn地址'),
	 stringParam(name: 'Artifacts', defaultValue: '', description: '请输入包名关键字,与yaml文件同名'),
	 stringParam(name: 'Config', defaultValue: '', description: '请输入配置文件名称spring.active.propertie=***'),
	 stringParam(name: 'Denv', defaultValue: '', description: '-Denv配置参数,未使用apollo配置的项目请留空'),
     stringParam(name: 'Cluster', defaultValue: '', description:'-Dapollo.cluster配置参数,未使用apollo配置的项目请留空'),
	 choice(
		name: 'ENV',
		choices: 'test\nyctest\nkxtest\ndemo\nwbl\nyc\ngz\nkx',
		description: '请选择部署到的环境:测试(万柏林)、测试(运城)、测试(市科协)、演示、万柏林、运城、贵州、科协'
	 ),
	 choice(
		name: 'YH',
		choices: '"',
		description: '默认分隔符忽略'
	 )])
]
properties(projectProperties)

podTemplate(label: 'mypod', cloud: 'kubernetes', 
        containers: [
		containerTemplate(name: 'maven', image: 'harbor.hseduyun.net/hs/maven:v2', command: 'cat', ttyEnabled: true),
		containerTemplate(name: 'docker', image: 'harbor.hseduyun.net/hs/docker', command: 'cat', ttyEnabled: true),
		containerTemplate(name: 'kubectl', image: 'harbor.hseduyun.net/hs/k8s-kubectl', command: 'cat', ttyEnabled: true)
        ],
		volumes: [
				persistentVolumeClaim(claimName: 'pvc-maven', mountPath: '/mnt/.m2', readOnly: false), 
				hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock'),
				hostPathVolume(hostPath: '/root/.kube', mountPath: '/root/.kube')
		]) 
{node('mypod') 
        {
		container('maven') {
		    stage('工单审批') {
                sh 'ENV=$(echo ${ENV})'
				sh 'echo 非运城线上环境可自由构建'
                sh 'if [ ${ENV} = yc ];then curl -s -X POST -d "proname=${Artifacts}&proenv=${ENV}&action=reset" "https://cmdb.hseduyun.net/auditapi/"; echo 上线需要审批; echo 等待审核中...;c=0;while [ $c -lt 10 ]; do sleep 3;CODE=`curl -Ss  "https://cmdb.hseduyun.net/auditapi/?proname=${Artifacts}&proenv=${ENV}"`;if [ ${CODE} -eq 1 ]; then echo ${ENV} ${Artifacts}工单审批已通过开始部署; echo break1;break;fi;if [ $c -eq 9 ]; then error echo 工单审批超时;fi; if [ ${CODE} -eq 0 ]; then error echo 工单已被拒绝;fi; c=`expr $c + 1`; done ;  fi'
		    }
			stage('svn代码检出') {
				checkout([$class: 'SubversionSCM', additionalCredentials: [], excludedCommitMessages: '', excludedRegions: '', excludedRevprop: '', excludedUsers: '', filterChangelog: false, ignoreDirPropChanges: false, includedRegions: '', locations: [[cancelProcessOnExternalsFail: true, credentialsId: '222', depthOption: 'infinity', ignoreExternalsOption: true, local: '.', remote: '${SVN_URL}']], quietOperation: true, workspaceUpdater: [$class: 'UpdateUpdater']])
			}

			stage('maven编译打包') { 
			if(fileExists('pom.xml')) 
				{
				sh 'Artifacts=$(echo ${Artifacts})'
				sh 'mvn clean install -Dmaven.test.skip=true -U'
				sh 'if [ -d target ]; then mkdir wraptmp && mv target wraptmp; fi'
				sh 'ls */target/*${Artifacts}*.*ar'
				}	
			 else {
				sh 'mkdir -p tmp/target && mv  *${Artifacts}*.*ar tmp/target'
			}
	
		    stage('编写yaml部署文件') {
				sh 	'Artifacts=$(echo ${Artifacts})'
				sh  'rm -f ${Artifacts}.yaml'
				sh  "echo 根据关键字下载yaml文件:你的关键字是${Artifacts}"
		        sh  "echo '如果下载报404找不到yaml文件 请确认关键字是否正确或联系ops !!'" 
				sh  "wget http://yaml.hseduyun.net/taiyuan/${ENV}/${Artifacts}.yaml"
				sh  "wget http://yaml.hseduyun.net/host.sh"
				sh  "sed -i \"s/hsns/${ENV}/g\" ${Artifacts}.yaml"
				sh  "sed -i \"s/hskw/${Artifacts}/g\" ${Artifacts}.yaml"
				sh  "sed -i \"s/hsimage/${ENV}-${Artifacts}/g\" ${Artifacts}.yaml"
				sh  "sed -i \"s/latest/v${BUILD_ID}/g\" ${Artifacts}.yaml"	
            }
			}    
		}
		container('docker') {
			stage('编写Dockerfile') {
				sh 'PKGNAME=`ls */target/*${Artifacts}*.*ar` && echo ${PKGNAME##*/} && \
				echo FROM harbor.hseduyun.net/hs/jdk-1.8.0:v3 >Dockerfile && \
				echo ADD */target/*${Artifacts}*.*ar /mnt/${PKGNAME##*/} >>Dockerfile && \
				echo ADD host.sh /usr/bin/host.sh >>Dockerfile && \
				echo RUN chmod +x /usr/bin/host.sh >>Dockerfile && \
				echo WORKDIR /mnt >>Dockerfile && \
				echo ENTRYPOINT [${YH}host.sh${YH}] >>Dockerfile && \
				echo CMD [${YH}${ENV}${YH},${YH}java -jar /mnt/${PKGNAME##*/} --spring.profiles.active=${Config} ${YH}] >>Dockerfile && \
	            if [  -n "${Config}" ]; then sed -i "/CMD/d" Dockerfile&&echo CMD [${YH}${ENV}${YH},${YH}java -jar /mnt/${PKGNAME##*/} --spring.profiles.active=${Config} ${YH}] >>Dockerfile;fi' 
				sh 'PKGNAME=`ls */target/*${Artifacts}*.*ar` && echo ${PKGNAME##*/} && \
				if [  -n "${Cluster}" ]; then sed -i "/CMD/d" Dockerfile&&sed -i "/CMD/d" Dockerfile&&echo CMD [${YH}${ENV}${YH},${YH}java -jar -Denv=${Denv} -Dapollo.cluster=${Cluster} /mnt/${PKGNAME##*/} --spring.profiles.active=${Config}${YH}] >>Dockerfile;fi'
				sh 'cat Dockerfile'
}
							
			stage('docker镜像构建推送') {
			   withDockerRegistry(credentialsId: '333', url: 'https://harbor.hseduyun.net/k8s') {docker.build('harbor.hseduyun.net/k8s/${ENV}-${Artifacts}:v${BUILD_ID}').push() }						
			}
			}
		stage('k8s部署镜像') {
			container('kubectl') {
				sh "kubectl --kubeconfig=/root/.kube/config apply -f ${Artifacts}.yaml" 
			}
		}
      	}
 }
