# BehaVerify

BehaVerify is a tool for turning specifications of Behavior Trees into nuXmv models for verification as well as generating Python and Haskell implementations of the specified trees.

- To recreate tests, see [REPRODUCIBILITY](https://github.com/verivital/behaverify/tree/main/REPRODUCIBILITY).
- For installation (including explanations and test runs), see [Installation](#installation).
- For running instructions (including a full list of options and examples), see [Options](#options).
- For a tutorial explaining how to create new models, see [Tutorial](https://github.com/verivital/behaverify/tree/main/tutorial_examples).

# References

Serena S. Serbinowska, Diego Manzanas Lopez, Dung Thuy Nguyen and Taylor T. Johnson, Neuro-Symbolic Behavior Trees and Their Verification, 2nd International Conference on Neuro-symbolic Systems (NeuS2025), Philadelphia, Pennsylvania, May 2025. https://proceedings.mlr.press/v288/serbinowska25a.html and https://neus-2025.github.io/files/papers/paper_56.pdf

Serena S. Serbinowska, Preston Robinette, Gabor Karsai, Taylor T. Johnson, Formalizing Stateful Behavior Trees, Proceedings Sixth International Workshop on Formal Methods for Autonomous Systems (FMAS2024), Manchester, UK, 11th and 12th of November 2024, Electronic Proceedings in Theoretical Computer Science 411, pp. 201–218. https://dx.doi.org/10.4204/EPTCS.411.14

Serena S. Serbinowska, Nicholas Potteiger, Anne M. Tumlin, Taylor T. Johnson, Verification of Behavior Trees with Contingency Monitors, Proceedings Sixth International Workshop on Formal Methods for Autonomous Systems (FMAS2024), Manchester, UK, 11th and 12th of November 2024, Electronic Proceedings in Theoretical Computer Science 411, pp. 56–72. https://dx.doi.org/10.4204/EPTCS.411.4

Serbinowska, S.S., Johnson, T.T. (2022). BehaVerify: Verifying Temporal Logic Specifications for Behavior Trees. In: Schlingloff, BH., Chai, M. (eds) Software Engineering and Formal Methods. SEFM 2022. Lecture Notes in Computer Science, vol 13550. Springer, Cham. https://doi.org/10.1007/978-3-031-17108-6_19

# Installation

This section contains the following

- [Instructions](#installation-instructions) for installing BehaVerify.
- An [explanation](#explanation-of-installation-instructions) of the instructions.
- A discussion on [using the virtual environment](#using-the-virtual-environment).
- A [test run](#test-run) to confirm that installation worked correctly.


## Installation Instructions


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

### Explanation of installation instructions

These four commands are used to download [nuXmv](https://nuxmv.fbk.eu/), extract the file, retrieve the executable, and ensure it is runnable.
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

### Using the Virtual Environment

To run BehaVerify, we will need to use the virtual environment we created during the installation process. This can be done in one of two ways.

1. Activate the virtual environment.
2. Explicitly call the virtual environment.

For method 1, run the following
```
source /path/to/behaverify_venv/bin/activate
```
Now, the terminal you are using should have (behaverify\_venv) listed prior to your username. The virtual environment has been activated within this terminal. You can now use BehaVerify within this terminal. Assuming you are in the top level of the repository and followed the installation instructions, this will be
```
source ../behaverify_venv/bin/activate
```

For method 2, you will need to modify each command that follows in the following manner:
```
python3 ...
```
becomes
```
/path/to/behaverify_venv/bin/python3 ...
```

Assuming you are in the top level of the repository and followed the installation instructions, this will be
```
../behaverify_venv/bin/python3 ...
```

### Test Run

Assuming you are in the top level of the BehaVerify repository, please test your installation by running the following command.
```
python3 -m behaverify nuxmv examples/DrunkenDrone/DrunkenDrone.tree ../behaverify_test --generate --invar --ctl --ltl --simulate 10 --nuxmv_path ../nuXmv 
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

# Options

The first argument to BehaVerify is the mode. Currently available modes (not case sensitive) are (in alphabetical order)
- [grid](#grid-mode)
- [Haskell](#haskell-mode)
- [LaTeX](#latex-mode)
- [nuXmv](#nuxmv-mode)
- [Python](#python-mode)
- [trace](#trace-mode)

Each of these is explained in a subsection below, and each features an example of how it could be run. Each example assumes you are at the top level of the repository and that the virtual environment is activated. Note that BehaVerify will do its best to not overwrite any existing files.

## Grid Mode
This mode is used to render a trace from a nuXmv or python execution of a grid world. It is still being developed and functionality is currently limited. Right now, it assumes variables are named in a very specific way, and as such only works with very specific examples. This will be improved in the future. Here we provide an example of how to run BehaVerify with grid mode. 

```
python3 -m behaverify nuxmv examples/NetworkExample/using9995.tree ../behaverify_example_grid/ --generate --ctl --nuxmv_path ../nuXmv
python3 -m behaverify grid nuxmv ../behaverify_example/nuxmv/using9995_output.txt ../behaverify_example_grid/ 10 10
```

The first command generates a nuXmv model and tries to verify the CTL specification. Since the specification is false, nuXmv produces a countertrace. This countertrace is then fed into the second command to produce images of the counterexample.

### Grid Mode Options

Below is a list of arguments for running BehaVerify using grid mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'grid' (case insensitive). If you use something else, you won't be in grid mode.
- *submode* : REQUIRED. String. This may be 'nuXmv' or 'python' (case insensitive). Use this to swap what kind of input is being parsed.
- *trace\_file* : REQUIRED. String (filepath). This must point to file containing a trace. That trace will be parsed and translated into images.
- *location* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *x\_size* : REQUIRED. Int. The size of the grid (length).
- *y\_size* : REQUIRED. Int. The size of the grid (height).
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.


## Haskell Mode
This mode is used to generate a Haskell implementation of the behavior tree.
```
python3 -m behaverify haskell ./examples/Collatz/collatz.tree ../behaverify_example_haskell/
```

### Haskell Mode Options

Below is a list of arguments for running BehaVerify using Haskell mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'haskell' (case insensitive). If you use something else, you won't be in haskell mode.
- *model\_file* : REQUIRED. String (filepath). This must point to file containing a model. Haskell code will be written based on the model.
- *location* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *output\_name* : OPTIONAL. String. If present, sets output name. If omitted, default (based on model\_file) is used instead.
- *max\_iter* : OPTIONAL. Int. The maximum number of iterations to simulate. Default is 100.
- *recursion\_limit* : OPTIONAL. Int. Can be used to increase the Python recursion limit. Particularly large or complex models may require a large recursion stack, mostly for TextX to correctly parse the model file.
- *no\_checks* : OPTIONAL. FLAG. If set, BehaVerify will skip grammar checking. As a result, files will be produced more quickly. Grammar checking is used to provide readable errors that explain why a model does not work. If a model\_file contains no errors, these may be safely ignored. If a model\_file contains errors and this is omitted, BehaVerify may crash in unexpected ways, or the output may not function correctly.
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.


## LaTeX Mode

This mode is used to generate a tikz diagram of the behavior tree.

```
python3 -m behaverify latex ./examples/Collatz/collatz_small.tree ../behaverify_example_latex/collatz_small.tex
```


### LaTeX Mode Options

Below is a list of arguments for running BehaVerify using LaTeX mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'LaTeX' (case insensitive). If you use something else, you won't be in LaTeX mode.
- *model\_file* : REQUIRED. String (filepath). This must point to file containing a model. A tikz diagram will be written based on the model.
- *output\_file* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *insert\_only* : OPTIONAL. Flag. If set, this will only generate a Tikz block of code for the model. If not set, a complete LaTeX file will be generated.
- *recursion\_limit* : OPTIONAL. Int. Can be used to increase the Python recursion limit. Particularly large or complex models may require a large recursion stack, mostly for TextX to correctly parse the model file.
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.
- *on\_sides* : OPTIONAL. Flag. If set, BehaVerify will change the placement of variable information, initial values, and environment updates.


## nuXmv mode
This mode is used to generate or run an existing nuXmv model for verification purposes.

```
python3 -m behaverify nuxmv examples/NetworkExample/using1000.tree ../behaverify_example_nuxmv/ --generate --ctl --nuxmv_path ../nuXmv
```



### nuXmv Mode Options

Below is a list of arguments for running BehaVerify using nuXmv mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'nuXmv' (case insensitive). If you use something else, you won't be in nuXmv mode.
- *model\_file* : REQUIRED. String (filepath). This must point to file containing a .tree model or a .smv model. If .tree is used, you probably want the generate flag. If .smv is used, do not set the generate flag.
- *location* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *output\_name* : OPTIONAL. String. If present, sets output name. If omitted, default (based on model\_file) is used instead.
- *generate* : OPTIONAL. Flag. If set, BehaVerify will generate a nuXmv model (model\_file must be a .tree file).
- *invar* : OPTIONAL. Flag. If set, BehaVerify will verify any invariant specifications using nuXmv. model\_file must be .smv or .tree with generate flag.
- *ctl* : OPTIONAL. Flag. If set, BehaVerify will verify any CTL specifications using nuXmv. model\_file must be .smv or .tree with generate flag.
- *ltl* : OPTIONAL. Flag. If set, BehaVerify will verify any LTL specifications using nuXmv. model\_file must be .smv or .tree with generate flag.
- *simulate* : OPTIONAL. Int. If greater than 0, BehaVerify will simulate using nuXmv for ARG number of steps. model\_file must be .smv or .tree with generate flag.
- *nuxmv\_path* : OPTIONAL. String (filepath). This points to where nuXmv is. It is required if any of invar, ctl, ltl, or simulate are being used.
- *keep\_last\_stage* : OPTIONAL. Flag. If set, disables an optimization that removes the last stage of variables under certain circumstances.
- *do\_not\_trim* : OPTIONAL. Flag. If set, disables an optimization that removes nodes that cannot run.
- *recursion\_limit* : OPTIONAL. Int. Can be used to increase the Python recursion limit. Particularly large or complex models may require a large recursion stack, mostly for TextX to correctly parse the model file.
- *no\_checks* : OPTIONAL. FLAG. If set, BehaVerify will skip grammar checking. As a result, files will be produced more quickly. Grammar checking is used to provide readable errors that explain why a model does not work. If a model\_file contains no errors, these may be safely ignored. If a model\_file contains errors and this is omitted, BehaVerify may crash in unexpected ways, or the output may not function correctly.
- *record\_times* : OPTIONAL. String (Filepath). If included, BehaVerify will write how long the process took to a the specified file.
- *use\_encoding* : OPTIONAL. String. One of ('naive' or 'fastforwarding') (case insensitive). Default is 'fastforwarding'. Changes what encoding is used for nuXmv.
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.



## Python mode
This mode is used to generate a Python implemention of the behavior tree.
```
python3 -m behaverify python ./examples/Collatz/collatz.tree ../behaverify_example_python/
```


### Python Mode Options

Below is a list of arguments for running BehaVerify using Python mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'Python' (case insensitive). If you use something else, you won't be in Python mode.
- *model\_file* : REQUIRED. String (filepath). This must point to file containing a model. Python code will be written based on the model.
- *location* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *output\_name* : OPTIONAL. String. If present, sets output name. If omitted, default (based on model\_file) is used instead.
- *max\_iter* : OPTIONAL. Int. The maximum number of iterations to simulate. Default is 100.
- *no\_var\_print* : OPTIONAL. Flag.
- *serene\_print* : OPTIONAL. Flag.
- *py\_tree\_print* : OPTIONAL. Flag.
- *recursion\_limit* : OPTIONAL. Int. Can be used to increase the Python recursion limit. Particularly large or complex models may require a large recursion stack, mostly for TextX to correctly parse the model file.
- *no\_checks* : OPTIONAL. FLAG. If set, BehaVerify will skip grammar checking. As a result, files will be produced more quickly. Grammar checking is used to provide readable errors that explain why a model does not work. If a model\_file contains no errors, these may be safely ignored. If a model\_file contains errors and this is omitted, BehaVerify may crash in unexpected ways, or the output may not function correctly.
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.


## Trace Mode
This mode is used to generate a series of images illustrating a trace from nuXmv.

```
python3 -m behaverify nuxmv examples/Collatz/collatz.tree ../behaverify_example_trace/ --generate --invar --nuxmv_path ../nuXmv
python3 -m behaverify trace examples/Collatz/collatz.tree ../behaverify_example_trace/nuxmv/collatz_output.txt ../behaverify_example/
```


### Trace Mode Options

Below is a list of arguments for running BehaVerify using trace mode. Each argument is formatted using the following syntax.
- *NAME* : TYPE. DATATYPE. EXPLANATION.
where
- NAME is the name of the argument
- TYPE is either REQUIRED or OPTIONAL.
    - REQUIRED means you must include this argument. Do not type the name of this argument. Order is set.
    - OPTIONAL means you may include this argument. To include it, type '--NAME ARG' where NAME is the name of the argument and ARG is the value. If the DATATYPE is FLAG, do not not include ARG.
- DATATYPE is either Int, String, or Flag.

---

- *mode* : REQUIRED. String. This must be 'trace' (case insensitive). If you use something else, you won't be in trace mode.
- *model\_file* : REQUIRED. String (filepath). This must point to the .tree model.
- *trace\_file* : REQUIRED. String (filepath). This must point to a file containing a trace. That trace will be parsed and translated into images.
- *location* : REQUIRED. String (filepath). This must point to a location where the output will be written.
- *do\_not\_trim* : OPTIONAL. Flag. If set, prevents BehaVerify from trimming nodes that cannot run.
- *recursion\_limit* : OPTIONAL. Int. Can be used to increase the Python recursion limit. Particularly large or complex models may require a large recursion stack, mostly for TextX to correctly parse the model file.
- *overwrite* : OPTIONAL. Flag. If set, BehaVerify will overwrite existing files.


# nuXmv

Per the licensing agreement of nuXmv (see https://nuxmv.fbk.eu/downloads/LICENSE.txt ), we may not re-distribute the software in any form for any purpose. Thank you for understanding. The installation section above, however, does provide you with commandline options for downloading, extracting, and moving the software.

To aquire nuXmv, see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz . You only need to download nuXmv. There should be no installation. Please make sure you download the appropriate version for your Operating System. 

For the Linux version, please ensure you download the Linux 64-bit x86 version 2.1.0 (November 29, 2024). The executable will be located in **nuXmv-2.1.0-linux64/bin/nuXmv**. There should be **NO FILE EXTENSION**.
