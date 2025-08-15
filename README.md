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

### Explanation of installation

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
python3 -m behaverify trace examples/Collatz/collatz.tree ../behaverify_example/nuxmv/collatz_output.txt ../behaverify_example/
```


# nuXmv

Per the licensing agreement of nuXmv (see https://nuxmv.fbk.eu/downloads/LICENSE.txt ), we may not re-distribute the software in any form for any purpose. Thank you for understanding. The installation section above, however, does provide you with commandline options for downloading, extracting, and moving the software.

To aquire nuXmv, see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.1.0-linux64.tar.xz . You only need to download nuXmv. There should be no installation. Please make sure you download the appropriate version for your Operating System. 

For the Linux version, please ensure you download the Linux 64-bit x86 version 2.1.0 (November 29, 2024). The executable will be located in **nuXmv-2.1.0-linux64/bin/nuXmv**. There should be **NO FILE EXTENSION**.
