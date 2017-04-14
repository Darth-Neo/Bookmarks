#!/usr/bin/env sh

export NOW=$(date +"%Y-%m-%d-%H-%M")

hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -files /home/hduser/run/mapper.py,/home/hduser/run/reducer.py   -reducer /reducer.py -input DaVinc.txt -output /go_$NOW
