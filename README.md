# behaverify
behavior tree verification



To recreate tests, download the docker file and run the following commands

docker build -t behaverify_img:latest - < Dockerfile
docker container create -i -t --name behaverify behaverify_img
docker start behaverify
docker exec behaverify /minimal_script.sh
docker cp behaverify:/root/behaverify/examples/processed_data/. ./processed_data
docker cp behaverify:/root/behaverify/examples/results/. ./results