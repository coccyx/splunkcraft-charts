FROM ubuntu
MAINTAINER Clint Sharp <csharp@splunk.com>
RUN apt-get update && apt-get install -y git wget openjdk-8-jdk python-cairo python-pycha python-pil python-pip
RUN pip install pypng && pip install splunk-sdk
RUN mkdir /tmp/minecraft /minecraft /data
RUN wget -O /tmp/minecraft/BuildTools.jar https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar
RUN cd /tmp/minecraft && java -jar BuildTools.jar --rev latest
RUN mv /tmp/minecraft/spigot-*.jar /minecraft
RUN rm -rf /tmp/minecraft
EXPOSE 25565
EXPOSE 4711
ADD start-minecraft.sh /root/start-minecraft.sh
COPY server.properties /data/server.properties
COPY raspberryjuice-1.8.jar /data/plugins/raspberryjuice-1.8.jar
COPY ops.json /data/ops.json
COPY usercache.json /data/usercache.json
COPY pycha-pie.diff /data/pycha-pie.diff
RUN patch /usr/share/pyshared/pycha/pie.py /data/pycha-pie.diff
COPY chart.py /data/chart.py
COPY minecraft /data/minecraft
COPY OpenSans-Regular.ttf /data/OpenSans-Regular.ttf
COPY crontab /data/crontab
# COPY cron_task.sh /data/cron_task.sh
COPY spigot.yml /data/spigot.yml
ENTRYPOINT ["/bin/bash", "/root/start-minecraft.sh"]
