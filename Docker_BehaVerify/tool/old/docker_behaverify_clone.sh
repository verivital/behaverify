#!/bin/bash

docker start behaverify
docker exec behaverify git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
docker exec -w '/home/behaverify/behaverify' behaverify git sparse-checkout set --no-cone
docker exec behaverify bash -c 'echo !/* > /home/behaverify/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo /src >> /home/behaverify/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo /metamodel >> /home/behaverify/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo /Docker_BehaVerify >> /home/behaverify/behaverify/.git/info/sparse-checkout'
docker exec -w '/home/behaverify/behaverify' behaverify git checkout
docker exec behaverify bash -c 'chmod -R +x /home/behaverify/behaverify/Docker_BehaVerify/*.sh'
docker exec behaverify bash -c 'chmod -R +x /home/behaverify/behaverify/Docker_BehaVerify/Additional_Files/*.sh'
docker exec behaverify python3 -m venv '/home/behaverify/behaverify_venv'
docker exec behaverify '/home/behaverify/behaverify_venv/bin/python3' -m pip install --upgrade pip
docker exec behaverify '/home/behaverify/behaverify_venv/bin/python3' -m pip install -r '/home/behaverify/behaverify/Docker_BehaVerify/Additional_Files/requirements.txt'
docker stop behaverify
