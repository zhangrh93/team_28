#!/bin/bash
nohup python3 /model/main.py &
nohup python3 Twitter_harvester.py 115.146.86.112 ausCollection aus 4 &
