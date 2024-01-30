#!/bin/bash

user=$behaverify

docker start behaverify
docker exec behaverify git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
docker exec behaverify bash -c "echo \"!/*\" > /home/${user}/behaverify/.git/info/sparse-checkout"
docker exec behaverify bash -c "echo \"/src\" >> /home/${user}/behaverify/.git/info/sparse-checkout"
docker exec behaverify bash -c "echo \"/metamodel\" >> /home/${user}/behaverify/.git/info/sparse-checkout"
docker exec behaverify bash -c "echo \"/Docker_BehaVerify\" >> /home/${user}/behaverify/.git/info/sparse-checkout"
docker exec -w "/home/${user}/behaverify" behaverify git checkout
docker exec behaverify bash -c "chmod -R +x /home/${user}/behaverify/Docker_BehaVerify/*.sh"
docker exec behaverify python3 -m venv "/home/${user}/behaverify_venv"
docker exec behaverify "/home/${user}/behaverify_venv/bin/python3" -m pip install --upgrade pip
docker exec behaverify "/home/${user}/behaverify_venv/bin/python3" -m pip install -r "/home/${user}/behaverify/Docker_Behaverify/Additional_Files/requirements.txt"
docker stop behaverify
