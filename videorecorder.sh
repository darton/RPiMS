#!/bin/bash

raspivid -t 5000  -fps 25 -b 6000000 -p 0,0,1920,1080 -o /home/pi/video/pivideo.h264

cd /home/pi/video

MP4Box -add pivideo.h264 pivideo.mp4

rm pivideo.h264
