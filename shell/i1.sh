mkdir log
nohup python3 -m http.server 8000 & >> ./log/http.log
nohup watch -n 3600 python3 mapReduceResult.py 115.146.86.112 requestCollection ausCollection Australia & >> ./log/aus.log
nohup watch -n 3600 python3 mapReduceResult.py 115.146.86.112 requestCollection vicCollection Victoria & >> ./log/vic.log
nohup watch -n 3600 python3 mapReduceResult.py 115.146.86.112 requestCollection melCollection Melbourne_City & >> ./log/mel.log
nohup watch -n 3600 python3 mapReduceResult.py 115.146.86.112 requestCollection sydCollection Sydney & >> ./log/syd.log
nohup watch -n 3600 python3 suburb_mapReduceResult.py 115.146.86.112 requestCollection suburbCollection & >> ./log/suburb.log
nohup watch -n 3600 python3 getData.py & >> ./log/getData.log