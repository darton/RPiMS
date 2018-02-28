#!/bin/bash

#raspivid -o - -t 0 -hf -w 640 -h 360 -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264

function stream_on {

raspivid -o - -t 0 -hf -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 &

}

function stream_off {

ps ax|grep raspivid | grep -v grep | awk '{print "kill -9 "$1}' |bash
ps ax|grep \/usr\/bin\/vlc |grep -v grep | awk '{print "kill -9 "$1}'|bash
exit 0

}



case "$1" in

    'start')
    stream_on
    ;;
    'stop')
    stream_off
    ;;
           *)
    echo -e "\nUsage: stream.sh start|stop"  ;;

esac
