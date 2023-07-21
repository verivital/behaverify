See version\_info.txt for information about dependency requirements.

# About this File and its Layout

1. Prerequisites and Information -> this section will explain what you need and what assumptions we make.
2. Test Information -> this section provides basic information about the tests.
3. Running Tests using Docker -> this section will explain how to run the tests using Docker.
4. Running Tests Locally (verbose) -> this section will explain how to run tests locally. It also explains why each step of the installation is necessary.
5. Running Tests Locally (concise) -> this section will explain how to run tests locally. It does not provide explanations.
6. Interpreting and Comparing Results -> this section will explain how to interpret the generated results and what they correspond to in the paper.

Finally, note that this is a .md file, and as such, we escape various characters. If you are reading this using a text editor, please make sure to keep this in mind.

# Prerequisites and Information

1. docker with the ability to run commands as a regular user (see https://docs.docker.com/engine/install/linux-postinstall/ )
2. nuXmv (see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.0.0-linux64.tar.gz ). Please ensure you download the Linux 64-bit x86 version 2.0.0 (October 14, 2019). The downloaded file should be **nuXmv-2.0.0-linux64.tar.gz**. Please extract this. After extracting, the executable will be located in **nuXmv-2.0.0-linux64/nuXmv-2.0.0-Linux/bin/nuXmv**. There should be **NO FILE EXTENSION**. This is the file we are interested in and will refer to later. We only want the executable, and are uninterested in the other files, folders, etc.

## Additional Assumption

The scripts assume you are able to run bash scripts. If you cannot, please run the commands present in the bash scripts manually. Note that this will require arguments to replaced. Specifically, $1 means the first argument provided to the bash script, $2 means the second argument provided to the bash script, etc.

# Test Information

1. The Minimal Test is mostly to test installation. However, it can also be used to confirm information for Light Controller and BlueROV. 
2. The Partial Test fully runs the Bigger Fish experiment, BlueROV, and Light Controller. It runs 20 random iterations of the Differential Testing. It does not meaningfully run the Simple Robot experiment.
3. The Full test replicates all results.

As some installations seem to have trouble with Haskell, we have provided the option to not install Haskell in docker and to not run Haskell in the subsequent tests.

---

# Running Tests With Docker

The tests can be run using docker. We provide several methods for doing this. Some utilize the provided docker image, while others rebuild the image. 

## Single Script Options

- Build Scripts -> These scripts use the Dockerfile to build a new image and then create a container. These scripts must be run in the same folder as the Dockerfiles (Dockerfile.haskell and Dockerfile.no_haskell).
- Load Scripts -> These scripts load the provided image and then create a container. These scripts must be run in the same folder as behaverify_image.tar. The load scripts will always use Haskell.

We provide 3 scripts of each type (1 for each test from Test Information). Each of these scripts takes two command line arguments.
	
- **/path/to/nuXmv** -> This should point to the executable you downloaded as a prerequisite. There should be no file extension.
- **/path/to/writable/location/** -> NOTE: the '/' at the end is required! This should point to a folder where the results will be written.

If a script fails because permission has been denied, please run the script without sudo (running docker without sudo requires some configuration). If the problem persists, please try a different location, as occasionally docker cannot write to secondary disks.

### Single Script: Minimal (about 10 minutes)

Build Script (using Haskell):

	./build_and_run_minimal.sh /path/to/nuXmv /path/to/writable/location/
	
Build Script (without Haskell):

	./build_and_run_minimal.sh /path/to/nuXmv /path/to/writable/location/ no_haskell

Load Script:

	./load_and_run_minimal.sh /path/to/nuXmv /path/to/writable/location/
	
The results will be written in **/path/to/writable/location/behaverify\_install\_test\_results**. See the Interpreting and Comparing Results section for more information.

Note that the '/' at the end of the location is required.

### Single Script: Partial (about 25 minutes)

Build Script (using Haskell):

	./build_and_run_partial.sh /path/to/nuXmv /path/to/writable/location/

Build Script (without Haskell):

	./build_and_run_partial.sh /path/to/nuXmv /path/to/writable/location/ no_haskell

Load Script:

	./build_and_run_partial.sh /path/to/nuXmv /path/to/writable/location/
	
The results will be written in **/path/to/writable/location/behaverify\_partial\_results**. See the Interpreting and Comparing Results section for more information.

Note that the '/' at the end of the location is required.

### Single Script: Full (under 12 hours)

Build Script (using Haskell):

	./build_and_run_full.sh /path/to/nuXmv /path/to/writable/location/

Build Script (without Haskell):

	./build_and_run_full.sh /path/to/nuXmv /path/to/writable/location/ no_haskell
	
Load Script:

	./build_and_run_full.sh /path/to/nuXmv /path/to/writable/location/
	
The results will be written in **/path/to/writable/location/behaverify\_results**. See the Interpreting and Comparing Results section for more information.

Note that the '/' at the end of the location is required.

---

## Step by Step Docker instructions

This section will explain how to utilize either the provided docker image or Dockerfile to recreate the tests using docker.

### 1. Creation of the Docker Image and Container.

Please execute only step 1a, 1b, or 1c. Steps 1a and 1b will utilize the Dockerfile to build the Docker Image and Container, but 1b will not install Haskell. Step 1c will load the Docker Image and Container from the provided .tar file.

#### 1a. Creation of the Docker Image and Container (using Haskell). Estimated time: 5 minutes

Should you wish to build the docker image yourself, please run

	./docker_build_script.sh

This will create a docker image named behaverify\_img with the tag latest. It will then also create a container named behaverify from that image.

#### 1b. Creation of the Docker Image and Container (without Haskell). Estimated time: 5 minutes

Should you wish to build the docker image yourself, please run

	./docker_build_script.sh no_haskell

This will create a docker image named behaverify\_img with the tag latest. It will then also create a container named behaverify from that image.

#### 1c. Using the provided Docker Image to create a Container

This will load the docker image from the .tar file.

	./docker_load_script.sh

### IMPORTANT:

The scripts below assume that the docker container is named behaverify. If you run 1a, 1b, or 1c, this will be handled for you and you need not worry.

### 2. Addition of nuXmv (estimated time: 30 seconds)

Next, please run

	./docker_add_nuxmv.sh /path/to/nuXmv

This will copy nuXmv from the path you provided to the correct location in the docker and ensure it is runable and an executable. Note that you should not point to the folder containing nuXmv, but to the nuXmv executable itself, and that the nuXmv version should be the Linux version. There should be no file extension.

### 3. Minimal Test (estimated time: 2 minutes)

The full test takes quite a while to run. To ensure everything works right, please run

	./docker_test_install.sh /path/to/writable/location/
	
or

	./docker_test_install.sh /path/to/writable/location/ no_haskell
	
If you used option 1b, please ensure you run the no\_haskell version. The no\_haskell version will not create or run Haskell files for the Differential Testing but is otherwise the same.

If the script fails because permission has been denied, please run the script without sudo (running docker without sudo requires some configuration). If the problem persists, please try a different location, as occasionally docker cannot write to secondary disks.

Note that the '/' at the end of the location is required.


### 4. Partial Test (estimated time: 20 minutes)

The full test takes quite a while to run. To replicate some of the results, run

	./docker_replicate_partial.sh /path/to/writable/location/

or

	./docker_replicate_partial.sh /path/to/writable/location/ no_haskell
	
If you used option 1b, please ensure you run the no\_haskell version. The no\_haskell version will not create or run Haskell files for the Differential Testing but is otherwise the same.

If the script fails because permission has been denied, please run the script without sudo (running docker without sudo requires some configuration). If the problem persists, please try a different location, as occasionally docker cannot write to secondary disks.

Note that the '/' at the end of the location is required.


### 5. Full Results (estimated time: under 12 hours)

This test takes a long time to complete. To replicate all results, run

	./docker_replicate_results.sh /path/to/writable/location/

or

	./docker_replicate_results.sh /path/to/writable/location/ no_haskell
	
If you used option 1b, please ensure you run the no\_haskell version. The no\_haskell version will not create or run Haskell files for the Differential Testing but is otherwise the same.

If the script fails because permission has been denied, please run the script without sudo (running docker without sudo requires some configuration). If the problem persists, please try a different location, as occasionally docker cannot write to secondary disks.

Note that the '/' at the end of the location is required.

---

# Verbose Installation for Running tests locally without docker.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Some of the scripts are likely to break on other systems. For instance, the scripts assume that nuXmv will be named nuXmv, and not nuXmv.exe. However, our code itself should still work (though we have not tested this).

This section is intentionally lengthy. If you are not interested in the details and just want the commands, please scroll down further. If you do not wish to install Haskell or run Haskell, skip any step which starts with HASKELL STEP. Haskell is only used for Differential Testing. If omitted, you will be able to replicate all the tests results, but the Differential Testing will only utilize the nuXmv model and the generate Python code.


1. nuXmv<br />2. The instructions provided are for Linux operating systems. If you are using a different OS, please download the appropriate version. Download nuXmv (see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.0.0-linux64.tar.gz ). Please ensure you download the Linux 64-bit x86 version 2.0.0 (October 14, 2019). The downloaded file should be **nuXmv-2.0.0-linux64.tar.gz**. Please extract this. After extracting, the executable will be located in **nuXmv-2.0.0-linux64/nuXmv-2.0.0-Linux/bin/nuXmv**. There should be **NO FILE EXTENSION**. This is the file we are interested in and will refer to later. We only want the executable, and are uninterested in the other files, folders, etc.
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
7. jinja2<br />jinja2 is used by BehaVerify.

		python3 -m pip install jinja2
8. textX<br />textX is used by BehaVerify for parsing.

		python3 -m pip install textX
9. matplotlib<br />matplotlib is used for generating graphs and plots.

		python3 -m pip install matplotlib
10. graphviz<br />graphviz is used to generate graphs and plots.

		sudo apt install graphviz
11. git<br />git is used to download our repository. If you would prefer to manually download our repository, you can skip this step.

		sudo apt install git
12. HASKELL STEP. Haskell prerequisites<br />These are prerequisites required by Haskell.

		sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5
13. HASKELL STEP. Additional Haskell prerequisite<br />

		sudo apt install libgmp3-dev
14. HASKELL STEP. GHCUP<br />Please follow the instructions at https://www.haskell.org/ghcup/ to install ghcup, Haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked. The relevant command to run is

		curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
	However, if you do not wish to use curl|sh, the aforementioned website provides additional options.
15. HASKELL STEP. Ghcup upgrade<br />This will upgrade ghcup.

		ghcup upgrade
16. HASKELL STEP. Cabal<br />This will install and set the specific version of cabal we used. Most likely, everything will work with a different version.

		ghcup install cabal 3.6.2.0
		ghcup set cabal 3.6.2.0
17. HASKELL STEP. GHC<br />This will install and set the specific version of ghc we used. Most likely, everything will work with a different version.

		ghcup install ghc 9.2.8
		ghcup set ghc 9.2.8
18. BehaVerify<br />Download our repository. If you did not install git, please download manually. If you installed git

		git clone https://github.com/verivital/behaverify
19. Enable scripts<br />This will allow all the necessary scripts to run. If you have not changed directories since running the previous command, then run the command listed below. Otherwise, please navigate to the directory containing our repository and then run the following

		sudo chmod -R +x behaverify/REPRODUCIBILITY/2023_SEFM/*.sh
20. Move nuXmv<br />You downloaded nuXmv in step 1. Please place it in **behaverify/REPRODUCIBILITY/2023\_SEFM/**. Please note that we only want the executable. The executable is expected to be name **nuXmv**, no file extension.
21. Enable nuXmv<br />If you have not changed directories since running step 19, then run the command listed below. Otherwise, please navigate to the directory containing our repository and then run the following

		sudo chmod +x behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv


You are now ready to run the scripts locally. Scroll past the concise installation instructions to see the scripts explanation.

---

# Concise Installation for Running the tests locally without docker.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Some of the scripts are likely to break on other systems. For instance, the scripts assume that nuXmv will be named nuXmv, and not nuXmv.exe. However, our code itself should still work (though we have not tested this).




Please download nuXmv (see  https://nuxmv.fbk.eu/ ). You only need to download nuXmv. There should be no installation. Download the relevant version for your system. It should be version 2.0.0.

	sudo apt update
	sudo apt upgrade
	sudo apt install python3
	sudo apt install pip
	python3 -m pip install py_trees
	python3 -m pip install pandas
	python3 -m pip install jinja2
	python3 -m pip install textX
	python3 -m pip install matplotlib
	sudo apt install graphviz
	sudo apt install git
	
If you do not wish to install Haskell or run Haskell, skip the following steps. Haskell is only used for Differential Testing. If omitted, you will be able to replicate all the tests results, but the Differential Testing will only utilize the nuXmv model and the generate Python code.

	sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5
	sudo apt install libgmp3-dev

Please follow the instructions at https://www.haskell.org/ghcup/ to install ghcup, haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked. The relevant command to run is

	curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
However, if you do not wish to use curl|sh, the aforementioned website provides additional options.

	ghcup upgrade
	ghcup install cabal 3.6.2.0
	ghcup set cabal 3.6.2.0
	ghcup install ghc 9.2.8
	ghcup set ghc 9.2.8
	
Regardless of whether or not you install Haskell, the subsequent commands are required.
	
	git clone https://github.com/verivital/behaverify

If you have not changed directories since running the previous command, then run the command listed below. Otherwise, please navigate to the directory containing our repository and then run the following

	sudo chmod -R +x behaverify/REPRODUCIBILITY/2023_SEFM/*.sh

You downloaded nuXmv in step 1. Please place it in **behaverify/REPRODUCIBILITY/2023\_SEFM/**. Please note that we only want the executable. The executable is expected to be name **nuXmv**, no file extension.

If you have not changed directories since running the previous chmod command, then run the command listed below. Otherwise, please navigate to the directory containing our repository and then run the following

	sudo chmod +x behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv

You are now ready to run the scripts locally. 

---

# Running Tests Locally without docker (requires installation, see above).

Note that each script will erase all the relevant results before running, to ensure that the results which exist after the script runs are accurate to that script. Thus if you wish to save the results, please move them before running another script.

## Minimal Script

To test everything is working, please navigate to behaverify/REPRODUCIBILITY/2023\_SEFM/ and run the following

	./minimal_script.sh ./
	
or

	./minimal_script.sh ./ no_haskell
	
If you did not install Haskell, make sure you use the no\_haskell version.

This will run a fairly small script. The results will be in behaverify/REPRODUCIBILITY/2023\_SEFM/examples/. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.

Note that the '/' at the end of the location is required.

## Partial Script

To create a subset of the results, please navigate to behaverify/REPRODUCIBILITY/2023\_SEFM/ and run the following

	./partial_results_script.sh ./

or

	./partial_results_script.sh ./ no_haskell
	
If you did not install Haskell, make sure you use the no\_haskell version.

This will run a larger, but still fairly small script. The results will be in behaverify/REPRODUCIBILITY/2023\_SEFM/examples/. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.

Note that the '/' at the end of the location is required.

## Full Script

To create all results, please navigate to behaverify/REPRODUCIBILITY/2023\_SEFM/ and run the following

	./results_script.sh ./
	
or

	./results_script.sh ./ no_haskell
	
If you did not install Haskell, make sure you use the no\_haskell version.

This will run a large script. The results will be in **behaverify/REPRODUCIBILITY/2023\_SEFM/examples/**. Please see the Interpreting and Comparing Results section for an explanation of what results to look for.

Note that the '/' at the end of the location is required.

---

# Interpreting and Comparing Results

The structure of these results will be the same, regardless of whether or not Haskell was used. Haskell is only used in Differential Testing. If you did not use Haskell, then the Differential Testing did not utilize Haskell and only compared the Python and nuXmv.

Upon completing any of the test scripts, you should find that /path/to/writable/location/ has a folder containing the results. The name of this folder depends on which test was run. See the specific tests for details. Within this folder, you should find the following folders, each of which corresponds to an experiment:

- light\_controller -> This experiment is called Light Controller in the paper (see **Section 6.1**). It is used in the paper.
- blueROV\_mod -> This experiment is called BlueROV in the paper (see **Section 6.2**). It is used in the paper.
- bigger\_fish\_expanded -> This experiment is called Bigger Fish in the paper (see **Section 6.3**). It is used in the paper. 
- simple\_robot -> This experiment is called Simple Robot in the paper (see **Section 6.4**). It is used in the paper.
- random\_haskell -> This is the Differential Experimenting (see **Section 7**). It is used in the paper.
- random\_sanity -> This is a confirmation that our comparison method works (see **Section 7.3**). It is used in the paper.
- bigger\_fish -> This experiment was not run, as the results were not used in the paper. It should have a single python file.
- checklist -> This experiment was not run, as the results were not used in the paper. It should have two python files and two .tree files.
- checklist\_invar -> This experiment was not run, as the results were not used in the paper. It should have two python files.
- simplified\_robot  -> This experiment was not run, as the results were not used in the paper. It should have a single python file and a single .tree file.

Some of the information gathered by the experiments is not used in the paper.

## Minimal Test

The minimal test can be used to confirm some of the results, but otherwise functions to test the installation.

The results should be in **/path/to/writable/location/behaverify\_install\_test\_results/**.

### Results that can be Compared with the Paper

- **light\_controller/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.1** we make several numerical claims based on these tables.
    - **light\_controller\_elapsed\_invar.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ctl.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ltl.tex** -> timing claim: results should be similar but may differ.
- **blueROV\_mod/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.2** we utilize some of the tables.
    - **blueROV\_mod\_elapsed\_invar.tex** -> timing claims: results should be similar but may differ. See **Table 1**.
	- **blueROV\_mod\_reachable\_states.tex** -> state claim: results should be exact. See **Table 2**. The value for first\_opt should also be between 2^62 and 2^63 reachable states, corresponding to the numerical claim made in **Section 6.4**.
- **blueROV\_mod/smv/** -> There should be a series of .smv files containing the nuXmv models. In **Section 6.4** we utilize information from these models.
    - **first\_opt\_blueROV\_mod\_1.smv** -> Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 73, for a total of 74 nodes. This should be exact. (The paper states 73; this is a typo and will be corrected).
- **random\_haskell/results/log.txt** -> This corresponds to **Section 7** of the paper. On each line, there should be a series of dashes and tX (X is a number, from 0 to 4). If there are any Comparison Failures, it means the results of the models differed. Note: if the Comparison Failure says "not enough ticks" (or something similar), then it is most likely indicating an installation error prevented one of the models from running correctly (probably the Haskell model). If you wish to double check the output of the models:
    - **random\_haskell/gen\_files/t\*/OUTPUT\_\*.txt** -> These files will contain the output of the run of each model. If the tick failure occurred, one of these is probably empty.
	- **random\_haskell/gen\_files/t\*/\*.smv** -> These files will contain the nuXmv models used. You can run them with nuXmv.
	- Python Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```python3 t*_runner.py```. This will run the Python Model (replace * with relevant number).
	- Haskell Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```cabal run```. This will run the Haskell Model.
		
Note that the presence of Comparison failure in the Differential Results in **random\_haskell** is possible as the trials were randomized. This indicates a bug with one of the models (or an installation error). The Minimal test generates only 5 of these tests, while the Full test generate 5000.

### Results that cannot be Compared with the Paper

- **bigger\_fish\_expanded/processed\_data/pictures/opt/** -> There should be a series of graphs (note: the 'graphs' will only have one data point). The minimal test does not run this test in full.
- **simple\_robot/processed\_data/pictures/opt/** -> There should be a series of graphs (note: the 'graphs' will only have one data point). The minimal test does not run this test in full.

## Partial Test

The partial test is between the minimal and full test. Some, but not all, of the results in the paper are generated through this test.

The results should be in **/path/to/writable/location/behaverify\_partial\_results/**.

### Results that can be Compared with the Paper

- **light\_controller/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.1** we make several numerical claims based on these tables.
    - **light\_controller\_elapsed\_invar.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ctl.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ltl.tex** -> timing claim: results should be similar but may differ.
- **blueROV\_mod/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.2** we utilize some of the tables.
    - **blueROV\_mod\_elapsed\_invar.tex** -> timing claims: results should be similar but may differ. See **Table 1**.
	- **blueROV\_mod\_reachable\_states.tex** -> state claim: results should be exact. See **Table 2**. The value for first\_opt should also be between 2^62 and 2^63 reachable states, corresponding to the numerical claim made in **Section 6.4**.
- **bigger\_fish\_expanded/processed\_data/pictures/opt/** -> There should be a series of graphs. In **Section 6.3** we utilize some of these graphs.
    - **bigger\_fish\_parallel\_ctl.png** -> This corresponds to part of **Figure 7**. timing claim: results should be similar but may differ.
	- **bigger\_fish\_parallel\_ltl.png** -> This corresponds to part of **Figure 7**. timing claim: results should be similar but may differ.
- **bigger\_fish\_expanded/smv/** -> There should be a series of .smv files containing nuXmv models. In **Section 6.3** we claim that the models with 600 checks have 1355 nodes. To verify this claim, open any of the files with the number 600 in the name. Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 1354, for a total of 1355 nodes. This result should be exact. (The paper states 1354; this is a typo and will be corrected).
- **blueROV\_mod/smv/** -> There should be a series of .smv files containing the nuXmv models. In **Section 6.4** we utilize information from these models.
    - **first\_opt\_blueROV\_mod\_1.smv** -> Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 73, for a total of 74 nodes. This result should be exact. (The paper states 73; this is a typo and will be corrected).
- **random\_haskell/results/log.txt** -> This corresponds to **Section 7** of the paper. On each line, there should be a series of dashes and tX (X is a number, from 0 to 20). If there are any Comparison Failures, it means the results of the models differed. Note: if the Comparison Failure says "not enough ticks" (or something similar), then it is most likely indicating an installation error prevented one of the models from running correctly (probably the Haskell model). If you wish to double check the output of the models:
    - **random\_haskell/gen\_files/t\*/OUTPUT\_\*.txt** -> These files will contain the output of the run of each model. If the tick failure occurred, one of these is probably empty.
	- **random\_haskell/gen\_files/t\*/\*.smv** -> These files will contain the nuXmv models used. You can run them with nuXmv.
	- Python Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```python3 t*_runner.py```. This will run the Python Model (replace * with relevant number).
	- Haskell Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```cabal run```. This will run the Haskell Model.
		
Note that the presence of Comparison failure in the Differential Results in **random\_haskell** is possible as the trials were randomized. This indicates a bug with one of the models (or an installation error). The Partial Test generates only 20 of these tests, while the Full test generate 5000.

### Results that cannot be Compared with the Paper
- **simple\_robot/processed\_data/pictures/opt/** -> There should be a series of graphs (note: the 'graphs' will only have one data point). The Partial test does not run this test in full.

## Full Test

The Full test generates all the results used in the paper.

The results should be in **/path/to/writable/location/behaverify\_results/**.

### Results that can be Compared with the Paper

- **light\_controller/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.1** we make several numerical claims based on these tables.
    - **light\_controller\_elapsed\_invar.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ctl.tex** -> timing claim: results should be similar but may differ.
	- **light\_controller\_elapsed\_ltl.tex** -> timing claim: results should be similar but may differ.
- **blueROV\_mod/processed\_data/tables/opt/** -> There should be a series of .tex files containing tables. In **Section 6.2** we utilize some of the tables.
    - **blueROV\_mod\_elapsed\_invar.tex** -> timing claims: results should be similar but may differ. See **Table 1**.
	- **blueROV\_mod\_reachable\_states.tex** -> state claim: results should be exact. See **Table 2**. The value for first\_opt should also be between 2^62 and 2^63 reachable states, corresponding to the numerical claim made in **Section 6.4**.
- **bigger\_fish\_expanded/processed\_data/pictures/opt/** -> There should be a series of graphs. In **Section 6.3** we utilize some of these graphs.
    - **bigger\_fish\_parallel\_ctl.png** -> This corresponds to part of **Figure 7**. timing claim: results should be similar but may differ.
	- **bigger\_fish\_parallel\_ltl.png** -> This corresponds to part of **Figure 7**. timing claim: results should be similar but may differ.
- **bigger\_fish\_expanded/smv/** -> There should be a series of .smv files containing nuXmv models. In **Section 6.3** we claim that the models with 600 checks have 1355 nodes. To verify this claim, open any of the files with the number 600 in the name. Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 1354, for a total of 1355 nodes. This should be exact. (The paper states 1354; this is a typo and will be corrected).
- **blueROV\_mod/smv/** -> There should be a series of .smv files containing the nuXmv models. In **Section 6.4** we utilize information from these models.
    - **first\_opt\_blueROV\_mod\_1.smv** -> Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 73, for a total of 74 nodes. This should be exact. (The paper states 73; this is a typo and will be corrected).
- **simple\_robot/processed\_data/pictures/opt/** -> There should be a series of graphs. In **Section 6.4** we utilize some of these graphs.
    - **simple\_robot\_ctl.png** -> This corresponds to part of **Figure 10**. timing claim: results should be similar but may differ.
	- **simple\_robot\_ltl.png** -> This corresponds to part of **Figure 10**. timing claim: results should be similar but may differ.
	- **simple\_robot\_reachable\_states.png** -> This corresponds to part of **Figure 10**. state claim: results should be exact.
- **simple\_robot/smv/** -> There should be a series of .smv files containing the nuXmv models. In **Section 6.4** we utilize information from these models.
    - **first\_opt\_simple\_robot\_50.smv** -> Please search this file for the phrase 'MODULE define\_nodes'. Following this phrase you will see an enumeration of the nodes, starting from 0 and ending at 21, for a total of 22 nodes. This should be exact. (The paper states 21; this is a typo and will be corrected).
	- **first\_opt\_simple\_robot\_50.smv** -> To verify the claim regarding number of reachable states, you will need to run nuXmv. Please execute the following commands:
	```
	nuXmv -int first_opt_simple_robot_50.smv
	go
	print_reachable_states
	quit
	```
	This will print the number of reachable states out of total states. Note that the go command will take more than 3 minutes to complete, but likely less than 10. You can then verify the claim that the model has about 2^25 reachable states.
- **random\_haskell/results/log.txt** -> This corresponds to **Section 7** of the paper. On each line, there should be a series of dashes and tX (X is a number, from 0 to 4999). If there are any Comparison Failures, it means the results of the models differed. Note: if the Comparison Failure says "not enough ticks" (or something similar), then it is most likely indicating an installation error prevented one of the models from running correctly (probably the Haskell model). If you wish to double check the output of the models:
    - **random\_haskell/gen\_files/t\*/OUTPUT\_\*.txt** -> These files will contain the output of the run of each model. If the tick failure occurred, one of these is probably empty.
	- **random\_haskell/gen\_files/t\*/\*.smv** -> These files will contain the nuXmv models used. You can run them with nuXmv.
	- Python Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```python3 t*_runner.py```. This will run the Python Model (replace * with relevant number).
	- Haskell Files -> Inside **random\_haskell/gen\_files/t\*/** folder, run ```cabal run```. This will run the Haskell Model.
		
Note that the presence of Comparison failure in the Differential Results in **random\_haskell** is possible as the trials were randomized. This indicates a bug with one of the models (or an installation error). The Full test generates 5000 random trials.

---

# Code Explanation

For an explanation on how to run our code, see our github repository https://github.com/verivital/behaverify
