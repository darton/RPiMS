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
#raspivid -o - -t 0 -hf -w 640 -h 360 -fps 25 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264

location=$(redis-cli get location)

function stream_on { 
    raspivid_pid=$(pidof raspivid)
    vlc_pid=$(pidof vlc)

    if ([ ! -n "$raspivid_pid" ] && [ ! -n "$vlc_pid" ]) then
	raspivid -o - -t 0 -n -a 8 -rot 270 -a "$location %Y-%m-%d %X" -fps 30 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264  --h264-fps=30 &
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
    echo -e "\nUsage: videostream.sh start|stop"  ;;

esac
