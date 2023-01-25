# Instructions for creating a .bt file for use with btree.tx

This file will not currently contain all relevant information. Specifically it will omit anything that deals solely with code generation. This file will therefore focus on the modeling side.

## Variables

All variables that will be used in the model must be declared in the appropriate section. A variable must be of the following format

'var' type=[Type] name=ID ('=' default=DefaultBBType)? (',' 'model_as' '(' model = ModelOptions (',' initial_value = Enumeration)? ')')? ';'

Thus an example would be

var bool example = False , model_as(bool, False);

Note that in the above example, the type and model are both bool. Similarly, the default and initial value are both False. This need not be the case. For instance

var String example2 = 'potato', model_as([0,3], 2);

is completely acceptable, though perhaps not productive for the goals of accurately modeling. Below we explain using example2 what each part means

- type : type defines what type the variable is IN CODE GENERATION. This has no effect on the model. This paramater is required.

- name : the name of the variable. This is used in the model and in code generation. This paramater is required.

- default : the default value (if any) to be used IN CODE GENERATION. This has no effect on the model. This paramter is optional.

These first three values are what is used by code generation. Of the three, only name matters for modeling. Note then that it is possible to declare a variable as follows

var Float32 example3;

Because exampl3 dose NOT have a model_as statement, it will not be modeled. example3 would only be used in code generation. Continuing with the explanation.

- model : model defines what type the variable is in the model. This has no effect on code generation, it is only used in the model. If the variable is to be modeled, this paramater is required.

- initial_value : initial_value defines what value the variable should initially have in the model. This has no effect on code generation, it is only used in the model. This paramater is optional.

Thus the model information from example2 would be as follows: name is example2, model is [0, 3], initial value is 2. 

### ModelOptions

ModelOptions describes what domains can be used to model a variable. ModelOptions must be of the following format

(is_bool = 'bool') | ('{' enums += EnumerationDec[','] '}') | ( '[' range_minimum = INT ',' range_maximum = INT ']')

Thus the three modes, so to speak, would be: bool, {enum1, enum2, ..., enumK}, [minVal, maxVal]. Note that an enum could be an int or a string. Thus {0, 'potato', 3, 'tomato'} is a valid set of enumerations. However, {'1.3', True, 'TRUE'} would all fail, if not here, then when the .smv file is ran. '1.3' would fail because it would end up being represented as 1.3 in .smv, and nuXmv does not allow floats in enumerations. True and 'TRUE' would fail because nuXmv places restrictions on booleans appear inside enumerations. However {'True', '3'} would be acceptable.


## Nodes

Once all variables are declared, we will need to be able to use them. Variables are used within Nodes. The main way to use variables in Nodes is through a set() declaration. A Node can have any number of set declarations, but they must be placed in the appropriate section. The order of set declarations matters: they will be executed in the order they are presented.


### set declaration

A set declaration defines how the variable should be updated when the node runs. set declarations must be of the following format

'set' '(' variable = [BBVar] ',' updates *= UpdateStatement default_update = CodeStatement')'

Thus two examples would be

set(example, True)

set(example2, try((not, example), (addition, example2, 1)), (any, 0, (subtraction, example2, 1)))

The first example sets the variable example to be True. The second example sets the variable example2 to be example2 + 1 if example is False, else it picks non-deterministically form 0 and example-1. In python code, this is equivalent to the following

if not example: example2 = example2 + 1

else: example2 = random.choice([0, example2 - 1])

Note that you can have any number of try statements, including 0. Furthermore, note that if a node had both of our examples as set declarations, it would be the same as the following python code segment

example = True

if not example: example2 = example2 + 1

else: example2 = random.choice([0, example2 - 1])

Let us now more specifically disect example2. it consists of 3 parts

- variable : this informs us which variable is being updated. In this case it's example2

- updates : these are the statements to try. The first update that succeeds will be applied. Update statements are described in more detail below

- defualt_update : this is the value to use if none of the updates applied. This is a CodeStatement. CodeStatements are described in more detail below.

### Update Statement

An update statement is a pair (condition, update_value). If the condition is True, then the update_value is used. Update Statements must be of the following format

'try(' condition = CodeStatement ',' update_value = CodeStatement ')' ','

Note that the comma at the end is to ensure each entry in the set declaration is comma separated, for asthetic reasons. Unfortunately, there was no easier way to handle this.

CodeStatement is described in more detail below. However, note that a CodeStatement need not resolve to a True or False according to the grammar. It is up to the user to ensure that the condition is actually something that can resolve to True or False (e.g, 'potato' is a valid CodeStatement, but would not function as a condition. However, type checking this is not currently enabled).

### CodeStatement

A CodeStatement is of the following format:

(constant = STRICTFLOAT) | (constant = INT) | (constant = BOOL) | (constant = STRING) | (variable = [BBVar]) | ('(' function_call = function ')') | ('(' CodeStatement = CodeStatement ')')

Intuitively, this means your code statement can be

1. a constant (float, int, bool, or string)

2. a variable. Note that the variable itself must be declared in the appropriate variable section, as described above. Here you will simple refer to the variable using it's name.

3. a function. all functions are of the form (FUNCTION_NAME, VALUE1, VALUE2, ...). Note that the surrounding () are required. A full list of functions can be found in btree.tx

4. a CodeStatement surrounded by (). I.E, you don't need to worry about adding in too many paranthesis. 


## Input Nodes

Input Nodes are a specific type of node. In general, it is assumed that an input node is monitoring some topic. If new data came in, then it will update a variable and return success, and potentially run some other code in the process. If no new data came in, then it returns running.


