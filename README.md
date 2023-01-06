# behaverify
behavior tree verification



To recreate tests, see REPRODUCIBILITY.



# General Usage

The following files make up BehaVerify

--behaverify_common.py (internal use only. do not interact with)

--behaverify_to_dsl.py - Converts behaverify files to DSL templates

--behaverify_to_smv.py - Converts behaverify files to SMV files (for use with nuXmv)

--dsl_to_behaverify.py - Converts DSL files to behaverify files

--dsl_to_python.py - Converts DSL files to python (py_trees)

--modifier.py (NOT CURRENTLY WORKING)

--node_creator.py (internal use only. do not interact with)

--pytree_to_behaverify.py - Converts a py_tree to Behaverify Files

--read_files.py (internal use only. do not interact with)

These files are located in ./src. Please note that this version is still being tested. There are errors and inefficiencies.


# WARNING

Information below is not accurate and has not been updated to the most recent version. 

Quick overview: the newest version utilizes a Domain Specific Language (DSL) as defined in the grammar folder. Eventually, the plan is to be able to create a DSL template from an existing py_trees implementation, but that functionality does not yet exist. Furthermore, owing to some re-writes, it is currently not possible to utilize tree_parser.py to create a modeol directly from an existing py_trees implementation.

Current usage: use dsl_to_python.py in order to create an intermediate file that is used with smv_writer.py to create an smv file for use with nuXmv. 

# NOTE

Some nuXmv functions currently not supported, like exp and ln, because I don't actually know how those functions work. I can't make them work in any examples.

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





# Detailed Documentation



# tree_parser.py


python3 tree_parser.py root_file root_method --root_args ROOT_ARGS --string_args STRING_ARGS --output_file OUTPUT_FILE

## Required Arguments

### root_file

### root_method

The root_file must contain the root_method. When called, the root_method must return a py_trees node. This node will be treated as the root. If additional parameters are required to call this method, please include them using the optional arguments.

## Optional Arguments

### root_args

### string_args

root_args and string_args both accept any number of arguments. Each arg in root_args will be used as an argument in the root_method. It must evaluate to a valid python expression. string_args function in the same way as root_args, but the argument will be passed as a string.

### output_file

The output_file is an optional argument indicating where the output should be written. WARNING: this will overwrite an existing file! If no output_file is provided, the output will be printed.



# modifier.py

## Required Arguments

### input_file

The input_file is where modifier will read it's information from. Most likely, this should be the output of tree_parser.py. The output of modifier.py will be in the same format as the input, so repeated modification is possible.

## Optional Arguments

### output_file

The output_file is an optional argument indicating where the output should be written. WARNING: this will overwrite an existing file! If no output_file is provided, the output will be printed.

### interactive_mode

If this flag is present, modifier.py will enter an interactive mode where the user can modify values via the command prompt. This feature is incomplete, and probably shouldn't be used.

### instruction_file

If an instruction_file is provided, modifier.py will apply every instruction in the file to the provided input. For repeatability reasons, this is probably the best way to use modifier.py. An explanation of how to write an instruction_file can be found below.

## Optional Arguments (global modifications)

The following Optional Arguments will be applied everywhere (where applicable).

### force_parallel_unsynch

Forces each parallel node to be treated as unsynchronized (i.e., without memory).

### force_parallel_synch

Forces each parallel node to be treated as synchronized (i.e., with memory).

### force_selector_memory

Forces each selector node to be treated as a node with memory.

### force_selector_memoryless

Forces each selector node to be treated as a node without memory.

### force_sequence_memory

Forces each sequence node to be treated as a node with memory.

### force_sequence_memoryless

Forces each sequence node to be treated as a node without memory.

### use_next_checks

Forces check_blackboard_variables to use the next value of the variable being checked. Useful if most blackboard variables have their value updated before any relevant checks are applied.

### use_current_checks

Forces check_blackboard_variables to use the current value of the variable being checked. Useful if most blackboard variables have their value updated after any relevant checks are applied.

### best_guess_checks

BehaVerify will attempt to detect when blackboard variables are updated and use a current or next check as appropriate in check_blackbaord_variables. Note: this is not guaranteed to work. Nodes with access may need to be updated for more accurate results.

### min_value

Sets the minimum value for each variable to the provided value.

### max_value

Sets the maximum value for each variable to the provided value.

### init_value

Sets the initial value for each variable to the provided value.

### no_init_value

Removes the initial value for each variable.

### always_exist

Variables are treated as always existing.

### sometimes_exist

Variables will need to be 'initialized'. I.E., until a node sets a value for a variable, it will be marked as not existing. All checks will automatically return False for the variable.

### init_exist

Variables initial exist will be set to this value (note: if variables always exist, this value is ignored).

### no_init_exist

Variables do not have an initial exist value.

### next_exist

If this value is provided, then when a variable's value is updated using anything other than the default case, the variable's exist value will be set to this.

### no_next_exist

Variables will be nondeterministically set to exist or not exist with each update.

### variables_auto_stay

If no node updates the variable's value, then the variable will automatically retain it's current value.

### variables_auto_change

If no node updates the variable's value, then the node will nondeterministically take on a new value.

### use_stages

Variables will be split into stages, allowing much easier modelling for variables which update repeatedly during a single execution. WARNING: greatly increases state space.

### no_stages

Varaiables will not use stages.



# smv_writer.py

## Required Arguments

### input_file

The input containing tree information. Most likely, this should be the output of tree_parser.py or modifier.py

## Optional Arguments

### blackboard_input_file

If this argument is provided, smv_writer.py will not generate a blackbaord file. Instead, it will directly include the contents of blackboard_input_file.

### module_input_file

If this argument is provided, smv_writer.py will not generate additional modules (such as blackboard checks or status setting modules). Instead, it will directly include the contents of module_input_file

### specs_input_file

If this argument is provided, smv_writer.py will include the contents of the file.

### output_file

If this argument is provided, smv_writer.py will write the output to the file. WARNING: this will overwrite existing files. If this argument is not provided, the output will be printed.

### blackboard_output_file

If this argument is provided, smv_writer.py will also write the blackboard to this file. This can then be used as a template to modify the blackboard by hand. The modified blackboard can then be used in subsequent runs as a blackboard_input_file. WARNING: this will overwrite existing files.

### module_output_file

If this argument is provided, smv_writer.py will also write the additional modules to this file. This can then be used as a template to modify the additional modules by hand. The modified modules can then be used in subsequent runs as a module_input_file. WARNING: this will overwrite existing files.








# Instruction File Documentation

The instruction file should be formatted as a list of dictionaries.

## target

Each dictionary needs to contain a 'target' key. There are three valid targets: 'global_flags', 'variable', and 'node'.

### global_flags

If 'target' maps to 'global_flags', then the only other entry in the dictionary should be 'instructions' which maps to a list of global flags to be applied. Most optional arguments (as described above) are accepted.

### variable

If 'target' maps to 'variable', then this dictionary is going to describe what variable is to be modified and how. The dictionary should have the following entries:

#### name

The name of the variable to be modified. This is a string.

#### create (optional)

This indicates that the variable needs to be created. Should map to True

### delete (optional)

This indicates that the variable needs to be deleted. Should map to True

### instructions

A dictionary of modifications to make.

### node

If 'target' maps to 'node', then this dictionary is going to describe what node is to be modified and how. This dictionary should have the following entries:

#### name

The name of the node to be modified

#### instructions

A dictionary of modifications to apply to the node.
