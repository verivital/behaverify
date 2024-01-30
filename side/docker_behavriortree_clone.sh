#!/bin/bash

docker start haskell_behaverify
docker cp ./install_script.sh 'haskell_behaverify:/home/haskell_BehaVerify/install_script.sh'
docker exec haskell_behaverify bash -c 'sudo chmod -R +x /home/haskell_BehaVerify/install_script.sh'
docker exec haskell_behaverify /home/haskell_BehaVerify/install_script.sh
docker stop haskell_behaverify
