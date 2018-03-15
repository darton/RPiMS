#!/bin/bash

#raspivid -o - -t 0 -hf -w 640 -h 360 -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264

function stream_on { 
    raspivid_pid=$(pidof raspivid)
    vlc_pid=$(pidof vlc)
    
if [ $raspivid_pid -n ]; 
then
    pkill raspivid
fi 
   
   if [ $vlc_pid -n]; 
then
    pkill vlc
fi 
    
    raspivid -o - -t 0 -n -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 &
}

function stream_off {
    pkill raspivid
    pkill vlc
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
