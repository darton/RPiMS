#!/usr/bin/env bash

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

video_dir=/home/pi/Videos
video_file=pivideo_$now

[[ -d $video_dir ]] || mkdir $video_dir;chown pi.pi $video_dir


ffmpeg_pid=$(pidof ffmpeg)

if [ $ffmpeg_pid -n ]
then
    pkill ffmpeg
fi

ffmpeg -use_wallclock_as_timestamps 1 -f mjpeg -i "http://localhost:8080/stream/video.mjpeg" -t 5 -c copy -y $video_dir/$video_file.mp4

exit 0
