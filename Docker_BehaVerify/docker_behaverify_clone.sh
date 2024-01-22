#!/bin/bash

docker start behaverify
docker exec behaverify git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
docker exec behaverify bash -c 'echo "!/*" > /home/user/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo "/src" >> /home/user/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo "/metamodel" >> /home/user/behaverify/.git/info/sparse-checkout'
docker exec behaverify bash -c 'echo "/Docker_BehaVerify" >> /home/user/behaverify/.git/info/sparse-checkout'
docker exec -w /home/user/behaverify behaverify git checkout
docker exec behaverify bash -c 'chmod -R +x /home/user/behaverify/Docker_BehaVerify/*.sh'
docker stop behaverify
