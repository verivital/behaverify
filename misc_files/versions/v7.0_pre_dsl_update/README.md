To recreate tests, download the docker file and run the following commands

docker build -t behaverify_img:latest - < Dockerfile
docker container create -i -t --name behaverify behaverify_img
docker start behaverify
docker exec behaverify /minimal_script.sh
docker cp behaverify:/root/behaverify/REPRODUCIBILITY/2022_SEFM/examples/processed_data/. ./processed_data
docker cp behaverify:/root/behaverify/REPRODUCIBILITY/2022_SEFM/examples/results/. ./results


to locally recreate models, navigate to the /REPRODUCIBILITY/2022_SEFM/examples folder, and then run
./generate_minimal.sh

to locally run the tests (once models have been built), navigate to the /REPRODUCIBILITY/2022_SEFM/examples folder, and then run
./run_minimal.sh

to do all of this at once, navigate to the /REPRODUCIBILITY/2022_SEFM/examples folder and then run
./do_minimal.sh


models will be built in /REPRODUCIBILITY/2022_SEFM/examples/EXAMPLE_NAME/models_MODEL_NAME/ where EXAMPLE_NAME is the relevant example, and MODEL_NAME is based on the encoding
results will be placed in /REPRODUCIBILITY/2022_SEFM/examples/results/EXAMPLE_NAME/

These tests run using the code version found in ./src/v6_paper_last_second_fix
The version in v6.5_input_recheck is identical to the total_v3 version in v6, except that it uses IVAR instead of a VAR in some places. Performance is very similar, but slightly favors the VAR variation.
