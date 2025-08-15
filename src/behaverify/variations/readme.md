WARNING: The encodings presented in this folder are incomplete and are not guaranteed to work for the DSL in general. They are here to generate working models based on specifically the examples in the subfolder of 2023_sefm.

Furthermore, norm is by far the most tested of these.
Even the variations based on norm are less test, and likely contain bugs that have been fixed in norm, such a bug with nodes with memory.
None of the known bugs affect the tests that these encodings are used for.


other known bugs:
you can write a tree with an unreachable node that updates a variable. if the node is pruned, then the nuxmv model will have an undefined reference. this has been fixed in norm.
