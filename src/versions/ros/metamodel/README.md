# Instructions for creating a .bt file for use with btree.tx

This file will not currently contain all relevant information. Specifically it will omit anything that deals solely with code generation. This file will therefore focus on the modeling side.

## Variables

All variables that will be used in the model must be declared in the appropriate section. A variable must be of the following format
```
'var' type=[Type] name=ID ('=' default=DefaultBBType)? (',' 'model_as' '(' model = ModelOptions (',' initial_value = Enumeration)? ')')? ';'
```
Note that while initial_value is listed as being of Enumeration type, this will also accept Ints or boolean values. Thus an example would be
```
var bool example = False , model_as(bool, False);
```
Note that in the above example, the type and model are both bool. Similarly, the default and initial value are both False. This need not be the case. For instance
```
var String example2 = 'potato', model_as([0,3], 2);
var SomeComplexMessagetype example3, model_as({'safe', 'unsafe'}, 'safe');
```
is completely acceptable, though perhaps not productive for the goals of accurately modeling. Below we explain using example2 what each part means

- type : type defines what type the variable is IN CODE GENERATION. This has no effect on the model. This paramater is required.

- name : the name of the variable. This is used in the model and in code generation. This paramater is required.

- default : the default value (if any) to be used IN CODE GENERATION. This has no effect on the model. This paramter is optional.

These first three values are what is used by code generation. Of the three, only name matters for modeling. Note then that it is possible to declare a variable as follows
```
var Float32 example4;
```
Because example4 does NOT have a model_as statement, it will not be modeled. example4 would only be used in code generation. Continuing with the explanation.

- model : model defines what type the variable is in the model. This has no effect on code generation, it is only used in the model. If the variable is to be modeled, this paramater is required.

- initial_value : initial_value defines what value the variable should initially have in the model. This has no effect on code generation, it is only used in the model. This paramater is optional.

Thus the model information from example2 would be as follows: name is example2, model is [0, 3], initial value is 2. 

### ModelOptions

ModelOptions describes what domains can be used to model a variable. ModelOptions must be of the following format
```
(is_bool = 'bool') | ('{' enums += EnumerationDec[','] '}') | ( '[' range_minimum = INT ',' range_maximum = INT ']')
```
Thus the three modes, so to speak, would be: bool, {enum1, enum2, ..., enumK}, [minVal, maxVal]. Note that an enum could be an int or a string. Thus {0, 'potato', 3, 'tomato'} is a valid set of enumerations. However, {'1.3', True, 'TRUE'} would all fail, if not here, then when the .smv file is ran. '1.3' would fail because it would end up being represented as 1.3 in .smv, and nuXmv does not allow floats in enumerations. True and 'TRUE' would fail because nuXmv places restrictions on booleans appear inside enumerations. However {'True', '3'} would be acceptable.


## Nodes

Once all variables are declared, we will need to be able to use them. Variables are used within Nodes. The main way to use variables in Nodes is through a set() declaration. A Node can have any number of set declarations, but they must be placed in the appropriate section. The order of set declarations matters: they will be executed in the order they are presented.


### set declaration

A set declaration defines how the variable should be updated when the node runs. set declarations must be of the following format
```
'set' '(' variable = [BBVar] ',' updates *= UpdateStatement default_update = CodeStatement')'
```
Thus two examples would be
```
set(example, True)
set(example2, try((not, example), (addition, example2, 1)), (any, 0, (subtraction, example2, 1)))
```
The first example sets the variable example to be True. The second example sets the variable example2 to be example2 + 1 if example is False, else it picks non-deterministically form 0 and example-1. In python code, this is equivalent to the following
```
if not example: example2 = example2 + 1
else: example2 = random.choice([0, example2 - 1])
```
Note that you can have any number of try statements, including 0. Furthermore, note that if a node had both of our examples as set declarations, it would be the same as the following python code segment
```
example = True
if not example: example2 = example2 + 1
else: example2 = random.choice([0, example2 - 1])
```
Let us now more specifically disect example2. it consists of 3 parts

- variable : this informs us which variable is being updated. In this case it's example2

- updates : these are the statements to try. The first update that succeeds will be applied. Update statements are described in more detail below

- defualt_update : this is the value to use if none of the updates applied. This is a CodeStatement. CodeStatements are described in more detail below.

### Update Statement

An update statement is a pair (condition, update_value). If the condition is True, then the update_value is used. Update Statements must be of the following format
```
'try(' condition = CodeStatement ',' update_value = CodeStatement ')' ','
```
Note that the comma at the end is to ensure each entry in the set declaration is comma separated, for asthetic reasons. Unfortunately, there was no easier way to handle this.

CodeStatement is described in more detail below. However, note that a CodeStatement need not resolve to a True or False according to the grammar. It is up to the user to ensure that the condition is actually something that can resolve to True or False (e.g, 'potato' is a valid CodeStatement, but would not function as a condition. However, type checking this is not currently enabled).

### CodeStatement

A CodeStatement is of the following format:
```
(constant = STRICTFLOAT) | (constant = INT) | (constant = BOOL) | (constant = STRING) | (variable = [BBVar]) | ('(' function_call = function ')') | ('(' CodeStatement = CodeStatement ')')
```
Intuitively, this means your code statement can be

1. a constant (float, int, bool, or string)

2. a variable. Note that the variable itself must be declared in the appropriate variable section, as described above. Here you will simple refer to the variable using it's name.

3. a function. all functions are of the form (FUNCTION_NAME, VALUE1, VALUE2, ...). Note that the surrounding () are required. A full list of functions can be found in btree.tx

4. a CodeStatement surrounded by (). I.E, you don't need to worry about adding in too many paranthesis. 


## Input Nodes

Input Nodes are a specific type of node. In general, it is assumed that an input node is monitoring some topic. If new data came in, then it will update a variable and return success, and potentially run some other code in the process. If no new data came in, then it returns running. Note that an Input Node will only excecute its set declarations if it received new data.

An InputNode is of the following format :
```
'input' name=ID input_topic=[Topic] '->' topic_bbvar=[BBVar] ('vars' bb_vars *= [BBVar][','] ';')? args *= Param ('comment' comment=STRING)? 
ignore_topic ?= 'model_ignore_topic' ignore_node ?= 'model_ignore' set_vars *= SetVar
'end'(';')?
```

For the purpose of modeling, we are interested in the following elements:

- name : the name of the Input Node.

- topic_bbvar : this identifies the variable that will be update when the Input Node receives new data from the input topic

- ignore_topic : this is a flag that, if present, indicates we will not be copying the input_topic into the topic_bbvar. Note that set var declarations still only trigger if new data was received.

- ignore_node : this is a flag that, if present, indicates we will not be modeling this node.

- set_vars : explained earlier as set declarations.

Note that ignore_topic and ignore_node can be useful tools for reducing the size of the model, but should be used with caution.

## Task Nodes

Task Nodes are a specific type of node. If a task node is ticked, then all of its set declarations are executed in order and it returns the appropriate status.

A TaskNode is of the following format :
```
'task' name=ID ('in' input_topics+=TopicArg[','] ';')? ('out' output_topics+=TopicArg[','] ';')?
('vars' bb_vars *= [BBVar][','] ';')? args*=Param ('comment' comment=STRING (';')?)?
set_vars *= SetVar 'return' return_status = StdBehaviorType
'end'(';')?
```
For the purpose of modeling, we are interested in the following elements:

- name : the name of the Task Node.

- set_vars : explained earlier as set declarations.

- return_status : this is either success or running or failure. This indicates what the task node returns. Note that the task node is assumed to always return the same status (because that's how all of the task nodes so far have worked).

## The Tree

The tree is obviously used for modeling. The tree wil be walked using a Depth First Pattern until all nodes have been visited. Each visited node will be modeled (unless marked as ignore (see Input Nodes)). Furthermore, all of the set declarations will be processed IN THIS ORDER. Therefore, if you place Node1 before Node2 in the tree, all of the set declarations in Node1 will occur before any of the set declarations in Node2.

## Variable Stages - Differences between Encoding and Reality

Suppose we have a simple tree. A parallel root with 2 children, A and B. A has a set declaration which sets the variable V to False. B has a set declaration which sets the variable V to True. Both Nodes are Task Nodes which return Success.

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

Here we will walk through creating a tree. Comments, marked by // will explain why something is being done.

```
system exampleSystem; //this is required, but adds no information to the model.
type notUsedSimple; //each 'SimpleType' we declare can be used for code generation. Because we want to include some variables, we need at least one SimpleType for code generation. This will not be used in the model
message notUsedMessage notUsedPackage end; //this is needed if we want to use an input node, which we do, because this is an example.
topic notUsedMessage notUsedTopic hi; //this is needed if we wnat to use an input node, which we do, because this is an example.
var notUsedSimple varA, model_as({'on', 'off', 'unknown'}, 'off'); //we've defined a variable named varA, which can be in 3 states: on, off, or unknown. it starts as off
var notUsedSimple varB, model_as(bool, False); //we've defined a variable named varB, which is a boolean. it starts as false.

input inputNode notUsedTopic -> varA //here we are declaring an Input Node. It will monitor the topic and set varA if a new value appears (this is abstracted as being set to a random value). if a random value would ruin the model, you are encouraged to use model_ignore_topic and instead set a new value using a set declaration.
set(varA, try((equal, varA, 'unknown'), 'off'), varA) //if the new value of varA is unknown, we will set varA to off, otherwise, we don't change the value
//varB is not set in this node.
end

//here we could write a check node. Check nodes are handled automatically and are fairly straight forward, so they weren't explained above.
check is_varB varB == True; //checks if varB is True.

task taskNode
set(varB, (equal, varA, 'on')) //sets varB equal to the result of varA == 'on'
set(varA, try(varB, varA), (any, 'off', 'unknown')) //if varB is true, then varA does not change. if varB is false, set varA nondeterministically to 'off' or 'unknown'
return success //value to return
end;
//now we construct the tree

tree ( updatetime = 1 , timeout = 1 ) //information for codeGeneration, we don't need any of this, but requred.
seq theRoot //our root node can have any name. this one is a sequence node. 
{
	mon inputNode //our first child is the input node
	sel someName // our second child is a selector node with a very creative and descriptive name
	{
		chk is_varB //our first child of the selector node
		exec taskNode //our second child of the selector node
	}
}
// here we could specify a tick pre-requisite. If one is not specified, the tree always ticks. 
// As an example, if you have a variable called MissionOver, and the tree shouldn't tick if MissionOver is True, then you might do
// tick_prerequisite { (not, MissionOver) } end_tick_prerequisite
// but we won't include a prereq here.
//next up are specifications. We'll include several of each type.
specifications {
	INVARSPEC { (not, (equal, varA 0, 'unknown')) } end_INVARSPEC //this specification says that at the start of each tick, varA is not equal to 'unknown' (this is false)
	INVARSPEC { (not, (equal, varA 2, 'unknown')) } end_INVARSPEC //this specification says that after 2 updates (so once inputNode finishes), varA is not equal to 'unknown' (this is false, because inputNode might fail to update varA)
	INVARSPEC { (or, varB -1, (not, varB -1)) } end_INVARSPEC //this specification says that at the end of each tick, varB is true or false (true...obviously).
	CTLSPEC { (exists_finally, varB 0) } end_CTLSPEC //this says that there exists a path where varB is eventually true (this is true)
	CTLSPEC { (always_finally, varB 0) } end_CTLSPEC //this says that on every path, varB is eventually true (this is false)
	LTLSPEC { (globally, (or, (not, varB 0), (not, (active, taskNode)))) } end_LTLSPEC //this says globally, at the start varB is False or taskNode is not active (this is true)
	LTLSPEC { (globally, (or, (not, varB 0), ((active, taskNode)))) } end_LTLSPEC //this says globally, at the start varB is False or taskNode not active (this is false)
} end_specifications
```

This exaqmple file can also be found at ./examples/guided_BT/guided_BT.bt, so you don't need to copy it from here.
