mkdir log
nohup python3 Twitter_harvester.py 115.146.86.112 vicCollection vic 1 & >> ./log/vic.log
nohup watch -n 3600 python3 suburb_crawler.py 115.146.86.112 2 & >> ./log/suburb.log
nohup python3 main.py & >> ./log/main.log