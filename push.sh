#!/bin/bash
HOST=192.168.10.204
USER=jake
PASS=mantabayray51
pftp -inv $HOST << EOF
user $USER $PASS
binary
cd /home/jake/CaliBot
put cbot.py
exit
EOF
