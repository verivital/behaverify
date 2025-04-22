EXAMPLE CODE FOR BT VERIFICATION

DESCRIPTION:
The files provided here contain the source code for our implementation of the methods in the paper, along with a Jupyter Notebook showing the execution and output from the example presented in section VI. The code gives an example of how these methods could be implemented. The Jupyter Notebook file (BT_Verification_Example.ipynb) augments the discussion given in section VI of the paper by showing the execution of the example presented there. The source code is split into two files: bt_verification and bt_parsing.

SIZE: 52 kB.

PLATFORM REQUIRED: A computer capable of running Python, and installing the SPOT model checker.

ENVIRONMENT: To view (but not execute) the example provided in the Jupyter Notebook file requires downloading Jupyter Notebook (available free at https://jupyter.org/install as of 2019). This requires Python to be installed (Python 3 recommended).

To execute the code (within the Jupyter Notebook or not) requires the following:
	-Python 3
	-The Python module `pyparsing`
	-Spot, model checking library, available free at https://spot.lrde.epita.fr/. This code has been tested on version 2.7.3. Installation of Spot requires a C++14-compliant compiler as well as a complete installation of Python version 3.3 or greater. The Python header files should also be installed. GNU tools `make` and `autoconf` are necessary for installation.

MAJOR COMPONENT DESCRIPTION: There are five files provided, including this README and the Summary.txt file. The other three are:
	- BT_Verification_Example.ipynb: Jupyter Notebook file containing discussion and output from the testing of the example in section VI.
	- bt_verification.py: a Python file containing functions and objects relating mainly to the verification algorithm.
	- bt_parsing.py: a Python file containing methods for parsing BTs in the syntax used in the paper.

SET-UP INSTRUCTIONS:
	-Download and install Python (if necessary).
	-Install the Python `pyparsing` module.
	-Download and install Jupyter Notebook (if necessary).
	-Download and install Spot. Ensure that Python can locate the Spot Python bindings, otherwise the `import spot` line may fail.
	-Place all of the files in the same folder.

RUN INSTRUCTIONS:
	-Run the file BT_Verification_Example.ipynb using Jupyter Notebook.
	-Run the cells in order.

EXPECTED OUTPUT: Without running any cells (even if Spot is not installed) in the BT_Verification_Example, the output should be visible. When a cell is run, the output will be replaced with the output of that execution, which should be exactly the same as what is provided.

CONTACT INFORMATION: If you have questions regarding this material, you can contact me (Oliver Biggar) at oliverb8991@gmail.com.