This README is meant to provide information about reproducing results used in the 2024 ANSR project. However, it can also be used as a more general installation guide for BehaVerify, though eventually it may be inadequate for this purpose as it will not be updated along with BehaVerify, in order to ensure it remains useful for its primary purpose, reproduction of results for 2024 ANSR.

# About this File and its Layout

1. Prerequisites and Information -> this section will explain what you need and what assumptions we make.
2. Test Information -> this section provides basic information about the tests.
3. Running Tests using Docker -> this section will explain how to run the tests using Docker.
4. Running Tests Locally (verbose) -> this section will explain how to run tests locally. It also explains why each step of the installation is necessary.
5. Running Tests Locally (concise) -> this section will explain how to run tests locally. It does not provide explanations.
6. Interpreting and Comparing Results -> this section will explain how to interpret the generated results and what they correspond to in the paper.
7. Potential Errors and Workarounds -> this section will explain how to deal with some of the potential errors encountered.
8. Directory Explained -> this section will provide detailed information about everything in this directory.

Finally, note that this is a .md file, and as such, we escape various characters. If you are reading this using a text editor, please make sure to keep this in mind.

# Prerequisites and Information

1. docker with the ability to run commands as a regular user (see https://docs.docker.com/engine/install/linux-postinstall/ ). Additionally, we will be using Ubuntu 23.10 inside docker. Some users appear to have issues with running commands like update or upgrade in docker when using Ubuntu; we do not have a workaround for this.
2. nuXmv (see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz ). You only need to download nuXmv. There should be no installation. Please ensure you download the Linux 64-bit x86 version 2.1.0. The executable will be located in **nuXmv-2.1.0-linux64/nuXmv-2.1.0-Linux/bin/nuXmv**. There should be **NO FILE EXTENSION**. Note that we are **ONLY** interested in the binary; you do not need the other files or the folder structure, so long as you have the binary.
3. If you choose to use Docker, we assume you have access to Python3. If you choose to run locally, we assume you are able to run bash scripts. These have **only been tested on Ubuntu**. If you cannot run the scripts, please run the commands present in the bash scripts manually. Note that this will require arguments to replaced. Specifically, $1 means the first argument provided to the bash script, $2 means the second argument provided to the bash script, etc.

Note, we require docker py for use with python3 if using docker. It can be installed using
```
python3 -m pip install docker
```

## nuXmv

Per the licensing agreement of nuXmv (see https://nuxmv.fbk.eu/downloads/LICENSE.txt ), we may not re-distribute the software in any form for any purpose. As such, while we appreciate that downloading nuXmv separately is tedious and means that this artifact is somewhat incomplete, we do not have any alternative available to us. Thank you for understanding.


# Test Information

1. Installation Test is mostly to test installation. It is very fast.
2. Full Results replicates all results that do not timeout.
3. Timeout Results replicates all results, including those that timeout.

---

# Running Tests With Docker

The tests can be run using docker. We provide several methods for doing this. Some utilize a prebuilt docker image, while others rebuild the image. If this is part of an artifact evaluation, we will provide a docker image.

## Single Script Options

- Build Scripts -> These scripts use the Dockerfile to build a new image and then create a container.

We provide 3 scripts of each type (1 for each test from Test Information). Each of these scripts takes four command line arguments, three of which are the same.
	
- **/path/to/Dockerfile/Folder/** -> This should point to the folder containing the Dockerfile.
- **/path/to/DockerImage** -> This should point to the Dockerimage.
- **/path/to/nuXmv** -> This should point to the executable you downloaded as a prerequisite. There should be no file extension.
- **mode** -> Required, sort of. This should be **install**, **partial**, or **full**. 
- **/path/to/output** -> The output will be copied to /path/to/output.tar. This will not override existing files, so make sure there is no existing file.

After each command, we provide an example command that assumes you placed the nuXmv binary in the top level of the reproducibility directory (the directory containing the Dockerfile). **THE EXAMPLES ASSUME YOU ARE IN THE DIRECTORY NAMED 2024\_ANSR**

### Single Script: Minimal 

Build Script:
```
python3 build_and_run.py /path/to/Dockerfile/Folder/ /path/to/nuXmv install /path/to/output
```
	
Build Example:
```
python3 ./python_script/build_and_run.py ./ ./nuXmv install ./install
```
	
The results will be written in **/path/to/output.tar**. Extract the archive and see the Interpreting and Comparing Results section for more information.

### Single Script: Full

Build Script:
```
python3 build_and_run.py /path/to/Dockerfile/Folder/ /path/to/nuXmv full /path/to/output
```
	
Build Example:
```
python3 ./python_script/build_and_run.py ./ ./nuXmv full ./full
```
	
The results will be written in **/path/to/output.tar**. Extract the archive and see the Interpreting and Comparing Results section for more information.

### Single Script: Timeout

Build Script:
```
python3 build_and_run.py /path/to/Dockerfile/Folder/ /path/to/nuXmv timeout /path/to/output
```
	
Build Example:
```
python3 ./python_script/build_and_run.py ./ ./nuXmv timeout ./timeout
```
	
The results will be written in **/path/to/output.tar**. Extract the archive and see the Interpreting and Comparing Results section for more information.

---

## Step by Step Docker instructions

This section will explain how to utilize either the provided docker image or Dockerfile to recreate the tests using docker. After each command, we provide an example command that assumes you placed the nuXmv binary in the top level of the reproducibility directory (the directory containing the Dockerfile). **THE EXAMPLES ASSUME YOU ARE IN THE DIRECTORY NAMED 2024\_ANSR.**

### 1. Creation of the Docker Image and Container

You only need to execute 1a or 1b. See 1b for steps using the image. However, should you wish to build the docker image yourself, please run
```
python3 reinstall.py /path/to/Dockerfile/folder
```

Example:
```
python3 ./python_script/reinstall.py ./
```

This will create a docker image named behaverify\_img with the tag latest. It will then also create a container named behaverify\_2024\_ansr from that image.

### IMPORTANT:
The scripts below assume that the docker container is named behaverify\_2024\_ansr. If you run step 1, this will be handled.

### 2. Addition of nuXmv (estimated time: 30 seconds)

Next, please run
```
python3 add_nuxmv.py /path/to/nuXmv
```

Example:
```
python3 ./python_script/add_nuxmv.py ./nuXmv
```

This will copy nuXmv from the path you provided to the correct location in the docker and ensure it is runable and an executable. Note that you should not point to the folder containing nuXmv, but to nuXmv itself, and that the nuXmv version should be the Linux version.

### 3. Install Test

The full test takes quite a while to run. To ensure everything works right, please run
```
python3 generate.py install /path/to/output
```

Example:
```
python3 ./python_script/generate.py install ./install
```

### 4. Full Test 

It doesn't take terribly long to generate all the results that do not timeout, but it will probably be at least a half hour.
```
python3 generate.py full /path/to/output
```

Example:
```
python3 ./python_script/generate.py full ./partial
```


### 5. Timeout Results

Warning, these tests take a **very** long time to complete (many hours).
```
python3 generate.py timeout /path/to/output
```

Example:
```
python3 ./python_script/generate.py timeout ./timeout
```

---

# Verbose Installation for Running tests locally without docker.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Some of the scripts are likely to break on other systems. For instance, the scripts assume that nuXmv will be named nuXmv, and not nuXmv.exe. However, our code itself should still work (though we have not tested this).

This section is intentionally lengthy. If you are not interested in the details and just want the commands, please scroll down further


1. nuXmv<br />Please download nuXmv (see  https://nuxmv.fbk.eu/ ). You only need to download nuXmv. There should be no installation. Download the relevant version for your system. It should be version 2.1.0. The download will include many files. You only need the executable (no file extension). See above for more information.
2. Updating<br /> We suggest running the following commands.

		sudo apt update
		sudo apt upgrade
3. Python3<br />Python3 is used to run BehaVerify. As such, it is necessary. If you already have python3 installed, skip the following step. If not, run
	
		sudo apt install python3
4. pip<br />pip is used to install other python packages. If you already have pip installed (for python3), skip the following step. If not, run

		sudo apt install pip
5. PyTrees<br />PyTrees is used in the generated python code. It is necessary for the differential testing experiments, or for using generated python code in general.

		python3 -m pip install py_trees
6. pandas<br />pandas is used for data gathering and displaying. It is necessary for graph and table creation.

		python3 -m pip install pandas
7. jinja2<br />jinja2 is used by something for graph/table creations.

		python3 -m pip install jinja2
8. textX<br />textX is used by BehaVerify for parsing. It is necessary for BehaVerify to run in any capacity

		python3 -m pip install textX
9. matplotlib<br />matplotlib is used for generating graphs and plots.

		python3 -m pip install matplotlib
10. graphviz<br />graphviz is used to generate graphs and plots.

		sudo apt install graphviz
11. git<br />git is used to download our repository. If you would prefer to manually download our repository, you can skip this step.

		sudo apt install git
12. (OPTIONAL) Haskell prerequisites<br />These are prerequisites required by Haskell. **THESE STEPS ARE UNNECESSARY FOR FMAS RESULTS**

		sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5
13. (OPTIONAL) Additional Haskell prerequisite<br />

		sudo apt install libgmp3-dev
14. (OPTIONAL) GHCUP<br />Please follow the instructions at https://www.haskell.org/ghcup/ to install GHCUP, Haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked.
15. (OPTIONAL) GHCUP upgrade<br />This will upgrade GHCUP.

		ghcup upgrade
16. (OPTIONAL) Cabal<br />This will install and set the specific version of cabal we used. Most likely, everything will work with a different version.

		ghcup install cabal 3.6.2.0
		ghcup set cabal 3.6.2.0
17. (OPTIONAL) GHC<br />This will install and set the specific version of ghc we used. Most likely, everything will work with a different version.

		ghcup install ghc 9.2.8
		ghcup set ghc 9.2.8
18. BehaVerify<br />Download our repository. If you did not install git, please download manually. If you installed git

		git clone https://github.com/verivital/behaverify
19. Enable scripts<br />This will allow all the necessary scripts to run. Please navigate to the top level of our repository and run the following

		sudo chmod -R +x ./REPRODUCIBILITY/2024_ANSR/*.sh
20. Move nuXmv<br />You downloaded nuXmv in step 1. Please place it in behaverify/REPRODUCIBILITY/2024\_ANSR/
21. Enable nuXmv<br />Please navigate to the top level of our repository and run the following

		sudo chmod +x ./REPRODUCIBILITY/2024_ANSR/nuXmv


You are now ready to run the scripts locally. Scroll past the concise installation instructions to see the scripts explanation.

---

# Concise Installation for Running the tests locally without docker.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Some of the scripts are likely to break on other systems. For instance, the scripts assume that nuXmv will be named nuXmv, and not nuXmv.exe. However, our code itself should still work (though we have not tested this).


Please download nuXmv (see  https://nuxmv.fbk.eu/ ). You only need to download nuXmv. There should be no installation. Download the relevant version for your system. It should be version 2.1.0.
```
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install pip
```
	
(OPTIONAL) PyTrees is required to use the python code generated by BehaVerify. However, this is not used in the FMAS tests
```
python3 -m pip install py_trees
```
	
Below we have more mandatory requirements
```
python3 -m pip install pandas
python3 -m pip install jinja2
python3 -m pip install textX
python3 -m pip install matplotlib
sudo apt install graphviz
sudo apt install git
```
	
(OPTIONAL) These are prerequisites for Haskell, which is not used in the FMAS tests.
```
sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5
sudo apt install libgmp3-dev
```

(OPTIONAL) Please follow the instructions at https://www.haskell.org/ghcup/ to install ghcup, Haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked.
```
ghcup upgrade
ghcup install cabal 3.6.2.0
ghcup set cabal 3.6.2.0
ghcup install ghc 9.2.8
ghcup set ghc 9.2.8
```
	
You may clone or download the repository
```
git clone https://github.com/verivital/behaverify
```

Please navigate to the top level of our repository and run the following
```
sudo chmod -R +x ./REPRODUCIBILITY/2024_ANSR/*.sh
```

You downloaded nuXmv earlier. Please place it in behaverify/REPRODUCIBILITY/2024\_FMAS/

Please navigate to the top level of our repository and run the following
```
sudo chmod +x ./REPRODUCIBILITY/2024_ANSR/nuXmv
```

You are now ready to run the scripts locally. 


---

# Running Tests Locally without docker (requires installation, see above).

Note that each script will erase all the relevant results before running, to ensure that the results which exist after the script runs are accurate to that script. Thus if you wish to save the results, please move them before running another script.

## Minimal Script

To test everything is working, please navigate to behaverify/REPRODUCIBILITY/2024\_ANSR/ and run the following
```
./behaverify_2024_ANSR_test_installation.sh ./
```

This will run a fairly small script. The results will be in behaverify/REPRODUCIBILITY/2024\_ANSR/examples/. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.

## Full Script

To create a subset of the results, please navigate to behaverify/REPRODUCIBILITY/2024\_ANSR/ and run the following
```
./behaverify_2024_ANSR_full_results.sh ./
```

This will run a larger, but still fairly small script. The results will be in **behaverify/REPRODUCIBILITY/2024\_ANSR/examples/**. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.

## Timeout Script

To create all results, please navigate to behaverify/REPRODUCIBILITY/2024\_ANSR/ and run the following
```
./behaverify_2024_ANSR_timeout_results.sh ./
```

This will run a large script. The results will be in **behaverify/REPRODUCIBILITY/2024\_ANSR/examples/**. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.


---

# Interpreting and Comparing Results

Upon completing any of the test scripts, you should find that /path/to/writable/location/ has a folder containing the results. The name of this folder depends on which test was run. See the specific tests for details. Within this folder, you should find the following folders, each of which corresponds to an experiment:

- bigger\_fish -> This is the Bigger Fish experiment. See **Section 7.1**.
- ISR -> This is the ISR experiment. See **Section 4.4** and **Section 7.3**.
- simple\_robot -> This experiment is the Simple Robot experiment. See **Section 7.2**.
- clean_all.sh -> This is a script for removing results. Ignore it.

## Install Test

The install test can only be used to confirm the installation worked. **THE IMAGES WILL ONLY HAVE A SINGLE DATA POINT EACH.**

### What to look for

As mentioned, you will not be able to find anything to compare. However, please confirm that the following files exist:

- **bigger\_fish/processed\_data/pictures/bigger\_fish/bigger\_fish_ltl.png** -> The key will include full\_opt and full\_opt\_CHANGED; each will have a single data point.
- **simple\_robot/processed\_data/pictures/simple\_robot\_ltl.png** -> The key will include full\_opt and full\_opt\_CHANGED; each will have a single data point.

## Partial Test

The partial test is between the install and full test. Some, but not all, of the results in the paper are generated through this test.

The results should be in **/path/to/output/extracted/examples/**.

### What to look for

- **bigger\_fish/processed\_data/pictures/full\_opt/bigger\_fish\_ltl.png** -> This will have some of the timing results for BehaVerify used for the Bigger Fish experiment. See **Section 7.1**, **Figure 5**. The key will include full\_opt and full\_opt\_CHANGED; note that this does **not** include the timing results for MoVe4BT. As such, the scale may look different. This is a timing experiment, so the results may differ somewhat.
- **simple\_robot/processed\_data/pictures/simple\_robot\_ltl.png** -> This will have some of the timing results for BehaVerivy used for Simple Robot experiment. See **Section 7.2**, **Figure 7**. The key will include full\_opt and full\_opt\_CHANGED; note that this graph does **not** include the timing results for MoVe4BT. As such, the scale may look different. This is a timing experiment, so the results may differ somewhat.

## Full Test

The Full test generates all the results used in the paper, but does not include MoVe4BT.

The results should be in **/path/to/output/extracted/examples/**.

### What to look for


- **bigger\_fish/processed\_data/pictures/full\_opt/bigger\_fish\_ltl.png** -> This will have all of the timing results for BehaVerify used for the Bigger Fish experiment. See **Section 7.1**, **Figure 5**. The key will include full\_opt and full\_opt\_CHANGED; note that this does **not** include the timing results for MoVe4BT. As such, the scale may look different. This is a timing experiment, so the results may differ somewhat.
- **ISR/processed\_data/pictures/counterexample\_for\_5/11x11\_line.png** -> This should correspond to **Section 7.3**, **Figure 8**.
- **simple\_robot/processed\_data/pictures/simple\_robot\_ltl.png** -> This will have all of the timing results for BehaVerivy used for Simple Robot experiment. See **Section 7.2**, **Figure 7**. The key will include full\_opt and full\_opt\_CHANGED; note that this graph does **not** include the timing results for MoVe4BT. As such, the scale may look different. This is a timing experiment, so the results may differ somewhat.

---

# Potential Errors and Workarounds

1. If a script fails because permission has been denied, please run the script without sudo (running docker without sudo requires some configuration). If the problem persists, please try a different location, as occasionally docker cannot write to secondary disks.
2. If building from the Dockerfile fails, please try and use the load option instead.
3. If building from the Dockerfile fails and the load option is not available, please consider running **clean\_docker.sh**. THIS WILL REMOVE ALL EXISTING DOCKER CONTAINERS AND IMAGES. This sometimes seems to help.
4. If everything runs to completion, but there are no images in the copied directory, please confirm if there are files in the results folders (e.g., **bigger\_fish\_selector/results/**). If there are, then most likely you encountered errors similar to the following during execution:
   ```
   OpenBLAS blas_thread_init: pthread_create failed for thread 1 of 16: Operation not permitted
   ```
   Note that this error would not prevent the scripts from completing; it would only prevent the generation of graphs and tables. The internet suggests upgrading your docker version (we tested using docker version 20.10.24, build 297e128). Alternatively, you may by manually compile the results into graphs by calling the scripts at https://github.com/verivital/behaverify/tree/main/REPRODUCIBILITY/2024_FMAS/scripts/process_results_scripts . These scripts must be run from the directory they are in and assume the repository structure exists.

---

# Directory Explained

- **BehaVerify\_2024\_FMAS\_SBT\_full\_results.sh** -> This is the script to locally run everything for the FMAS results. It is also used by the docker scripts.
- **BehaVerify\_2024\_FMAS\_test\_installation.sh** -> This is the script to locally test the install. It is also used by the docker scripts.
- **BehaVerify\_2024\_FMAS\_partial\_results.sh** -> This is the script to locally run almost everything for the FMAS results. It is also used by the docker scripts.
- **Dockerfile** -> This is a Dockerfile for BehaVerify 2024 FMAS edition.
- **nuXmv** -> This doesn't exist but you should make it exist if you plan to run tests locally.
- **README.md** -> Hello there!
- **version\_info.txt** -> Information about what versions of stuff was used.
- **examples** -> This contains the Experiments to be run
	- **clean\_all.sh** -> This is used to remove all existing experiment results.
	- **bigger\_fish\_selector** -> This contains the Bigger Fish experiment.
		- **create\_bigger\_fish.py** -> This is used to generate the DSL files for the bigger fish experiment.
		- **processed\_data/pictures/opt** -> This will contain the graphs with timing and state results.
		- **processed\_data/tables/opt** -> This will contain the tables with timing and state results.
		- **results** -> This will contain the outputs of nuXmv.
		- **smv** -> This will contain the nuXmv models generated by BehaVerify.
	- **ISR** -> This contains the ISR experiment
		- **ISR\_5.tree** -> This is the DSL specification for when the target can move every 5 turns.
		- **ISR\_10.tree** -> This is the DSL specification for when the target can move every 10 turns.
		- **parse\_nuxmv\_output.py** -> This is used to visualize the counterexample.
		- **parse\_python\_output.py** -> This is used to visualize a random trace. This was used to generate **Section 4.4**, **Figure 3**. It is not used in the tests.
		- **processed\_data/pictures** -> This will contain the counterexample visualization.
		- **results** -> This will contain the outputs of nuXmv.
		- **smv** -> This will contain the nuXmv models generated by BehaVerify.
		- **tree** This will contain the DSL specifications for the Bigger Fish models.
	- **simple\_robot** -> This contains the Simple Robot experiment.
		- **make\_tree.py** -> This is used to generate the DSL files for the simple robot experiment.
		- **parse\_python\_output.py** -> This is used to visualize a random trace. This was used to generate **Section 7.3**, **Figure 8**, left half. It is not used in the tests.
		- **template.tree** -> This is an incomplete DSL file that is used by make\_tree.py.
		- **processed\_data/pictures/opt** -> This will contain the graphs with timing and state results.
		- **processed\_data/tables/opt** -> This will contain the tables with timing and state results.
		- **results** -> This will contain the outputs of nuXmv.
		- **smv** -> This will contain the nuXmv models generated by BehaVerify.
		- **tree** This will contain the DSL specifications for the Bigger Fish models.
- **metamodel/behaverify.tx** -> This is the file containing the structure of the DSL. TextX uses it to parse .tree files.
- **python\_scripts** -> These are used to control docker.
- **scripts** -> This folder contains various scripts for building and running experiments. We will not describe all of them.
- **src** -> This contains the source code for BehaVerify.
  - **behaverify\_common.py** -> This contains methods used by multiple parts of BehaVerify.
  - **behaverify\_gui.py** -> This can be used to run a basic GUI for BehaVerify. It's main use is tree visualization and generating visualizations of trace counterexamples.
  - **behaverify\_to\_smv.py** -> This is used by dsl\_to\_nuxmv.py to write the nuXmv model.
  - **check\_grammar.py** -> This is used to ensure the user didn't do anything weird in the DSL model (e.g. True + 3 + 'hello').
  - **dsl\_to\_haskell.py** -> This is used to generate Haskell code from a DSL file.
  - **dsl\_to\_nuxmv.py** -> This is used to generated a nuXmv model from a DSL file.
  - **dsl\_to\_python.py** -> This is used to generate Python code from a DSL file.
  - **node\_creator.py** -> This is used by behaverify\_to\_smv.py to create certain elements of the nuXmv model.
  - **serene\_functions.py** -> This is used to 'compile' certain computations in a DSL file. 
  - **alternative\_printing** -> This is used to augment how PyTrees prints information, to improve debugging.
  - **haskell\_file** -> This is used with haskell code generation.
  - **tick\_overwrite** -> This is used to augment how PyTrees prints information, to improve debugging.

---

# Code Explanation

For an explanation on how to run our code, see our github repository https://github.com/verivital/behaverify
