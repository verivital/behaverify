# Instructions for creating a .tree file for use with behaverify.tx

This document is meant as a guide for creating .tree files for use with behaverify.tx. A .tree file is necessary if you wish to convert a .tree file to .smv or into pytree code using BehaVerify. The user is assumed to generally understand how Behavior Trees work. However, as there is some pytree specific terminology, we will first provide a brief vocabulary explanation. After the terminology, we will cover the .tree format, and then give an example.

# Terminology

For brevity, we omit some mathematical terminology here. We require that a Behavior Tree have exactly 1 root node and all other nodes to have exactly 1 parent.

## Node

We consider 3 types of nodes: Leaf, Decorator, and Composite. Leaf nodes have no children, Decorators have exactly 1 child, and Composite nodes have 2 or more children. Regardless of type, all nodes can either be active or not. If a node is active its status is success, running, or failure. If a node is not active its status is invalid.

## Composite Node

A composite node is a node with 2 or more children. Children of composite nodes are ordered, meaning there is a first child, second child, etc. This order does not change. Composite nodes can be Selector, Sequence, or Parallel. Each type can also be With Memory or Without Memory (note: pytrees uses different terminology for parallel nodes). Nodes with memory can 'resume' from where they left off if they returned running instead of starting from scratch. In general, composite nodes tick their children in order until some end condition is met.

### Selector Node

A Selector node ticks each child in order until a child returns success or running at which point the Selector returns that status. If all children return failure, the Selector returns failure. A Selector With Memory that returned running will begin ticking nodes from the child node which returned running.

### Sequence Node

A Sequence node ticks each child in order until a child returns failure or running at which point the Sequence returns that status. If all children return success, the Sequence returns sequence. A Sequence With Memory that returned running will begin ticking nodes from the child node which returned running.

### Parallel Node

A Parallel node ticks each child in order until all children have been ticked. Once all children have been ticked, the Parallel node returns a status based on it's policy. Currently, we offer only two policies for parallel nodes (based on pytrees). 

1. SuccessOnAll: If any child returned failure, return failure. If any child returned running, return running. If all children returned success, return success.
2. SuccessOnOne: If any child returned failure, return failure. If any child returned success, return success. If all children returned running, return running.

A Parallel Node With Memory and the SuccessOnAll policy that returned running will tick ONLY the children that returned running.

## Decorator Nodes

A Decorator node is a node with exactly 1 child. The purpose of a decorator node is generally to modify the behavior of the child node. Currently, the only supported decorator type is X_is_Y. 

### X_is_Y

If the child of an X_is_Y node returns the status X, the node will return Y. Thus if X is running and Y is failure, it would convert running into failure.

## Leaf Node

A Leaf node is a node with no children. We consider three types of leaf nodes: Check, Check_Environment, and Action. Note that Check and Check_Environment nodes could be written as Action nodes.

### Check Node

A Check node evaluates a given statement. If the statement is true, it returns success. Otherwise, it returns failure. In general, this checks the status of some blackboard variables (shared memory). Specific details on what a statement can look like are provided later.

### Check Environment Node

This functions in the same way as a Check Node, but instead of evaluating a statement based on shared memory, the node queries the environment. Details provided later.

### Action Node

A more general Leaf node, it can return success, failure, or running depending on conditions. It is possible to update shared memory, read the environment, and 'act' upon the enviroment (e.g., a robot control could issue a "go forward" command). Details are provided later.

## Blackboard

Nodes can share memory by writing information to the Blackboard.


# The .tree Format

The .tree file is seperated into various sections. The order is as follows:

1. variables - These are blackboard variables, representing shared memory
2. local variables - These are variables that are not shared between nodes.
3. environment variables - These are variables that represent the environment.
4. check nodes - These were described above
5. check environment nodes - These were described above
6. action nodes - These were described above
7. the tree itself
8. tick prerequisite - Here you can specify a condition which must be met in order for a tick to occur. This is used to allow the simulation to 'end'. THIS SECTION IS OPTIONAL.
9. specifications - Here you can specify specifications to be checked.

Each section, except tick prerequisite, is required. Before covering the sections, we will introduce Code Statements and Variable Statements.

## Code Statement

A Code Statement is of the following form:

```
    code_statement:
    (constant = STRICTFLOAT) | (constant = INT) | (constant = BOOL) | (constant = STRING) |
    (is_local ?= 'local' variable = [variable]) |
    ('(' function_call = function ')') |
    ('(' code_statement = code_statement ')')
;
```

Intuitively, this means that a Code Statement can be 
1. a Constant : this can be of type Float, Int, Bool, or String.
2. a Variable : note that in a code statement you will simply use the name of the variable.
3. a Function surrounded by parantheses : these are of the form (function, value1, value2...). Note that value1, value2, etc are all code statements. A full list of functions will be included somewhere. (or you can look in the behaverify.tx file).
4. a CodeStatement surrounded by parantheses : this condition means you an always include more parantheses.

Thus, an example would be

```
(addition, varA, (multiplication, (varB), 3), 1)
```
which is of course
```
varA + ((varB) * 3) + 1
```

Currently, there is no type checking. It is on the user to ensure that the statement makes sense (i.e, do not add a string to an integer).

## Variable Statement

A Variable Statement is of the following form:
```
    variable_statement:
    'variable_statement' '{'
    is_local ?= 'local' variable = [variable]
    case_results *= variable_case_result
    default_result = variable_default_result
    '}' 'end_variable_statement'
;
```
The purpose of the Variable Statement is to assign a value to a variable. Each Case Result is a (Condition, Value) pair. If the Condition is met, the Value is used. If no Condition is met, the Default value is used, as declared in Default Result. Each Condition is a Code Statement. Each Value is one or more Code Statements. Thus, for example:

```
variable_statement {
	varA
	case { (equal, 0, 1) } end_case result { 0, 1, (addition, varA, 1) } end_result
	case { (or, varB, (not, varC)) } end_case result { 0, (mod, 12, varA) } end_result
	result { 1 } end_result
} end_variable_statement
```
This corresponds to the following python code sequence:
```
if 0 == 1:
  varA = random.choice([0, 1, varA+1])
elif varB or not varC:
  varA = random.choice([0, 12 % varA])
else:
  varA = 1
```
Note that this means each Condition should ultimately return a Boolean value. This is not currently typed check. It is up to the user to enforce this. Similiary, if varA is a variable that is supposed to be a String, it is up to the user to ensure that a String value is provided.

## Variables

The first section will be the Variable section representing the blackboard variables in the model. The section is formatted as

``` 
variables {
declare variables here
} end_variables
```

All blackboard variables used in the model must be declared within this section.

A variable declaration is defined as:

```
variable:
    'variable' '{'
    name = ID
    ((model_as = 'VAR' domain = variable_domain) | (model_as = 'FROZENVAR' domain = variable_domain) | (model_as = 'DEFINE'))
    '}' 'end_variable'
;
```

Thus an example would be

```
variable { varA VAR [0, 3] } end_var
```

Note that usually, environment variables are not allowed in variable statements. When they are allowed, you must use env before the variable name (e.g env varE).

### model_as

The three options for modeling are VAR, FROZENVAR, and DEFINE.

1. DEFINE : DEFINE is an unchanging constant. 
2. FROZENVAR : FROZENVAR is initially set to some value, and then never changes.
3. VAR : VAR can change at each state.

### domain

The three options for variable domains are [minVal, maxVal], BOOLEAN, and {enum1, enum2...enumK}.

1. [minVal, maxVal] : both minVal and maxVal must be an integer
2. BOOLEAN : represents True and False
3. {enum1, enum2...enumK} : an enumration of options

Note that an enum could be an int or a string. Thus {0, 'potato', 3, 'tomato'} is a valid set of enumerations. However, {'1.3', True, 'TRUE'} would all fail, if not here, then when the .smv file is ran. '1.3' would fail because it would end up being represented as 1.3 in .smv, and nuXmv does not allow floats in enumerations. True and 'TRUE' would fail because nuXmv places restrictions on booleans appear inside enumerations. However {'True', '3'} would be acceptable.

Note that a DEFINE variable does not have a domain.

### How Variables Are Used

Note that the variable declaration does not say anything about how the variable changes over time, or even what the initial value is. This information will be conveyed within the various check, check_environment, and action nodes.

## local variable

These are defined identically to variables. The difference is they are used slightly differently in nodes and cannot appear in certain places. The local variable secion is formatted as

``` 
local_variables {
	declare local variables here
} end_local_variables
```

## environment 

As the environment variables are meant to model the environment, these involve a bit more complexity compared to variables and local variables. While they are declared the same way, we also need to specify what values they take at the start and how they change over time. The section is formatted as

```
environment {
	environment_variables {
		declare variables here
	} end_environment_variables
	initial_values {
		declare initial values here
	} end_initial_values
	update_values {
		declare update values here
	} end_update_values
} end_variables
```
Environment variables are declared as

```
environment_variable:
'environment_variable' '{'
name = ID
((model_as = 'VAR' domain = variable_domain) | (model_as = 'FROZENVAR' domain = variable_domain) | (model_as = 'DEFINE'))
'}' 'end_environment_variable'
;
```

The initial and declare values consist of Variable Statements, which were defined above.

## Nodes

At this point, all the variables have been declared. The next step is to define the various nodes that will be used. Only the Leaf nodes need to be defined.

## Check Nodes

Check nodes are used to check Blackboard Variable values. This section looks like this:

```
checks {
	declare check nodes here
} end_checks
```
Each check node looks as follows:
```
    check_node:
    (node_type = 'check') '{'
    name = ID
    'read_variables' '{' read_variables *= [variable]  '}' 'end_read_variables'
    ('condition' '{' condition = code_statement '}' 'end_condition')
    '}' 'end_check'
;
```
Note that while the Read Variables are required, this information is only used when generating a Python file. These are used to properly set blackboard permissions in py_trees. The Condition is a Code Statement. This Code Statement should evaluate to a Boolean, but type checking is not enforced. If the Condition is True, the node will return success, and otherwise it will return failure. Note that the Condition CANNOT use Environment or Local Variables.

Thus an example is:
```
check {
	checkName
	read_variables { varA varB } end_read_variables
	condition { (equal, (multiplication, varA, 2), varB) } end_condition
} end_check
```
Thus this check will return success if 2*varA=varB, else failure.

## Check Environment Nodes

Check Environment Nodes are used to check environment variables. This section looks like this:

```
environment_checks {
	declare environment checks
} end_environment_checks
```

Each environment check looks as follows:
```
    check_environment_node:
    (node_type = 'check_environment') '{'
    name = ID
    ('imports' '{' imports *= STRING[','] '}' 'end_imports')?
    ('python_function' '{' python_function = STRING '}' 'end_python_function')?
    ('condition' '{' condition = code_statement_env '}' 'end_condition')
    '}' 'end_check_environment'
;
```

Here imports and python function are optional and only used when generating py_trees. Condition is the same as in Check Nodes, except the code statement is now allowed to contain Environment Variables. Thus an example would be:

```
check_environment {
	checkEnvName
	imports { 'myImport' } end_imports
	python_function { 'myImport.myFunction()' } end_python_function
	condition { (equal, env varE, 1) } end_condition
} end_check_environment
```

Thus this is an environment check that returns success if the environment variable varE is equal to 1, and failure otherwise. In a py_tree, this environment check node will instead call myImport.myFunction(). If the result is true, the node will return success, otherwise it will return failure.

Note that when referencing an environment variable in a code statement, you must preceed the variable name with 'env'.

## Action Nodes

Any leaf node that is not a Check or Environment Check node is an Action node. Note that it is possible to recreate the behavior of a Check node or Environment Check with an Action node. Action Nodes are also the only place where Local Variables are used. This section looks as follows:

```
actions {
	declare actions here
} end_actions
```

Each action is of the following form:

```
    action_node:
    (node_type = 'action') '{'
    name = ID
    ('imports' '{' imports *= STRING[','] '}' 'end_imports')?
    'read_variables' '{' read_variables *= [variable]  '}' 'end_read_variables'
    'write_variables' '{' write_variables *= [variable]  '}' 'end_write_variables'
    'initial_values' '{'
    init_statements *= statement
    '}' 'end_initial_values'
    'update' '{'
    pre_update_statements *= statement
    return_statement = return_statement
    post_update_statements *= statement
    '}' 'end_update'
    '}' 'end_action'
;
```

Imports is optional, as described in Check Environment Nodes. Read Variables and Write Variables are required, but only for setting permissions in py_trees. The first core of the Action Node is the initial values subsection. This subsection defines the initial values of variables and local variables. Initial values consist of Statements. These can be Variable Statements, as described earlier, or Read Statements, or a mixture of both. The purpose of a Read Statement is to copy the value of an Enviornment Variable into a Blackboard Variable. Formally, they are as follows:

```
    read_statement:
    'read_environment' '{'
    ('python_function' '{' python_function = STRING '}' 'end_python_function')?
    (('condition' '{' condition = code_statement_env '}' 'end_condition') | (is_local = 'local' condition_variable = [variable]))
    'set_variables' '{' variable_environment_pairs *= variable_environment_pair[','] '}' 'end_set_variables'
    '}' 'end_read_environment'
;
```
Here python function is only used in py_tree generation and represents how the code would read the environmeent. You must either provide a Condition under which the environment is successfully read or, if non-determinism is preferred, assign a Local Variable to store whether or not the read was successful. Each Variable Environment pair couples a Local or Blackboard Variable with an Environment variable.

Thus an example would be
```
read_environment {
	python_function { 'importedByActionNode.myFunc()' } end_python_function
	condition { True } end_condition
	set_variables { (varA, env varE), (local varB, env varE) } end_set_variables
} end_read_environment
```

This example would set varA to the value of the environment variable varE. It would also set the Local Variable varB to the value of the environment variable varE. Another example would be

```
read_environment {
	python_function { 'importedByActionNode.myFunc()' } end_python_function
	local varC
	set_variables { (varA, env varE), (local varB, env varE) } end_set_variables
} end_read_environment
```

Which will do the same thing, but it can nondeterministically succeed or fail. If it fails, the local variable varC will be set to false. If it succeeds, the local variable varC will be set to true.

The second core section of Action nodes is the Update section. This defines how variables and local variable are changed by the Action node, as well as how the Action node detremines what value to return. Pre-update statements and post-update statements can be Variable statements, read statement, or write statements. These are divided into pre and post so that the return value can be determined using intermediate variable values. We've covered Variable Statements and Read Statements before, so here we will only describe Write Statements.

The purpose of a Write Statement is to affect the Environment. Formally, this looks as follows:

```
	write_statement:
    'write_environment' '{'
    ('python_function' '{' python_function = STRING '}' 'end_python_function')?
    'update_values' '{'
    update *= environment_statement
    '}' 'end_update_values'
    '}' 'end_write_environment'
;
```
An environment statement is like a variable statement, except it can use environment variables. Additionally, it can be marked as instant. Instant environment statements take place immediately, while non-instant environment statements take place after the tick ends, but before environment variables update. Remember to use env before any environment variable names. An example is then:

```
write_environment {
	python_function { 'importedByActionNode.myFunc()' } end_python_function
	update_values {
		environment_statement {
			instant
			env varE
			case { local varB} end_case result { 0 } end_result
			result { 1, 2 } end_result
		} end_environment_statement
		environment_statement {
			env varF
			case { local varB} end_case result { 0 } end_result
			result { 1, 2 } end_result
		} end_environment_statement
	} end_update_values
} end_write_environment
```

Thus this is a Write Statement which will immediately set varE to 0 if the local variable varB is true, and otherwise nondeterministically pick 1 or 2. It will also set varF to 0 if the local variable varB is true and 1 or 2 otherwise, but this will not take place until later.

Finally, return statements are like variable statements. They look as follows:
```
    return_statement:
    'return_statement' '{'
    case_results *=  status_case_result
    default_result = status_default_result
    '}' 'end_return_statement'
;
```

Thus an example would be:

```
return_statement {
	case { varA } end_case result { success } end_result
	result { failure } end_result
} end_return_statement
```

Thus the action node with this return statement would return success if varA is true, and failure otherwise.

Putting it all together, an example of an action node would be:

```
action {
	get_mission
	imports {'robot'} end_imports
	read_variables {} end_read_variables
	write_variables {mission target_x target_y} end_write_variables
	initial_values {
		variable_statement {
			mission result { False } end_result
		} end_variable_statement
		variable_statement {
			target_x result { 0 } end_result
		} end_variable_statement
		variable_statement {
			target_y result { 0 } end_result
		} end_variable_statement
	} end_initial_values
	update {
		read_environment {
			python_function { 'robot.get_mission()' } end_python_function
			local saw_target
			set_variables { (target_x, env x_goal), (target_y, env y_goal) } end_set_variables
		} end_read_environment
		variable_statement {
			mission
			case { local saw_target } end_case result { True } end_result
			result { False } end_result
		} end_variable_statement
		return_statement {
			case { local saw_target } end_case result { success } end_result
			result { failure } end_result
		} end_return_statement
	} end_update
} end_action
```

This is an Action called get_mission. It imports robot. It does not need read permissions, but it does need write permissions for mission, target_x, and target_y. It initializes mission to False, target_x to 0, and target_y to 0. When it upates, it nondeterministically reads the environment, potentially setting target_x and target_y. It then updates based on the result of the nondetermisim, which was stored in the local variable saw_target. It then also returns based on the value of saw_target.


## The Tree

The tree is obviously used for modeling. The tree wil be walked using a Depth First Pattern until all nodes have been visited. Each visited node will be modeled. Furthermore, all of the initializations and updates will be handled in this oder.. Therefore, if you place Node1 before Node2 in the tree, all of the statements in Node1 will occur before any of the statements in Node2. For a more concrete example, consult the walkthrough provided later on.

## Variable Stages - Differences between Encoding and Reality

Suppose we have a simple tree. A parallel root with 2 children, A and B. A has a variable statement which sets the variable V to False. B has a variable statement which sets the variable V to True. Both Nodes are ACtion Nodes which return Success.

In reality, a tick will look as follows:

1. The Root receives a tick signal. Because it is a parallel node, it begins to run the children. It sends a tick to A.
2. A receives a tick signal. A will set V to False, and then return Success.
3. The Root sees that A has returned Success, and so it continues to run the children. It sends a tick to B.
4. B receives a tick signal. B will set V to True, and then return Success.
5. The Root sees that B has returned Success, and so it continues to run the children. Since there are no more children to run, it returns (in this case, with Success).
6. The tick is now over.

Note that these events happen one at a time sequentially. If one were to open a debugger you could step through these events. However, a direct encoding which mimics this exact behavior is very inefficient. Therefore, the BehaVerify encoding used considers the entire sequence of events above as happening during a single step. This greatly improves performance and makes reasoning about the outcome of a tick substantially simpler. However, it can complicate variable logic. Let us consider how V is handled in BehaVerify.

1. New tick begins. Via a set of equations, both A and B realize that they will be active during this tick.
2. Because both A and B are active, A will set V to False and B will set V to True.
3. Therefore, V_stage_1 is set to False, and V_stage_2 is set to True, because A comes before B in the tree.

In essence, V is now 3 variables instead of 1: V, V_stage_1, and V_stage_2. Through various encoding tricks, this doesn't increase the number of states the model needs to consider unless one of these stages can be set non-determinisitically. None of the information has been lost.

Finally, suppose we had a more complicated tree, one where if node A sets V then node B does NOT set V and vice versa. In this case, we will still use three stages! It doesn't matter that in practice, V can only be set once, all three stages will still be used. Naturally, this means that if A sets the value of V, which means V_stage_1 is False, then V_stage_2 would now also be False. The reverse, however, is not true, because B comes after A.


## Specifications

A model can be useful without specifications. You could run simulation events manually to confirm how various things might work. However, writing specifications can greatly improve the use of the model by providing formal guarantees. We allow for three types of Specifications to be written: Invariant, LTL, CTL. All three use a similar structure.

### Invariant

An Invariant is a specification that we want to always be true. For instance, the statement "x is always greater than 0" would be an invariant specifications. The statement "at some point in time x is greater than 0" is NOT an Invariant specification.

NOTE: If possible, you should write your specifications as Invariants. This is because while an Invariant specification can easily be written using LTL or CTL, nuXmv will check invariant specifications far more efficiently because it is able to make various simplifying assumptions.

An invariant specification takes the following form :
```
(spec_type = 'INVARSPEC' '{' CodeStatement = CodeStatementINVAR '}' 'end_INVARSPEC')
```
Note that we've already seen what CodeStatement is. CodeStatementINVAR is like CodeStatement, except several new functions are allowed. One key difference is that CodeStatementINVAR allows NodeNames to appear inside specific functions. Those functions are:

- active : this function will return true if the node is active and false otherwise. E.G. (active, nodeA). 

- success : this function will return true if the node returned success and false otherwise. E.G. (success, nodeA).

- running : this function will return true if the node returned running and false otherwise. E.G. (running, nodeA).

- failure : this function will return true if the node returned failure and false otherwise. E.G. (failure, nodeA).

Note that the grammar will parse even if the node name does not refer to a node that actually exists. It is up to the user to check that the node in question exists.

An example invariant specifcation, then, is as follows
```
INVARSPEC { (implies, (active, nodeA), (active, nodeB)) } end_INVARSPEC
```
This specification states that if nodeA is active, then nodeB is active.

The second key difference between CodeStatement and CodeStatementINVAR is that CodeStatementINVAR requires you to specify an additional bit of information with respect to variables. This is because of the Variable Stages discussed earlier. Each variable must now be followed by an Integer.

- -1 : This indicates that the last stage of the variable should be used (i.e, the value the variable has at the end of the tick).

- 0 : This indicates that the 0th stage of the variable should be used (i.e, the value the variable has at the start of the tick).

- x : (x is positive). This indicates that xth stage of the variable should be used. If x is 1, then this means the first stage, meaning after the variable has been set 1 time. If x exceeds the number of stages the variable has, then it defaults to the last stage.

Thus we could write a specification as follows
```
INVARSPEC { (or, (active, nodeA) (equal, varA 1, -5)) } INVARSPEC
```
Which states that nodeA is active, or varA_stage_1 is -5, or both.


### CTLSPEC

In some cases, a specification requires the concept of time and an Invariant specification cannot describe it adequately. In these cases, either a CTL or LTL spec is required. From personal experience, CTL specifications seem to generally perform faster than LTL specifications, though the output is generally cryptic by comparison and they seem harder to reason about.

The primary difference between a CTL specificaiton and an Invariant Specifcation is, as mentioned, the presence of time. When writing a CTL specification, various additional functions are enabled in order to reason about time, though they cannot always be used. An example of this would be the following:
```
CTLSPEC { (exists_finally, (active, nodeA)) } end_CTLSPEC
```
Which specifies that there exists a path where eventually nodeA is active. In general, you cannot make specifications regarding time within certain specific functions. 
```
CTLSPEC { (equal, (addition, (exists_finally, varA 0), 1) 1) } end_CTLSPEC
```
Is therefore invalid and will throw an error when parsed. However
```
CTLSPEC { (exists_finally, (equal, (addition, varA 0, 1) 1)) } end_CTLSPEC
```
is completely acceptable. Note also that a time specification need not be at the highest level. For instance:
```
CTLSPEC { (or, (always_finally, (active, nodeA)), (exists_globally, (active, nodeB))) } end_CTLSPEC
```
which specifies that either the nodeA is always eventually active, or there exists a path where nodeB is always active. 

Time can be specified using the following functions:

- exists_globally : there exists a path where the condition always holds

- exists_next : there exists a path where in the next state the condition holds

- exists_finally : there exists a path where eventually the condition holds

- exists_until : there exists a path where condition1 holds until condition2 holds

- always_globally : on every path the condition always holds

- always_next : on every path the condition holds in the next state

- always_finally : on every path the condition eventually holds 

- always_until : on every path condition1 holds until condition2 holds

Note that these can be combined. For instance:
```
CTLSPEC { (exists_finally (always_globally, (active, nodeA))) } end_CTLSPEC
```
is a specification that states that there exists a path where eventually all subsequent paths always an active nodeA.

Note that each of these functions takes 1 argument, except the until functions which take 2.


### LTLSPEC

Finally, there are LTL specifications. These function exactly like CTL specifications, except the list of time functions is different. It is as follows:


- next : in the next state, the condition holds.

- globally : in all states, the condition holds

- globally_bounded : in all states (within the bound) the condition holds

- finally : the condition eventually holds

- finally_bounded : the condition holds at some point within the bound

- until : condition1 holds until condition2 holds

- until_bounded : condition1 holds until condition2 holds during the bound

- release : condition1 holds until condition2 holds (unlike until, when the swap happens both must hold)

- release_bounded : condition1 holds until condition2 holds during the bound (unlike until, when the swap happens both must hold)

- previous : the condition held in the previous state (false at initial state)

- not_previous_not : the condition held in the previous state (true at initial state)

- historically : the condition has always held

- historically_bounded : the condition always held during the bound

- once : the condition held at some point in the past

- once_bounded : the condition held at some point in the past in the specified bound

- since : condition1 held until condition2 held

- since_bounded : condition1 held until condition2 held during the bound

- triggered : condition1 held until condition2 held (unlike since, when the swap happened both must have held)

- triggered_bounded : condition1 held until condition2 held during the bound (unlike since, when the swap happened both must have held)


The main new feature is the introduction of bounds. A bound can take one of two forms

[minVal, maxVal]

[minVal, +oo]

where +oo represents infinity.


# A guided example of the entire process

Here we will walk through creating a tree. Comments, marked by #comment# ACTUAL COMMENT #end_comment# will explain why something is being done. The idea will be as follows: we want to create a tree that controls a robot that gets cookies to the user.

```
variables {
	variable { on_a_mission VAR BOOLEAN } end_variable 
	#comment# We will use this variable to store if we are on a mission, which we will store as a Boolean #end_comment#
} end_variables
local_variables {} end_local_variables #comment# no local variables for this example #end_comment#
environment {
	environment_variables {
		environment_variable { cookies_requested VAR BOOLEAN } end_environment_variable
		environment_variable { num_cookies VAR [0, 3] } end_environment_variable
		#comment# we will use this to track the number of cookies #end_comment#
	} end_environment_variables
	initial_values {
		#comment# we don't set an initial value for cookies_requested. #end_comment#
		#comment# we don't set an initial value for num_cookies. this represents the possibility of there already being cookies in the house. #end_comment#
	} end_initial_values
	update_values {
		environment_statement {
			env cookies_requested
			case { env cookies_requested} end_case result { True } end_result
			result {True, False} end_result
		} end_environment_statement
		#comment# cookies can be requsted at any point, but once requested, can't be unrequsted #end_comment#
		#comment# we assume that cookies don't appear or disappear in general, so we need to clarify that #end_comment#
	} end_update_values
} end_environment
checks {
	check {
		#comment# this will just check if we're on a mission #end_comment#
		on_mission
		read_variables { on_a_mission } end_read_variables
		condition { on_a_mission } end_condition
	} end_check
} end_checks
environment_checks {
	check_environment {
		#comment# this will just check if a mission was requested #end_comment#
		mission_called
		imports { 'cookie_robot_interface' } end_imports
		python_function { 'cookie_robot_interace.cookies_requested()' } end_python_function
		condition { env cookies_requested } end_condition
	} end_check_environment
	check_environment {
		#comment# checks if cookies already exist #end_comment#
		cookies_present
		imports { 'cookie_robot_interface' } end_imports
		python_function { 'cookie_robot_interace.cookies_present()' } end_python_function
		condition { (greater_than, env num_cookies, 0) } end_condition
	} end_check_environment
} end_environment_checks
actions {
	action {
		set_mission
		read_variables {} end_read_variables
		write_variables { on_a_mission } end_write_variables
		initial_values {
			variable_statement {
				on_a_mission
				result { False } end_result
			} end_variable_statement
		} end_initial_values
		update {
			variable_statement {
				on_a_mission
				result { True } end_result
			} end_variable_statement
			return_statement { result { success } end_result } end_return_statement
		} end_update
	} end_action
	action {
		bake_cookies
		imports { 'cookie_robot_interface' } end_imports
		read_variables {} end_read_variables
		write_variables {} end_write_variables
		initial_values {} end_initial_values
		update {
			write_environment {
				python_function { 'cookie_robot_interface.bake()' } end_python_function
				update_values {
					environment_statement {
						env num_cookies
						result { 0, 1, 2, 3 } end_result
					} end_environment_statement
				} end_update_values
			} end_write_environment
			return_statement { result { running } end_result } end_return_statement
		} end_update
	} end_action
	action {
		serve_cookies
		imports { 'cookie_robot_interface' } end_imports
		read_variables {} end_read_variables
		write_variables {} end_write_variables
		initial_values {} end_initial_values
		update {
			write_environment {
				python_function { 'cookie_robot_interface.serve()' } end_python_function
				update_values {
					environment_statement {
						env num_cookies
						result { (max, 0, (subtraction, env num_cookies, 1)), (max, 0, (subtraction, env num_cookies, 2)), (max, 0, (subtraction, env num_cookies, 3)) } end_result
					} end_environment_statement
					environment_statement {
						env cookies_requested
						result { False } end_result
					} end_environment_statement
				} end_update_values
			} end_write_environment
			return_statement { result { success } end_result } end_return_statement
		} end_update
	} end_action
} end_actions
root_node
composite {
	cookie_control
	sequence
	#comment# Cookie Control is our root node.
	It is a sequence, so it goes to the next child only if the current child returns success.
	The False means no memory #end_comment#
	children {
		#comment#
		We will first Confirm we have a mission
		then we will confirm we have cookies
		then we will serve cookies.
		#end_comment#
		composite {
			confirm_mission
			selector
			children {
				#comment#
				First, check if we are alredy on a cookie mission.
				If we aren't, see if someone has asked for cookies.
				#end_comment#
				on_mission
				composite {
					check_new_mission
					sequence
					children {
						mission_called
						set_mission #comment# mark the new mission. #end_comment#
					} end_children
				} end_composite
			} end_children
		} end_composite
		composite {
			confirm_cookies
			selector
			#comment# before we can serve cookies, we need to have cookies.
			Check if we have cookies, if we do, done.
			If not, bake cookies.#end_comment#
			children {
				cookies_present
				bake_cookies
			} end_children
		} end_composite
		serve_cookies
	} end_children
} end_composite
tick_prerequisite {True} end_tick_prerequisite #comment# since in this case, our prerequisite is just True, we could have omitted this#end_comment#
specifications {
	INVARSPEC { (implies, (greater_than,  env num_cookies 0, 0), (not, (active, bake_cookies)))} end_INVARSPEC #comment# this one is true #end_comment#
	CTLSPEC { (always_globally, (implies, env cookies_requested 0, (always_finally, (active, serve_cookies)))) } end_CTLSPEC #comment# this one is false #end_comment#
} end_specifications
```

This exaqmple file can also be found at ./examples/guided_tree/guided_tree.tree, so you don't need to copy it from here.
