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
# https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.min.js.map
# https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.min.js

source /var/www/html/conf/rpims-stream.conf

function stream_on {
    ffmpeg_pid=$(pidof ffmpeg)
    raspivid_pid=$(pidof raspivid)

    if ([ ! -n "$ffmpeg_pid" ] && [ ! -n "$raspivid_pid" ]  ) then

        [[ -d /dev/shm/streaming ]] || mkdir -p /dev/shm/streaming

        if [ ! -e /var/www/html/streaming ]; then
            ln -s  /dev/shm/streaming /var/www/html/streaming
        fi
        if [ ! -e /var/www/html/streaming/stream.html ]; then
            cp /var/www/html/stream/stream.html /var/www/html/streaming/
        fi
        if [ ! -e /var/www/html/streaming/hls.min.js ]; then
            cp /var/www/html/stream/hls.min.js /var/www/html/streaming/
        fi
        if [ ! -e /var/www/html/streaming/hls.min.js.map ]; then
            cp /var/www/html/stream/hls.min.js.map /var/www/html/streaming/
        fi

            #raspivid -w 640 -h 480  -o - -t 0 -n -a 8 -rot 0 -a "$location %Y-%m-%d %X" -fps 30 | cvlc --rtsp-timeout 10 -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 --h264-fps=30 &
            #raspivid -o - -t 0 -n -w 1280 -h 1024 -rot 0 -a "$location %Y-%m-%d %X" -fps 30 | cvlc  --rtsp-timeout 1000  -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264 --h264-fps=30 --sout-rtsp-user rpims --sout-rtsp-pwd password &
            ##/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 1640x922 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8
            #/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -use_wallclock_as_timestamps 1 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags independent_segments+delete_segments /dev/shm/streaming/live.m3u8
            #/usr/bin/ffmpeg -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags split_by_time+delete_segments /dev/shm/streaming/live.m3u8
            #/usr/bin/ffmpeg -y -hide_banner -use_wallclock_as_timestamps 1 -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -map_metadata 0 -metadata:s:v rotate="90" -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8
            #/usr/bin/ffmpeg -y -hide_banner -use_wallclock_as_timestamps 1 -input_format h264 -f video4linux2  -video_size 640x480 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 6 -hls_list_size 6 -hls_flags delete_segments /dev/shm/streaming/live.m3u8
            #raspivid -n -o - -t 0 -vf -hf -fps 30 -b 6000000 -rot 270 -w 640 -h 480 | /usr/bin/ffmpeg -y -hide_banner -use_wallclock_as_timestamps 1 -f h264 -i - -c:v copy -f hls -hls_time 6 -hls_list_size 3 -hls_flags delete_segments /dev/shm/streaming/live.m3u8

            #/usr/bin/ffmpeg -y -hide_banner -use_wallclock_as_timestamps 1 -input_format h264 -f video4linux2 -video_size 640x480 -framerate 30 -i /dev/video0 -c:v copy -f hls -hls_time 1 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8

            #/usr/bin/raspivid -n -o - -t 0 -rot 0 -w 640 -h 480 -fps 25 -b 6000000 | /usr/bin/ffmpeg -y -hide_banner -use_wallclock_as_timestamps 1 -f h264 -i - -c:v copy -f hls -hls_time 6 -hls_list_size 30 -hls_flags delete_segments /dev/shm/streaming/live.m3u8

            /usr/bin/raspivid -n \
			      -o - \
			      -t 0 \
			      -rot $ROT \
			      -fps $FPS \
			      -w $DISPX \
			      -h $DISPY \
			      -b $BITRATE| \
            /usr/bin/ffmpeg -i - \
                            -y \
                            -hide_banner \
                            -use_wallclock_as_timestamps 1 \
                            -c:v copy \
                            -f hls \
                            -hls_time 2 \
                            -hls_list_size 5 \
                            -hls_flags delete_segments /dev/shm/streaming/live.m3u8
    else
            echo "ffmpeg or raspivid is already running !"
    fi

}

function stream_off {
    pkill ffmpeg
    pkill raspivid
    exit 0
}

case "$1" in

    'start')
    pkill ffmpeg
    pkill raspivid
    stream_on
    ;;
    'stop')
    stream_off
    ;;
           *)
    echo -e "\nUsage: videostreamer.sh start|stop"  ;;

esac
