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

now=$(date +%H%M%S_%m_%d_%Y)

video_dir=/home/pi/Video
video_file=pivideo_$now

[[ -d $video_dir ]] || mkdir $video_dir

raspivid_pid=$(pidof raspivid)

if [ $raspivid_pid -n ]
then
    pkill raspivid
fi 

#raspivid -t 5000 -fps 25 -b 6000000  -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -p 0,0,1920,1080 -o $video_dir/$video_file.h264
#raspivid  --profile high --level 4.2 -t 5000 -fps 30 -b 10000000  -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -n -o $video_dir/$video_file.h264
#ffmpeg -fflags +genpts -i $video_file.h264 -c copy $video_file.mp4
#ffmpeg  -i $video_file.h264 -c copy -vsync 0 -enc_time_base -1 $video_file.mp4

raspivid -t 5000 -fps 30 -b 6000000  -a 8 -a "Serwerownia_1 %Y-%m-%d %X" -n -o $video_dir/$video_file.h264

cd $video_dir

MP4Box -fps 30 -add $video_file.h264 $video_file.mp4

rm *.h264

exit 0
