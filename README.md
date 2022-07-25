# behaverify
behavior tree verification



To recreate tests, download the docker file and run the following commands

docker build -t behaverify_img:latest - < Dockerfile
docker container create -i -t --name behaverify behaverify_img
docker start behaverify
docker exec behaverify /minimal_script.sh
docker cp behaverify:/root/behaverify/examples/processed_data/. ./processed_data
docker cp behaverify:/root/behaverify/examples/results/. ./results


to locally recreate models, navigate to the ./examples folder, and then run
./generate_minimal.sh

to locally run the tests (once models have been built), navigate to the ./examples folder, and then run
./run_minimal.sh

to do all of this at once, navigate to the ./examples folder and then run
./do_minimal.sh


models will be built in ./examples/EXAMPLE_NAME/models_MODEL_NAME/ where EXAMPLE_NAME is the relevant example, and MODEL_NAME is based on the encoding
results will be placed in ./examples/results/EXAMPLE_NAME/
