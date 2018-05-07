mkdir log
nohup python3 Twitter_harvester.py 115.146.86.112 ausCollection aus 0 & >> ./log/aus.log
nohup python3 main.py & >> ./log/main.log