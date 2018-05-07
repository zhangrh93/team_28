mkdir log
nohup python3 Twitter_harvester.py 115.146.86.112 melCollection mel 2 & >> ./log/mel.log
nohup python3 Twitter_harvester.py 115.146.86.112 synCollection syd 3 & >> ./log/syd.log
nohup python3 main.py & >> ./log/main.log