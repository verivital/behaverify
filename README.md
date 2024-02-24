# BehaVerify

BehaVerify is a tool for turning specifications of Behavior Trees into nuXmv models for verification as well as generating Python and Haskell implementations of the specified trees.

To recreate tests, see REPRODUCIBILITY.

Older versions can be found in subfolders of /src/versions/. The documentation for older versions may not be accurate.

# References

Serbinowska, S.S., Johnson, T.T. (2022). BehaVerify: Verifying Temporal Logic Specifications for Behavior Trees. In: Schlingloff, BH., Chai, M. (eds) Software Engineering and Formal Methods. SEFM 2022. Lecture Notes in Computer Science, vol 13550. Springer, Cham. https://doi.org/10.1007/978-3-031-17108-6_19

# Installation/Requirements

We have no reason to believe that BehaVerify would work only on Ubuntu 22.04. However, that is the only system we have tested on.

from apt

- python3=3.10.6-1~22.04
- graphviz=2.42.2-6
- pip=22.02

from pip

- py\_trees=2.2.3
- pandas=2.0.2 <- only relevant for making graphs
- Jinja2=3.1.2
- textX=3.1.1
- matplotlib=3.7.1 <- only relevant for making graphs
- #numpy=1.24.3 <- installed automatically by pandas

from ghcup <- only relevant if generating Haskell files

- GHC=9.2.8
- cabal-install=3.6.2.0

You will also need to download nuXmv (behaverify will generate .smv files even if you don't have nuXmv, but you will not be able to do anything with the .smv files if you don't have nuXmv). nuXmv can be downloaded from https://nuxmv.fbk.eu/

Once all the requirements are downloaded and installed, download this repository (or just the src files in /src along with with /src/haskell\_file and /src/tick\_overwrite and behaverify.tx in /metamodel). 

# General Layout

File extensions are not mandatory. This documentation will use the following convention for them

- .smv -> a file for use with nuXmv
- .tree -> a specification file that follows the rules in /metamodel/behaverify.tx (a textx file)
- .tx -> a metamodel file.

The following files make up BehaVerify and are located in /src

- dsl\_to\_behaverify.py -> Converts .tree files to .smv files
- dsl\_to\_haskell.py -> Converts .tree files to Haskell
- dsl\_to\_python.py -> Converts .tree files to Python (py\_trees)
- behaverify\_common.py -> (Internal use only. Do not interact with)
- behaverify\_to\_smv.py -> (Internal use only. Do not interact with)
- check\_model.py -> (Internal use only. Do not interact with)
- node\_creator.py -> (Internal use only. Do not interact with)
- serene\_functions.py -> (Internal use only. Do not interact with)

Additionally, the files in /src/haskell\_file and /src/tick\_overwrite are used by BehaVerify when generating Haskell files and generating Python files, respectively.

# Generating .smv files for nuXmv

.smv files can be used with nuXmv for model verification. You can generate .smv using the following command:

	python ./src/dsl_to_behaverify.py ./metamodel/behaverify.tx /path/to/tree.tree --output_file /path/to/smv.smv

Assumptions:
1. python refers to python3.
2. you are running this command from the top level of the repository. If not, please adjust paths as necessary.

## Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- --output\_file -> this argument is optional. If it is not provided, the output will be printed to the console. If it is provided, the output will be written to the file location provided. You do not need to make this a .smv file.

## Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --keep\_stage\_0 -> Flag option (no additional information required). This disables the stage\_0 pruning optimization. 
- --keep\_last\_stage -> Flag option (no additional information required). This disables the last\_stage pruning optimization. 
- --do\_not\_trim -> Flag option (no additional information required). This disables node pruning. BehaVerify will not restructure your tree to remove unreachable nodes.

## Using nuXmv for verification

Please run the following command

	/path/to/nuXmv --int /path/to/smv.smv

Here --int will turn this into interactive mode. Now, run the following commands

	go
	check_ctlspec
	check_ltlspec
	check_invar
	quit

go is a command which runs several commands, in preparation of model checking. The check commands check the relevant specifications. If a specification is False, a counterexample will be produced.

# Generating Python Files

Python files can be generated using the following command:

	python ./src/dsl_to_pytree.py ./metamodel/behaverify.tx /path/to/tree.tree /path/to/folder/ fileName 

Assumptions:
1. python refers to python3.
2. you are running this command from the top level of the repository. If not, please adjust paths as necessary.

## Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- /path/to/folder/ -> this argument must point to a folder. This is where the python files will be written.
- fileName -> this should not include any extension. fileName.py, fileName\_environment.py, and fileName\_runner.py will depend upon this name.

Note that various other files will also be created. serene\_safe\_assignment.py is a file that ensures the assignments to variables are valid. Additionally, for each action and check node, a file will be created. 

## Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --max\_iter -> Requires an integer as well. Defaults to 100. This dictates how many iterations fileName\_runner.py will execute.
- --no\_var\_print -> Flag option (no additional information required). This disables the printing of variables.
- --serene\_print -> Flag option (no additional information required). This enables the printing of the status of the tree after each tick.
- --py\_tree\_print -> Flag option (no additional information required). This enables the use of PyTree visualizers to print information about the status of the tree (warning: this does not reflect the status the nodes returned when running, as those nodes are sometimes reset).


## Utilizing the Generated Files

Run

	python /path/to/folder/fileName_runner.py

# Generating Haskell Files

Haskell Files are slightly more irritating to generate and use. First, create a folder where you wish to store your Haskell files. Then use the following command

	cabal init --non-interactive

This will cause cabal to initiate a project in the current folder. Next, run  the following command:

	python ./src/dsl_to_pytree.py ./metamodel/behaverify.tx /path/to/tree.tree /path/to/folder/ fileName 

Assumptions:

1. python refers to python3.
2. you are running this command from the top level of the repository. If not, please adjust paths as necessary.

## Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- /path/to/folder/ -> this argument must point to a folder. The haskell files will be written to /path/to/folder/app/, which was created by cabal init.
- fileName -> this should not include any extension. fileName.hs will depend upon this name.

Note that various other files will also be created. BehaviorTreeBlackboard.hs, BehaviorTreeCore.hs, and BehaviorTreeEnvironment.hs are files necessary for the Behavior Tree. SereneOperation.hs is a file for some additional functions, and SereneRandomizer.hs is a utility file for random functions. Main.hs will run the tree and print information. Additionally, for each action and check node, a file will be created. 

NOTE: cabal is currently utilized because non-determinism depends on the System.Random package, and cabal is the easiest way we found to quickly deal with this.

## Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --max\_iter -> Requires an integer as well. Defaults to 100. This dictates how many iterations Main.hs will execute.

## Utilizing the Generated Files

In /path/to/folder/, run

	cabal run

If you wish to change the randomized starting seeds, use 

	cabal run fileName -- seed1 seed2

(seed1 controls the initial seed for the blackboard, while seed2 controls the initial seed for the environment).


# Creating .tree Files

Please see **/examples/light\_controller/light\_controller.tree** for an example (with comments) that explains what goes into a .tree file.
