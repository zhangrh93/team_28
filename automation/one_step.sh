#!/bin/bash
eval 'ssh-agent'
ssh-add ~/.ssh/pegga

python create_instance.py
ansible-playbook -i inventory.ini deploy.yml
