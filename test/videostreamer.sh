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


function stream_on {
    ffmpeg_pid=$(pidof ffmpeg)

    if ([ ! -n "$ffmpeg_pid" ]) then

        [[ -d /dev/shm/streaming ]] || mkdir -p /dev/shm/streaming

        if [ ! -e /var/www/html/streaming ]; then
            ln -s  /dev/shm/streaming /var/www/html/streaming
        fi
        if [ ! -e /var/www/html/streaming/index.html ]; then
            cp /var/www/html/stream/index.html /var/www/html/streaming/
        fi
        if [ ! -e /var/www/html/streaming/hls.js ]; then
            cp /var/www/html/stream/hls.js /var/www/html/streaming/
        fi

        #raspivid -w 640 -h 480  -o - -t 0 -n -a 8 -rot 0 -a "$location %Y-%m-%d %X" -fps 30 | cvlc --rtsp-timeout 10 -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 --h264-fps=30 &
        #raspivid -o - -t 0 -n -w 1280 -h 1024 -rot 0 -a "$location %Y-%m-%d %X" -fps 30 | cvlc  --rtsp-timeout 1000  -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264 --h264-fps=30 --sout-rtsp-user rpims --sout-rtsp-pwd password &
        ##/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 1640x922 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8
        #/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -use_wallclock_as_timestamps 1 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags independent_segments+delete_segments /dev/shm/streaming/live.m3u8
        #/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags split_by_time+delete_segments /dev/shm/streaming/live.m3u8
        /usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8
    else
        echo "ffmpeg is already running !"
    fi

}

function stream_off {
    pkill ffmpeg
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
