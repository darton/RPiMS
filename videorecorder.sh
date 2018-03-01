#!/bin/bash

video_dir=/home/pi/video
video_file=pivideo

pkill raspivid

#raspivid -t 5000 -fps 25 -b 6000000  -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -p 0,0,1920,1080 -o $video_dir/$video_file.h264
raspivid -t 5000 -fps 25 -b 6000000  -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -n -o $video_dir/$video_file.h264

cd $video_dir

MP4Box -add $video_file.h264 $video_file.mp4

rm $video_file.h264

exit 0
