# behaverify
behavior tree verification



To recreate tests, see REPRODUCIBILITY.

Older versions can be found in subfolders of ./src/. The documentation for older versions may not be accurate.


# Installation/Requirements

textx

python3.10

you will also need to download nuXmv (behaverify will generate .smv files even if you don't have nuXmv, but you will not be able to do anything with the .smv files if you don't have nuXmv).

py_trees (only necessary if you're using the py_trees to .smv function)


# General Usage

File extensions are not mandatory. This documentation will use the following convention for them

-- .behave - an intermediate file that BehaVerify creates.
-- .bt - a specification file that follows the rules in ./metamodel/btree/btree.tx (a textx file)
-- .smv - a file for use with nuXmv
-- .tree - a specification file that follows the rules in ./metamodel/behaverify.tx (a textx file)
-- .tx - a metamodel file. The two relevant ones are ./metamodel/behaverify.tx and ./metamodel/btree/btree.tx


The following files make up BehaVerify

--behaverify_common.py (internal use only. do not interact with)

--behaverify_to_dsl.py - Converts .behave files to .tree templates

--behaverify_to_smv.py - Converts .behave files to .smv files (for use with nuXmv)

--btree_dsl_to_behaverify.py - Converts .bt files to .behave files

--dsl_to_behaverify.py - Converts .tree files to .behave files

--dsl_to_python.py - Converts .tree files to python (py_trees)

--node_creator.py (internal use only. do not interact with)

--pytree_to_behaverify.py - Converts a py_tree to .behave

These files are located in ./src.

## Suggested Use

There are five main ways to go about using Behaverify.

### .tree to .smv

In this case, the user begins by creating a .tree file that follows the rules specified in ./metamodel/behaverify.tx. Assuming the user is at the top level directory of this repository and their tree is named ex.tree, the user will then execute the following commands

python ./src/dsl_to_behaverify.py ./metamodel/behaverify.tx ex.tree --output_file ex.behave

python ./src/behaverify_to_smv.py ex.behave --output_file ex.smv

And at this point, the user may use the ex.smv file with nuXmv.

### .bt to .smv

FOR A DETAILED GUIDE TO CREATING A .BT FILE, SEE ./metamodel/btree/README.md

In this case, the user begins by creating a .tree file that follows the rules specified in ./metamodel/btree/btree.tx. Assuming the user is at the top level directory of this repository and their tree is named ex.tree, the user will then execute the following commands

python ./src/btree_dsl_to_behaverify.py ./metamodel/btree/btree.tx ex.tree --output_file ex.behave

python ./src/behaverify_to_smv.py ex.behave --output_file ex.smv

And at this point, the user may use the ex.smv file with nuXmv.


### .tree to py_tree

In this case, the user begins by creating a .tree file that follows the rules specified in ./metamodel/behaverify.tx. Assuming the user is at the top level directory of this repository and their tree is named ex.tree, the user will then execute the following command

python ./src/dsl_to_pytree.py ./metamodel/behaverify.tx ex.tree ex.py path_to_output_directory

And at this point, ex.py and other required .py files will be present in the specified output_directory. ex.py will contain exactly 1 method, create_tree() which returns the root node of the py_tree.


### py_trees to .tree

In this case, the user starts with a py_tree. In order for this to function, there must be a method which returns the root node of the tree. Assuming that the user is at the top level directory of this repository, their py_tree is in ex.py, and ex.py has a method called create_root(required_args, optional_args), then the user will execute the following commands

python ./src/pytree_to_behaverify.py ex.py create_root --root_args some_arg1 some_arg2 --string_args some_string_arg some_string_arg2 --output_file ex.behave
python ./src/behaverify_to_dsl.py ex.behave --output_file ex.tree

And at this point the ex.tree file will be ready to be modifed by the user. Note that some modification will likely be required in order to ensure the ex.tree file actually works as intended.


### py_tree to .smv

In this case, the user starts with a py_tree. In order for this to function, there must be a method which returns the root node of the tree. Assuming that the user is at the top level directory of this repository, their py_tree is in ex.py, and ex.py has a method called create_root(required_args, optional_args), then the user will execute the following commands

python ./src/pytree_to_behaverify.py ex.py create_root --root_args some_arg1 some_arg2 --string_args some_string_arg some_string_arg2 --output_file ex.behave
python ./src/behaverify_to_smv.py ex.behave --output_file ex.smv

And at this point the ex.smv file will be ready for use with nuXmv. Note that most likely the model will not accurately reflect the original py_tree, as information regarding blackboard variables and leaf nodes is unlikely to be fully captured. It is instead suggested to use a .tree file. If no .tree file exists, a template may be created using the py_trees to .tree method described above.


# File Explanations

## behaverify_to_dsl.py

The only reason to use this is if a .behave file was generated from a py_tree, in which case a .tree file can be generated. The generated file will not match the py_tree, nor is it guaranteed to be correct (i.e, attempting to use it out of the box may cause errors). The purpose is to save time in writing the .tree file.

### Required Arguments

- input file - a .behave file.

### Optional Arguments

- output_file - where the .tree file will be written

python behaverify_to_dsl.py ex.behave --output_file ex.tree


## behaverify_to_smv.py

This converts a .behave file to .smv for use with nuXmv.


### Required Arguments

- input file - a .behave file

### Optional Arguments

- output_file - where the .smv file will be written

- specs_input_file - additional INVAR/LTL/CTL specifications to copy in. Note that if the .tree file was generated using dsl_to_behaverify.py, then  these can instead be written into the .tree file.

- do_not_trim - a flag. if present, behaverify will not remove unreachable nodes or correct for composite nodes with only 1 child.

python behaverify_to_smv.py ex.behave --output_file ex.smv


## btree_dsl_to_behaverify.py

This converts a .bt file to .smv for use with nuXmv.

### Required Arguments

- metamodel file - a .tx file. In this case, ./metamodel/btree/btree.tx should be used.

- input file - a .bt file which follows the rules described in the metamodel file

### Optional Arguments

- keep_stage_0 - a flag. if present, behaverify will not perform an optimization which removes stage_0 of variables.

- output_file - where the .behave file will be written

python btree_dsl_to_behaverify.py /path/to/btree.tx ex.bt --output_file ex.behave


## dsl_to_behaverify.py

This converts a .behave file to .smv for use with nuXmv.

### Required Arguments

- metamodel file - a .tx file. In this case, ./metamodel/behaverify.tx should be used.

- input file - a .tree file which follows the rules described in the metamodel file

### Optional Arguments

- keep_stage_0 - a flag. if present, behaverify will not perform an optimization which removes stage_0 of variables.

- output_file - where the .behave file will be written

python dsl_to_behaverify.py /path/to/behaverify.tx ex.tree --output_file ex.behave


## dsl_to_pytree.py

This converts a .behave file to a .py file.

### Required Arguments

- metamodel file - a .tx file. In this case, ./metamodel/behaverify.tx should be used

- model file - a .tree file that follows the rules described in the metamodel file

- output file - the name of the main python file to be used. Note that this should just be a name, something like ex.py. No path information should be included

- location - the path to a directory where the files should be output.

python dsl_to_pytree.py /path/to/behaverify.tx ex.tree ex.py /path/to/output/

## pytree_to_behaverify.py

This converts a pytree to a .behave file.

### Required Arguments

- root file - a .py file.

- root method - a method in the root file which returns the root node of the pytree to convert

### Optional Arguments

- root args - any number of arguments (space separated). Each argument will be passed, in order, to the root method

- string_args - any number of arguments (space separated). Each argumenty will be surrounded by quotation marks and then passed, in order, to the root method

- output_file - where the .behave file will be written

python pytree_to_behaverify.py ex.py create_root --output_file ex.behave
