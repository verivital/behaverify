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

These tests run using the code version found in ./src/v6_paper_last_second_fix
The version in v6.5_input_recheck is identical to the total_v3 version in v6, except that it uses IVAR instead of a VAR in some places. Performance is very similar, but slightly favors the VAR variation.



# General Usage

For the most current version, there are 4 python files neccessary to execute BehaVerify. They are

--modifier.py
--node_creator.py
--smv_writer.py
--tree_parser.py

These files are located in ./src. Please note that this version is still being tested. There are errors and inefficiencies.

## tree_parser.py

This is the first file that will be used. It will create a tree object based on the input arguments it receives and the walk this object, gathering relevant information. If an output file is provided, it will write the output to that file. Otherwise, it will print the output.

An example call would be

python3 tree_parser.py file_with_BT.py method_to_create_root --output_file my_output

where

file_with_BT.py is a file provided by the user. This file needs to have a method which when called returns the root of the tree. This method is method_to_create_root. If there are arguments that this method needs, they can be provided using the optional flags --input_args and --input_string_args.

## modifier.py

This is the second file that will be used. It is used to modify the output of tree_parser.py. In the example call, this output was my_output. As this is a text file, it can be modified by hand. However, it may be easier or faster to utilize modifer.py for this task. There are a variety of flags which can be used to mass edit nodes and variables. It is also possible to specify individual nodes/variables to modify.

An example call would be

python3 modifer.py my_output.txt --force_parallel_sync --instruction_file list_of_instructions --output_file my_output2


## smv_writer.py

This is the final file that will be used. It uses the file created by modifier.py (or tree_parser.py, if no editing was required). It will create the actual .smv file to be used by nuXmv. An example call would be

python3 smv_writer.py my_output2 --spec_file ltl_specs --blackboard_output_file my_blackboard --output_file my_output.smv

Various arguments can be provided to smv_writer.py. These include a custom blackboard (this will prevent the smv_writer.py from generating a new blackboard and use the one provided instead), specifications (these are directly copy and pasted into the file), etc.

Various outputs can be requested, allowing for greater reusability.


## node_creator.py

This is used internally. It is required, but you will not use it directly.