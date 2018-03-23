#!i/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

os.system(r'ffmpeg -f video4linux2 -i /dev/video0 -s 854x486 -r 15 -b:v 1000k -c:v h264_omx -maxrate 1600k -bufsize 4M -f flv "rtmp://txy.live-send.acg.tv/live-txy/?streamname="')
