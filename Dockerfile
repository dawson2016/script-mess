FROM 192.168.1.15:5000/centos6.8:latest 
MAINTAINER Dawson dawson.dong@bibenet.com
ENV CATALINA_HOME /tomcat
ENV JAVA_HOME /jdk
ENV CLASSPATH /jdk/lib/dt.jar:/jdk/lib/tools.jar
ENV LANG zh_CN.UTF-8
ADD tomcat /tomcat
ADD jdk1.7.0  /jdk
ADD szca  /data/szca
ADD szcaVerify  /data/szcaVerify
ADD run.sh /run.sh
RUN useradd bitbid  -s /bin/bash && chown -R bitbid.bitbid /tomcat /jdk /run.sh
USER bitbid
EXPOSE 9080
CMD ["/run.sh"]
