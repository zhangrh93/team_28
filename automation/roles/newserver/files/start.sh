#!/bin/bash
nohup python3 /home/ubuntu/model/main.py &
nohup python3 /home/ubuntu/harvester/Twitter_harvester.py 115.146.86.112 ausCollection aus 4 &
