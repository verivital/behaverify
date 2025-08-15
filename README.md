# BehaVerify

BehaVerify is a tool for turning specifications of Behavior Trees into nuXmv models for verification as well as generating Python and Haskell implementations of the specified trees.

To recreate tests, see REPRODUCIBILITY.

# References

Serena S. Serbinowska, Diego Manzanas Lopez, Dung Thuy Nguyen and Taylor T. Johnson, Neuro-Symbolic Behavior Trees and Their Verification, 2nd International Conference on Neuro-symbolic Systems (NeuS2025), Philadelphia, Pennsylvania, May 2025. https://proceedings.mlr.press/v288/serbinowska25a.html and https://neus-2025.github.io/files/papers/paper_56.pdf

Serena S. Serbinowska, Preston Robinette, Gabor Karsai, Taylor T. Johnson, Formalizing Stateful Behavior Trees, Proceedings Sixth International Workshop on Formal Methods for Autonomous Systems (FMAS2024), Manchester, UK, 11th and 12th of November 2024, Electronic Proceedings in Theoretical Computer Science 411, pp. 201–218. https://dx.doi.org/10.4204/EPTCS.411.14

Serena S. Serbinowska, Nicholas Potteiger, Anne M. Tumlin, Taylor T. Johnson, Verification of Behavior Trees with Contingency Monitors, Proceedings Sixth International Workshop on Formal Methods for Autonomous Systems (FMAS2024), Manchester, UK, 11th and 12th of November 2024, Electronic Proceedings in Theoretical Computer Science 411, pp. 56–72. https://dx.doi.org/10.4204/EPTCS.411.4

Serbinowska, S.S., Johnson, T.T. (2022). BehaVerify: Verifying Temporal Logic Specifications for Behavior Trees. In: Schlingloff, BH., Chai, M. (eds) Software Engineering and Formal Methods. SEFM 2022. Lecture Notes in Computer Science, vol 13550. Springer, Cham. https://doi.org/10.1007/978-3-031-17108-6_19

# Installation

The following commands will download and install BehaVerify. A breakdown of the commands is provided below, in case something goes wrong. While the installation commands are formatted for Linux, we believe that BehaVerify will work on other operating systems.

```
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz -O ./nuXmv_DL.tar.xz
tar -xf ./nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
mv ./nuXmv_DL/bin/nuXmv ./nuXmv
chmod +x nuXmv
git clone https://github.com/verivital/behaverify
cd behaverify
python3 -m venv ../behaverify_venv
source ../behaverify_venv/bin/activate
python3 -m pip install .
```

---

These four commands are used to download nuXmv ( https://nuxmv.fbk.eu/ ), extract the file, retrieve the executable, and ensure it is runnable.
```
wget https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz -O ./nuXmv_DL.tar.xz
tar -xf ./nuXmv_DL.tar.xz --one-top-level=nuXmv_DL --strip-components 1
mv ./nuXmv_DL/bin/nuXmv ./nuXmv
chmod +x nuXmv
```
We provide some additional details about [nuXmv](#nuXmv).

---

These two commands are used to clone the repository and move into it.
```
git clone https://github.com/verivital/behaverify
cd behaverify
```

---

These three commands are used to create a Python virtual environment, activate it, and then install BehaVerify
```
python3 -m venv ../behaverify_venv
source ../behaverify_venv/bin/activate
python3 -m pip install .
```

---

Assuming all of the commands have been executed, BehaVerify has now been installed within the virtual environment and is ready for use. See [test run](#test-run) to test your installation.


# Running BehaVerify

### Using the Virtual Environment

To run BehaVerify, we will need to use the virtual environment we created during the installation process. This can be done in one of two ways.

1. Activate the virtual environment.
2. Explicitly call the virtual environment.

For method 1, run the following
```
source /path/to/behaverify_venv/bin/activate
```
Now, the terminal you are using should have (behaverify\_venv) listed prior to your username. The virtual environment has been activated within this terminal. You can now use BehaVerify within this terminal.

For method 2, you will need to modify each command that follows in the following manner:
```
python3 ...
```
becomes
```
/path/to/behaverify_venv/bin/python3 ...
```

### Test Run

Assuming you are in the top level of the BehaVerify repository, please test your installation by running the following command.
```
python3 -m behaverify nuxmv examples/DrunkenDrone/DrunkenDrone.tree ../test --generate --invar --ctl --ltl --simulate 10 --nuxmv_path ../nuXmv 
```

Then use
```
cat ../test/nuxmv/DrunkenDrone.smv
```
and
```
cat ../test/nuxmv/DrunkenDrone_output.txt
```
to view the nuXmv model and verification results, respectively.

## Examples

We suggest reading the following examples, in order. The files are well documented, and help explain how 

# Options

The first argument to BehaVerify is the mode. Currently available modes (not case sensitive) are (in alphabetical order)
- [grid](#grid-mode)
- [Haskell](#haskell-mode)
- [LaTeX](#latex-mode)
- [nuXmv](#nuxmv-mode)
- [Python](#python-mode)
- [trace](#trace-mode)
Each of these is explained in a subsection below, and each features an example of how it could be run. Each example assumes you are at the top level of the repository and that the virtual environment is activated. Note that BehaVerify will do its best to not overwrite any existing files.

## grid mode
This mode is used to render a trace from a nuXmv or python execution of a grid world. It is still being developed and functionality is currently limited. Right now, it assumes variables are named in a very specific way, and as such only works with very specific examples. This will be improved in the future.

```
python3 -m behaverify nuxmv examples/NetworkExample/using9995.tree ../behaverify_example/ --generate --ctl --nuxmv_path ../nuXmv
python3 -m behaverify grid nuxmv ../behaverify_example/nuxmv/using9995_output.txt ../behaverify_example/ 10 10
```

The first command generates a nuXmv model and tries to verify the CTL specification. Since the specification is false, nuXmv produces a countertrace. This countertrace is then fed into the second command to produce images of the counterexample.


## Haskell mode
This mode is used to generate a Haskell implementation of the behavior tree.
```
python3 -m behaverify haskell ./examples/Collatz/collatz.tree ../behaverify_example/
```

## LaTeX mode
This mode is used to generate a tikz diagram of the behavior tree.
```
python3 -m behaverify latex ./examples/Collatz/collatz_small.tree ../behaverify_example/collatz_small.tex
```

## nuXmv mode
This mode is used to generate or run a nuXmv model for verification purposes.

```
python3 -m behaverify nuxmv examples/NetworkExample/using1000.tree ../behaverify_example/ --generate --ctl --nuxmv_path ../nuXmv
```

## Python mode
This mode is used to generate a Python implemention of the behavior tree.
```
python3 -m behaverify python ./examples/Collatz/collatz.tree ../behaverify_example/
```

## trace mode
This mode is used to generate a series of images illustrating a trace from nuXmv.

```
python3 -m behaverify nuxmv examples/Collatz/collatz.tree ../behaverify_example/ --generate --invar --nuxmv_path ../nuXmv
```


# nuXmv

Per the licensing agreement of nuXmv (see https://nuxmv.fbk.eu/downloads/LICENSE.txt ), we may not re-distribute the software in any form for any purpose. Thank you for understanding. The installation section above, however, does provide you with commandline options for downloading, extracting, and moving the software.

To aquire nuXmv, see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz . You only need to download nuXmv. There should be no installation. Please make sure you download the appropriate version for your Operating System. 

For the Linux version, please ensure you download the Linux 64-bit x86 version 2.1.0 (November 29, 2024). The executable will be located in **nuXmv-2.1.0-linux64/bin/nuXmv**. There should be **NO FILE EXTENSION**.

---

# Concise Installation Instructions.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Please adapt commands as necessary (e.g., changing python3 to python).

This section is intentionally conscise. If you are interested in the details, please scroll down.

Download nuXmv

```
sudo apt update -y
sudo apt upgrade -y
sudo apt install python3 git -y
sudo apt install pip -y
git clone https://github.com/verivital/behaverify
cd behaverify
python3 -m pip install -r behaverify/requirements/core.txt
sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 -y
sudo apt install libgmp3-dev -y
```

Please follow the instructions at https://www.haskell.org/ghcup/ to install GHCUP, Haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked.

```
ghcup upgrade
ghcup install cabal 3.6.2.0
ghcup set cabal 3.6.2.0
ghcup install ghc 9.2.8
ghcup set ghc 9.2.8
sudo chmod +x /path/to/nuXmv
```

---

# Verbose Installation Instructions.

The instructions are for Linux (and more specifically Ubuntu). We have not tested this on any other systems. Please adapt commands as necessary (e.g., changing python3 to python).

This section is intentionally lengthy. If you are not interested in the details and just want the commands, please scroll up.


1. (OPTIONAL) nuXmv<br />Please download nuXmv (see  https://nuxmv.fbk.eu/ ). You only need to download nuXmv. There should be no installation. Download the relevant version for your system. It should be version 2.0.0. The download will include many files. You only need the executable (no file extension). See above for more information. You only need to execute this step if you are interested in verifying the generated models with nuXmv.
2. Updating<br /> We suggest running the following commands.

```
sudo apt update
sudo apt upgrade
```

3. Python3<br />Python3 is used to run BehaVerify. As such, it is necessary. If you already have python3 installed, skip the following step. If not, run

```
sudo apt install python3
```

4. pip<br />pip is used to install other python packages. If you already have pip installed (for python3), skip the following step. If not, run

```
sudo apt install pip
```

5. git<br />git is used to download our repository. If you would prefer to manually download our repository, you can skip this step.

```
sudo apt install git
```

6. BehaVerify<br />Download our repository. If you did not install git, please download manually. If you installed git

```
git clone https://github.com/verivital/behaverify
```

7. Change Directory<br />Move into the repository.

```
cd behaverify
```

8. Installing Python Packages.<br />You may install the packages manually, or utilize the requirements file. Subsequent steps will explain what each of the Python packages does. The command for using the requirements file is (command assumes you are at the top level of the repository)

```
python3 -m pip install -r behaverify/requirements/core.txt
```

8a. (OPTIONAL) PyTrees<br />PyTrees is used in the generated python code. If you do not wish to run generated python code, you may skip this step.

```
python3 -m pip install py_trees
```

8b. textX<br />textX is used by BehaVerify for parsing. It is necessary for BehaVerify to run in any capacity

```
python3 -m pip install textX
```

8c. (OPTIONAL) onnxruntime<br />onnxruntime is used when handling neural networks in leaf nodes. If you do not plan to use neural networks in leaf nodes, you may skip this step.

```
python3 -m pip install onnxruntime
```

8d. (OPTIONAL) onnx<br />onnx is used when handling neural networks in leaf nodes. If you do not plan to use neural networks in leaf nodes, you may skip this step.

```
python3 -m pip install onnx
```

9. (OPTIONAL) Haskell prerequisites<br />These are prerequisites required by Haskell.

```
sudo apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 libgmp3-dev
```

10. (OPTIONAL) GHCUP<br />Please follow the instructions at https://www.haskell.org/ghcup/ to install GHCUP, Haskell, and cabal. These are used to run generated Haskell code. Please preappend (or append) your path when asked.
11. (OPTIONAL) GHCUP upgrade<br />This will upgrade GHCUP.

```
ghcup upgrade
```

12. (OPTIONAL) Cabal<br />This will install and set the specific version of cabal we used. Most likely, everything will work with a different version.

```
ghcup install cabal 3.6.2.0
ghcup set cabal 3.6.2.0
```

13. (OPTIONAL) GHC<br />This will install and set the specific version of ghc we used. Most likely, everything will work with a different version.

```
ghcup install ghc 9.2.8
ghcup set ghc 9.2.8
```

14. (OPTIONAL) Enable nuXmv<br />If you plan to use nuXmv, please ensure you can run nuXmv as an executable

```
sudo chmod +x /path/to/nuXmv
```

---

# Running BehaVerify Locally

This section will be structured as follows

- General Layout and Information
- Generating .smv files for nuXmv
- Generating .py files for Python
- Generating .hs files for Haskell

---

## General Layout and Information

File extensions are not mandatory. This documentation will use the following convention for them

- .smv -> a file for use with nuXmv
- .tree -> a specification file that follows the rules in behaverify/metamodel/behaverify.tx (a textx file)
- .tx -> a metamodel file.
- .py -> a Python file (either generated by BehaVerify, or a source file for BehaVerify)
- .hs -> a Haskell file (generated by BehaVerify)

The following files are relevant to the user. They assume they are in the in behaverify/src and may not work correctly if moved or if other files are missing from that directory.

- dsl\_to\_nuxmv.py -> Converts .tree files to .smv files
- dsl\_to\_haskell.py -> Converts .tree files to Haskell
- dsl\_to\_python.py -> Converts .tree files to Python (py\_trees)

---

## Generating .smv files for nuXmv

.smv files can be used with nuXmv for model verification. You can generate .smv using the following command:

```
python3 ./src/dsl_to_behaverify.py ./metamodel/behaverify.tx /path/to/tree.tree /path/to/smv.smv
```

We assume you are running this command from the top level of the repository. If not, please adjust paths as necessary.

### Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- /path/to/smv.smv -> the output will be written to the file location provided. You do not need to make this a .smv file.

### Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --keep\_stage\_0 -> Flag option (no additional information required). This disables the stage\_0 pruning optimization. 
- --keep\_last\_stage -> Flag option (no additional information required). This disables the last\_stage pruning optimization. 
- --do\_not\_trim -> Flag option (no additional information required). This disables node pruning. BehaVerify will not restructure your tree to remove unreachable nodes.

### Using nuXmv for verification

Please run the following command

```
/path/to/nuXmv --int /path/to/smv.smv
```

Here --int will turn this into interactive mode. Now, run the following commands

```
go
check_ctlspec
check_ltlspec
check_invar
quit
```

go is a command which runs several commands in preparation of model checking. The check commands check the relevant specifications. If a specification is False, a counterexample will be produced.

---

## Generating Python Files

Python files can be generated using the following command:

```
python3 ./src/dsl_to_pytree.py ./metamodel/behaverify.tx /path/to/tree.tree /path/to/output/folder/ fileName 
```

We assume you are running this command from the top level of the repository. If not, please adjust paths as necessary.

### Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- /path/to/output/folder/ -> this argument must point to a folder. This is where the python files will be written.
- fileName -> this should not include any extension. fileName.py, fileName\_environment.py, and fileName\_runner.py will depend upon this name.

Note that various other files will also be created.

### Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --max\_iter -> Requires an integer. Defaults to 100. This dictates how many iterations fileName\_runner.py will execute.
- --no\_var\_print -> Flag option (no additional information required). This disables the printing of variables.
- --serene\_print -> Flag option (no additional information required). This enables the printing of the status of the tree after each tick.
- --py\_tree\_print -> Flag option (no additional information required). This enables the use of PyTree visualizers to print information about the status of the tree (warning: this does not reflect the status the nodes returned when running, as those nodes are sometimes reset).


### Utilizing the Generated Files

Run

```
python3 /path/to/folder/fileName_runner.py
```
	
---

## Generating Haskell Files

Haskell Files are slightly more irritating to generate and use. First, create a folder where you wish to store your Haskell files. Then use the following command

```
mkdir /path/to/output/folder
mkdir /path/to/output/folder/app
```

This will cause cabal to initiate a project in the current folder. Next, run  the following command:

```
python ./src/dsl_to_pytree.py ./metamodel/behaverify.tx /path/to/tree.tree /path/to/output/folder/ fileName 
```

We assume you are running this command from the top level of the repository. If not, please adjust paths as necessary.

### Arguments

- ./metamodel/behaverify.tx -> this argument must point to the metamodel file.
- /path/to/tree.tree -> this argument must point to a specification file. It does not need to have the .tree extension.
- /path/to/output/folder/ -> this argument must point to a folder. The haskell files will be written to /path/to/folder/output/app/.
- fileName -> this should not include any extension. fileName.hs will depend upon this name.

Note that various other files will also be created.

NOTE: cabal is currently utilized because non-determinism depends on the System.Random package, and cabal is the easiest way we found to quickly deal with this.

### Additional Optional Arguments

Additional arguments are listed below. You must preface them with --

- --max\_iter -> Requires an integer as well. Defaults to 100. This dictates how many iterations Main.hs will execute.

### Utilizing the Generated Files

In /path/to/output/folder/, run

```
cabal run
```

If you wish to change the randomized starting seeds, use 

```
cabal run fileName -- seed1 seed2
```

(seed1 controls the initial seed for the blackboard, while seed2 controls the initial seed for the environment).
