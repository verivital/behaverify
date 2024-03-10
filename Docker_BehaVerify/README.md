# BehaVerify

BehaVerify is a tool for turning specifications of Behavior Trees into nuXmv models for verification as well as generating Python and Haskell implementations of the specified trees.

To recreate tests, see REPRODUCIBILITY.

Older versions can be found in subfolders of /src/versions/. The documentation for older versions may not be accurate.

# References

Serbinowska, S.S., Johnson, T.T. (2022). BehaVerify: Verifying Temporal Logic Specifications for Behavior Trees. In: Schlingloff, BH., Chai, M. (eds) Software Engineering and Formal Methods. SEFM 2022. Lecture Notes in Computer Science, vol 13550. Springer, Cham. https://doi.org/10.1007/978-3-031-17108-6_19

# READMEs and Instructions

There are several README files placed throughout this repository, each serving a unique purpose. We suggest using BehaVerify through Docker.

- behaverify/README.md -> This README provides information about how to install and run BehaVerify directly on your machine.
- behaverify/Docker\_BehaVerify/README.md -> This README provides information about how to use BehaVerify through Docker.
- behaverify/metamodel/README.md -> This README provides details about the BehaVerify language.
- behaverify/REPRODUCIBILITY/*/README.md -> This README provides details about running the tests for the relevant paper (regardless of if the submission was accepted).

---

# Layout of this README

- nuXmv -> Instructions regarding nuXmv.
- Prequisites, Requirements, and Information
- Installation Instructions
- Running BehaVerify through Docker

---

# nuXmv

Per the licensing agreement of nuXmv (see https://nuxmv.fbk.eu/downloads/LICENSE.txt ), we may not re-distribute the software in any form for any purpose. Thank you for understanding.

To aquite nuXmv, see  https://nuxmv.fbk.eu/download.html or https://nuxmv.fbk.eu/theme/download.php?file=nuXmv-2.0.0-linux64.tar.gz . You only need to download nuXmv. There should be no installation. Regardless of your OS, please ensure you download the Linux 64-bit x86 version 2.0.0 (October 14, 2019). The executable will be located in **nuXmv-2.0.0-linux64/nuXmv-2.0.0-Linux/bin/nuXmv**. There should be **NO FILE EXTENSION**.

---

# Prequisites, Requirements, and Information

- docker
- git (Strictly speaking not necessary, if you are willing to manually download files).
- Python3
- docker-py (a python pacakge)We provide a requirements file for installing this.
- nuXmv (must be downloaded seperately (instructions were provided above)).

---

# Installation Instructions

## Docker

We have provided a Docker File which can be used to build a Docker Image and Docker Container for running BehaVerify. We provide python files for Building the Docker Image, Creating the Docker Container, and running the tool.

## nuXmv

Please download nuXmv, as instructed above.

## Installation

The following instructions are formatted for Linux.
Some commands may differ on other operating systems (e.g., you may need to replace 'python3' with 'python').

`
git clone https://github.com/verivital/behaverify
cd behaverify
python3 -m pip install -r ./requirements/docker.txt
cd Docker_BehaVerify/python_script
python3 reinstall.py ../
python3 add_nuxmv.py /YOUR/PATH/TO/nuXmv
`

You may alternatively manually download the repository or individually download all of the files in behaverify/Docker\_BehaVerify and behaverify/requirements. Note that the commands will assume that the files are structured in the same way the repository is.

**IMPORTANT: Replace /YOUR/PATH/TO/nuXmv with the appropriate path on your machine.**

### Explanations

The reinstall script removes any exsting images/containers that would cause conflicts (behaverify, behaverify\_img). It then runs the install script. The install script will create a Docker Image named behaverify\_img with the tag latest. It will then also create a Docker Container named behaverify from that Docker Image. This Docker Container can now be used to generate (and execute) nuXmv models, Python code, and Haskell code.

---

# Running BehaVerify Through Docker

## BehaVerify Demos in Docker
The following commands assume you are in behaverify/Docker\_BehaVerify/python\_scripts. The following instructions are formatted for Linux. Some commands may differ on other operating systems (e.g., you may need to replace 'python3' with 'python').

`
python3 generate.py demo ANSR_ONNX_2 ./ANSR_ONNX_2
python3 generate.py demo ANSR_ONNX_2_counter \
  ./ANSR_ONNX_2_counter
python3 generate.py demo ANSR_ONNX_2 \
  ./ANSR_ONNX_2_with_changes \
  --additional_input \
  "x_min := 0, y_min := 0, x_max := 6, y_max := 6, tree_count := 2,\
  vision_range := 2, tree_range := 2,\
  y_change := 1, movement_cooldown := 4"
`

The above commands will place ANSR\_ONNX\_2.tar, ANSR\_ONNX\_2\_counter.tar, and ANSR\_ONNX\_2\_with\_changes in Docker\_BehaVerify/python\_script. Inside, you should find something like

- ANSR\_ONNX\_2
  - app
    - ANSR\_ONNX\_2.smv
  - networks
    - x\_net.onnx
	- y\_net.onnx
  - output
	- nuxmv\_ctl\_results.txt
    - potentially images.
  - ANSR\_ONNX\_2.tree
  
The images are a visualization of the counterexample produced by nuXmv. If you use the additional input flag, you may rearrange the arguments in any order, but all arguments must be present. These will control the parameters of the ANSR\_ONNX model.

## Running BehaVerify through Docker
The following commands assume you are in behaverify/Docker\_BehaVerify/python\_scripts. The following instructions are formatted for Linux. Some commands may differ on other operating systems (e.g., you may need to replace 'python3' with 'python').

`
  python3 generate.py /path/to/model /path/to/networks \
    /path/to/output TO\_GENERATE COMMAND FLAGS
`

- **/path/to/model** should point to a file containing the specification for the desired Behavior Tree. See the .tree files in behaverify/examples.
- **/path/to/networks** should point to a folder containing the networks used by the Behavior Tree. If there is no such folder, please replace this argument with "-".
- **/path/to/output** should point to a folder where the output should be placed.
- **TO\_GENERATE** should be one of 'nuXmv', 'Python', and 'Haskell'.  This determines what output should be generated.
- **COMMAND** should be one of 'generate', 'simulate', 'ctl', 'ltl', or 'invar'.
  - **generate** produces the model or code, but does nothing else.
  - **simulate** produces the model or code and records a simulation.
  - **ctl** (nuXmv only) produces the model and checks if the CTL specifications are satisfied.
  - **ltl** (nuXmv only) produces the model and checks if the LTL specifications are satisfied.
  - **invar** (nuXmv only) produces the model and checks if the Invariant specifications are satisfied.
  \end{itemize**
- **FLAGS** These are flags for modifying the behavior of BehaVerify. Some flags are only available in some modes.
  - **--recursion\_limit** (Haskell, Python, nuXmv), INTEGER, sets the recursion limit for Python during model/code generation. This is important, as large models will likely involve complex textX \CiteAsRef{textX** parsing which may exceed the default recursion limit.
  - **--max\_iter** (Haskell, Python), INTEGER, sets the number of iterations afterwhich the simulation should end.
  - **--no\_var\_print** (Python), None, disables the printing of variable values for Python code.
  - **--serene\_print** (Python), None, enables the printing out the state of the tree. The built in py\_trees printing can be misleading as nodes will often be marked as Invalid even though they ran, because they have already been reset.
  - **--py\_tree\_print** (Python), None, enables the printing out of the state of the tree using the built in methods.
  - **--safe\_assignment** (Python), None, enforces more strict typing for python (not recommended).
  - **--keep\_stage\_0** (nuXmv), None, disables an optimization which removes the stage 0. This can (on rare occasions), improve performance. More relevantly, it might make parts of the nuXmv model more intuitive.
  - **--keep\_last\_stage** (nuXmv), None, disables an optimization which removes the last stage. This can (on rare occasions), improve performance. More relevantly, it might make parts of the nuXmv model more intuitive.
  - **--do\_not\_trim** (nuXmv), None, disables an optimization that removes parts of the tree that cannot run.

If everything goes well, your output should appear in a folder in the specified location.
Inside, you should find something like

- model\_name
  - app
	- Code or Model
  - networks, if present
  - output
    - output of simulation or verification, if requested
  - model\_name.tree

## Known Issues
If you encounter permission errors regarding copying to/from a specified location, please ensure that everything is located on your 'primary' disk. Docker sometimes seems to have issues copying to/from secondary disks.

Consider ensuring that docker can run without the use of sudo (if applicable). Please ensure that you are running Docker without the use of sudo. See https://docs.docker.com/engine/install/linux-postinstall/ .
