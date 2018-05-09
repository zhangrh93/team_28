"""
Team 28
Ruihan Zhang 865529
Linrong Chen 854645
Ming Yin 816159
Hongyun Ma 805266
Jinge Zhang 769474
"""

import boto
import time
import os
from boto.ec2.regioninfo import RegionInfo

access_key_id = 'XXXXXXXXXXXXXXXXXXXXXXX'
secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXX'
primary_ip = "XXX.XXX.XXX.XXX"

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ec2_conn = boto.connect_ec2(aws_access_key_id=access_key_id,
                            aws_secret_access_key=secret_access_key,
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/services/Cloud',
                            validate_certs=False)
print("connected with nectar\n")

def create_instances(conn):
    ip_pool = []
    for i in range(2):
        reservation = conn.run_instances('ami-00003837',
                                         key_name='peppa',
                                         placement='melbourne-qh2',
                                         instance_type='m2.small',
                                         security_groups=['ssh'])
        instance = reservation.instances[0]
        name = "Node"+str(i+1)
        print("instance: {} creating".format(name))

        while instance.state != "running":
            time.sleep(0.5)
            instance.update()

        ip = instance.private_ip_address
        ip_pool.append(ip)
        print("build complete, ip address: {}\n".format(ip))

    print("all instances created\n")
    return ip_pool

ip_pool = create_instances(ec2_conn)

# dynamically create inventory file for ansible
with open("inventory.ini","w") as f:
    f.write("[newserver]\n")
    f.write(ip_pool[0] + "\n")
    f.write(ip_pool[1] + "\n\n")
    f.write("[primary]\n")
    f.write(primary_ip + "\n\n")
print("ansible inventory file created\n")

# create variables for ansible roles

current_dir = os.path.dirname(os.path.abspath(__file__))
var_path = os.path.join(current_dir,"roles","primary","defaults","main.yml")
with open(var_path,"w") as f:
    f.write("host1: " + ip_pool[0] + ":27017\n")
    f.write("host2: " + ip_pool[1] + ":27017")
print("ansible variables created")
