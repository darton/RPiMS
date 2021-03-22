#!/bin/bash

#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

location=$(redis-cli get location)

function stream_on {
    raspivid_pid=$(pidof raspivid)
    vlc_pid=$(pidof vlc)

    if ([ ! -n "$raspivid_pid" ] && [ ! -n "$vlc_pid" ]) then
        #raspivid -o - -t 0 -n -a 8 -rot 270 -a "$location %Y-%m-%d %X" -fps 30 | cvlc --rtsp-timeout 10 -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 --h264-fps=30 &
        raspivid -o - -t 0 -n -w 1280 -h 1024 -rot 0 -a "$location %Y-%m-%d %X" -fps 30 | cvlc --rtsp-timeout 1000 -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264 --h264-fps=30 --sout-rtsp-user rpims --sout-rtsp-pwd password &
        #raspivid -o - -t 0 -n -w 1440 -h 1080 -rot 0 -a "$location %Y-%m-%d %X" -fps 24 | cvlc --rtsp-timeout 1000 -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264 --h264-fps=24 --sout-rtsp-user username --sout-rtsp-pwd password
    fi

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
    echo -e "\nUsage: videostreamer.sh start|stop"  ;;

esac
