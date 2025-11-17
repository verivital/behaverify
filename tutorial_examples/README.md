#### Overview

Hello! Thank you for taking an interest in BehaVerify. This tutorial is meant to help you learn how to make models for BehaVerify. For instructions on actually running BehaVerify, please see the main [README](https://github.com/verivital/behaverify/tree/main).

1. If you are unfamiliar with behavior trees, please read [Behavior Tree Introduction](#behavior-tree-introduction) to get a basic overview of behavior trees.
2. Go to the [line\_drone.tree](https://github.com/verivital/behaverify/blob/main/tutorial_examples/line_drone.tree) example. This example is fully commented. Please read through it. In several places, you will encounter the string FILL-HERE. This indicates that a portion has intentionally left blank for you to fill in. A completed version of this example can be found at [line\_drone\_ans.tree](https://github.com/verivital/behaverify/blob/main/tutorial_examples/line_drone_ans.tree).


## Contents

- [Overview](#overview) is a brief explanation of this document
- [Abbreviations and definitions](#abbreviation-and-definitions) contains various abbreviations and definitions used throughout this readme.
- [Behavior Tree Introduction](#behavior-tree-introduction) is a brief introduction for behavior trees.
- [Syntax](#syntax-of-behaverify) contains information about functions and other features of BehaVerify.

### Abbreviations and Definitions


- active : a node that is currently executing. At most one node is active at a time.
- tick : An overloaded word. We will use this to mean the external signal that starts the execution of the tree (e.g., when the tick arrives). We will also use it to mean the entire episode of a tree executing. That is to say, a tick (episode) starts when the tick (signal) arrives and ends when the root returns.
- BT : Behavior Tree
- composite : a node with two or more children. One of parallel, selector, or sequence. Used to control which nodes are activated in the tree.
- decorator : a node with exactly one child. Used to modify the behavior of a child without reimplementing.
- leaf : a node with no children. Either an action or a check.
- action : a generalized leaf node. Can return S, F, or R. Can modify variables.
- check : a specialized leaf node. It checks if a condition holds. If it does, it returns S. Otherwise, it returns F.
- parallel : Composite node. Exact behavior depends on implementation. PyTrees version does not support true parallelism. Instead, simply executes each child from left to right. Once all children have been executed, returns a status based on a policy.
- selector : Composite node. Executes children from left to right. If any child returns success, the selector returns success. If a child returns running, the selector returns running. If a child returns failure, the selector continues to the next child. If all children return failure, the selector returns failure.
- sequence : Composite node. Executes children from left to right. If any child returns failure, the sequence returns failure. If a child returns running, the sequence returns running. If a child returns success, the sequence continues to the next child. If all children return success, the sequence returns success. 
- S : short for success, a status a node can return.
- R : short for running, a status a node can return.
- F : short for failure, a status a node can return.
- I : short for invalid, the status of a node before it returns.



# Behavior Tree Introduction

A behavior tree (BT) is a rooted tree structure used for decision-making and control flow in autonomous systems, robotics, and game AI. It provides a modular and hierarchical approach to defining complex behaviors by composing simple, reusable components. The tree executes from the root downward, with each node representing either a decision point (composite/decorator) or an action/condition (leaf). Unlike traditional finite state machines, behavior trees offer better scalability, readability, and easier modification of complex behaviors.

For our purposes, a leaf node is a node with no children, a decorator is a node with exactly 1 child, and composite nodes are nodes with 2 or more children. The leaf nodes of a BT are used to check conditions or to do actions, while the composite nodes control which leaf nodes are executed. For now, at least, we will ignore decorator nodes.

The BT does nothing until it receives an external signal, called a tick. When the tick arrives, the root becomes active (starts executing). In general, traversal through the tree follows a depth first traversal pattern, though composite nodes can 'terminate early' without exploring each child. There are also cases where nodes can be skipped, but we need not worry about that yet. Below we find descriptions of how each node works.

### Node Statuses

Each node in a behavior tree can return one of four statuses during execution:

- **Success (S)**: The node has completed its task successfully. For a check node, this means the condition evaluated to true. For an action node, this means the action was performed successfully. For composite nodes, the meaning depends on the specific type (see below).

- **Running (R)**: The node is still executing and has not yet completed. This status is used for actions that take multiple ticks to complete (e.g., moving to a location, waiting for a sensor reading). When a node returns Running, the tree execution pauses at that node, and on the next tick, execution resumes from that same node.

- **Failure (F)**: The node has failed to complete its task. For a check node, this means the condition evaluated to false. For an action node, this means the action could not be performed. For composite nodes, the meaning depends on the specific type (see below).

- **Invalid (I)**: The initial status of a node before it has been executed or returned a value. This status indicates the node has not yet begun execution in the current tick.

The status values propagate up the tree according to the semantics of each composite node type, allowing complex behaviors to be built from simple components.

### Selector

These nodes will execute their children in a left to right order, one at a time. When the first child completes, the child will return one of success, running, or failure (S, R, F). If the child returns S, then the selector has 'selected' a working child, and it returns S. If the child returns R, then the selector returns R. If the child returns F, the selectors continues to search for a child that will return S, and executes the next child.

Thus, a selector node (also known as a fallback node), 'selects' a child or 'falls back' in the case of failure.

### Sequence

These nodes will execute their children in a left to right order, one at a time. When the first child completes, the child will return one of success, running, or failure (S, R, F). If the child returns F, then the sequence has failed and returns F. If the child returns R, then the sequence returns R. If the child returns S, the sequence continues and executes the next child.

Thus, a sequence node executes children in sequence until a failure occurs.

### Action

An action node is a user defined custom leaf node that does something (such as changing the value of a variable).

### Check

A check node is a user defined custom leaf node that checks a condition.


# Syntax of BehaVerify

## code vs meta\_code
In various places we will make a distinction between code and meta\_code. meta\_code is essentially code that the compiler can fully compute at compile time. E.G. (add, 1, 3) is valid meta\_code, but (add, 1, var45) is not (assuming that var45 is some variable). loop variables can be used in meta\_code (see loop description below). (Note: sometimes you can use meta\_code but not code. However, you can always use meta\_code instead of code).

## Code
At various points, you will need to specify values. In these cases, we utilize code statements, which generally look as follows
```
CONSTANT | VARIABLE | (func, val1, val2, ... valk)
```
each val can be another code statement, so nesting is possible. You may always include more parentheses. Below we provide a list of functions that can be used and the requirements.

1. **CTL ONLY FUNCTIONS:** `exists_globally`, `exists_next`, `exists_finally`, `exists_until`, `always_globally`, `always_next`, `always_finally`, `always_until` - These are Computational Tree Logic operators used only in CTLSPEC specifications for expressing branching-time properties.
2. **LTL ONLY FUNCTIONS:** `next`, `globally`, `finally`, `until`, `release`, `previous`, `not_previous_not`, `historically`, `once`, `since`, `triggered` - These are Linear Temporal Logic operators used only in LTLSPEC specifications for expressing linear-time properties.
3. **BOUNDED TEMPORAL FUNCTIONS:** `globally_bounded`, `finally_bounded`, `until_bounded`, `release_bounded`, `historically_bounded`, `once_bounded`, `since_bounded`, `triggered_bounded` - These are bounded temporal operators that accept a time bound `[lower, upper]` to constrain the temporal property to a specific time window.
4. **STATUS FUNCTIONS (specifications only):** `active`, `success`, `running`, `failure` - These functions query the status of a specific node and are used only in specifications. Syntax: `(status_function, node_name)`. Example: `(success, my_action_node)` checks if `my_action_node` returned success.
5. **Boolean functions that can take LTL/CTL specifications as arguments:** `not`, `and`, `or`, `xor`, `xnor`, `implies`, `equivalent` - These logical operators can be used with temporal logic formulas.
6. **Comparisons:** `eq`, `neq`, `lte`, `gte`, `lt`, `gt` - Comparison operators (detailed below).
7. **Arithmetic:** `abs`, `max`, `min`, `neg`, `add`, `sub`, `mult`, `idiv`, `mod`, `rdiv` - Arithmetic operators (detailed below).
8. **Misc:** `if`, `count`, `loop`, `case_loop`, `index` - Utility functions (detailed below).
9. **Functions that don't work well in nuXmv:** `sin`, `cos`, `exp`, `tan`, `ln`, `floor` - These transcendental and floating-point functions are not well-supported by SMV-based model checkers. Use them only when generating Python/Haskell/C++ code.

### loop
```
(loop, LOOP_VAR, DOMAIN such_that DOMAIN_CONDITION, code)
```
- LOOP_VAR -> name of the loop variable (this must not be a variable declared in the variables section). This variable will only be available inside the loop. The loop variable will go through each value in the DOMAIN that satisfies the DOMAIN_CONDITION
- DOMAIN -> this can be either [min_val, max_val] or {val1, val2, ...}. Each of min_val, max_val, val1, val2, ... is meta\_code (see below). The meta\_code for min_val and max_val must resolve to integers, and min_val must be less than or equal to max_val. Each of val1, val2, ... must be of the same type. You may optionally use reverse DOMAIN to reverse the order (e.g. reverse [1, 10] will result in the evaluation order being 10, 9, 8, ..., 1 instead of 1, 2, 3, ... 10.
- DOMAIN_CONDITION -> meta\_code condition that must resolve to a boolean. Can utilize the loop variable. If for a given value of loop variable the condition is true, that value is used. If the condition is false, the value is not used (e.g., [0, 10] such_that (eq, (mod, loop_var, 2), 0) will result in only even numbers being used).
- code -> this is code.
### Loop EXAMPLES
```
(add, (loop, my_loop, [0, 10] such_that (eq, (mod, my_loop, 2), 0), my_loop))
```
The loop will produce [0, 2, 4, 6, 8, 10]. This will then be treated as inputs to add.
```
result {(loop, a_loop, {'a', 'b', 'c'} such_that True, a_loop)}
```
The loop will produce ['a', 'b', 'c']. This will be treated as possible values. (note: if you actually wanted this you could simply write result{'a', 'b', 'c'}).

In essence, the output of the loop will always be 'flattened'. Loops can thus be nested. E.g.
```
result {(loop, loop1, [0, 10] such_that True, (loop, loop2, [(add, 1, loop1), 10] such_that True, (mult, loop1, loop2)))}
```
I won't write out everything this produces, as that would take quite some time, but you could think of it using the following python code
```
result = []
for loop1 in range(0, 10 + 1): # + 1 because python range doesn't include the final value, but the BehaVerify language does.
	for loop2 in range(loop1 + 1, 10 + 1):
		result.append(loop1 * loop2)
```
Note that duplicate values in result are acceptable, but do not 'do' anything (at least in terms of nuXmv). They may affect the probability that a constant is chosen in generated code though.

Finally, note that it is perfectly legal to include that `(add, 1, loop1)` statement in the domain. This is because while loop1 is a variable, it is a loop\_variable. It will not appear in nuXmv. Rather, the compiler will unravel the loop, using each possibly value for the loop, and then place the result of that in nuXmv.
### case\_loop
```
(case_loop, LOOP_VAR, DOMAIN such_that DOMAIN_CONDITION, condition, code, default_code)
```
refer to loop for details on everything except condition, code, and default_code.
As with the loop, this will iterate through the possible values. However, instead of compiling all of the values, it will instead select the first value that meets the condition, and use that. If no value meets the condition, the default_code value will be used. The condition does not need to be meta code!
### case\_loop EXAMPLES
```
(add, 1, (case_loop, my_loop, reverse [0, 10] such_that (eq, (mod, my_loop, 2), 0), (lt, my_loop, some_var), my_loop, 5))
```
This is basically equivalent to the following python code
```
temp_val = 5
for my_loop in filter(lambda x: x % 2 == 0, reversed(range(0, 10 + 1))):
    if my_loop <= some_var:
		temp_val = my_loop
        break
```
`temp_val + 1` is then used for something.
### index
```
(index, TO_INDEX, INDEX_VAL)
```
- TO_INDEX -> this must resolve to an array variable (usually done by just specifying the variable. However, you can use meta\_code. E.G, if you created a constant called mode_config = True (or mode_config = False), you could use (if, mode_config, array1, array2) to swap which array is indexed using the config constant).
- INDEX_VAL -> this must resolve to an integer. If you write this using meta\_code, you may add the tag constant_index. This will allow various optimizations to be implemented.
### index EXAMPLES
```
(add, (loop, loop_var, [0, 10] such_that True, (index, array_var, constant_index loop_var)))
```
this will add the values of `array_var[0] + ... array_var[10]`. Because loop\_var is a loop\_variable, it is acceptable as meta\_code, and therefore we can use constant\_index to more efficiently index into the array (very relevant for nuXmv).
```
result { (index, array_var, (add, var1, var2))}
```
here we are using `array_var[var1 + var2]` for something. Since var1 and var2 are not loop variables, this is not meta\_code, so we cannot use the constant\_index optimization.
### MISC EXAMPLES
- not
```
(not, code)
```
Boolean negation. Code must resolve to boolean. Code must resolve to exactly 1 boolean (you can use a loop but it can't produce more than 1 value).

---
- and
```
(and, code1, code2, ...)
```
Boolean conjunction. Each code statement must resolve to one or more booleans (e.g., by using a loop you can produce multiple booleans using a single code statement). There must always be at least 2 values produced (though this can be done using a single loop).

---
- or
```
(or, code1, code2, ...)
```
Boolean disjunction. Each code statement must resolve to one or more booleans (e.g., by using a loop you can produce multiple booleans using a single code statement). There must always be at least 2 values produced (though this can be done using a single loop).

---
- xor
```
(xor, code1, ...)
```
Boolean exclusive or. Code must resolve to boolean. You can provide as many code statements as you like (minimum of 1), but they must resolve to exactly 2 booleans.

---
- xnor
```
(xnor, code1, ...)
```
Boolean exclusive nor. Code must resolve to boolean. You can provide as many code statements as you like (minimum of 1), but they must resolve to exactly 2 booleans.

---
- implies
```
(implies, code1, code2, ...)
```
Boolean implication (code1 → code2 → ...). Each code statement must resolve to exactly one boolean. Requires at least 2 boolean values. Equivalent to `(or, (not, code1), code2)` for two arguments. With multiple arguments, chains implications left to right.

---
- equivalent
```
(equivalent, code1, code2, ...)
```
Boolean equivalence (code1 ↔ code2 ↔ ...). Each code statement must resolve to exactly one boolean. Requires at least 2 boolean values. Returns true if all values are the same (all true or all false).

---
- if
```
(if, condition, true_value, false_value)
```
Conditional expression (ternary operator). The condition must resolve to a single boolean. If the condition is true, returns true_value; otherwise returns false_value. The true_value and false_value can be of any type but must be compatible. Example: `(if, (lt, x, 0), -1, 1)` returns -1 if x is negative, otherwise 1.

---
- abs
```
(abs, code)
```
Absolute value. Code must resolve to a single numeric value (integer or real). Returns the absolute value of the number. Example: `(abs, -5)` returns 5.

---
- max
```
(max, code1, code2, ...)
```
Maximum value. Each code statement must resolve to one or more numeric values. Requires at least 2 values total. Returns the maximum value among all provided values. Example: `(max, 3, 7, 2)` returns 7.

---
- min
```
(min, code1, code2, ...)
```
Minimum value. Each code statement must resolve to one or more numeric values. Requires at least 2 values total. Returns the minimum value among all provided values. Example: `(min, 3, 7, 2)` returns 2.

---
- sin
```
(sin, code)
```
Sine function. Code must resolve to a single numeric value (angle in radians). Returns the sine of the value. **Note:** This function does not work well in nuXmv models. Use primarily for Python/Haskell/C++ generation.

---
- cos
```
(cos, code)
```
Cosine function. Code must resolve to a single numeric value (angle in radians). Returns the cosine of the value. **Note:** This function does not work well in nuXmv models. Use primarily for Python/Haskell/C++ generation.

---
- exp
```
(exp, code)
```
Exponential function (e^x). Code must resolve to a single numeric value. Returns e raised to the power of the value. **Note:** This function does not work well in nuXmv models. Use primarily for Python/Haskell/C++ generation.

---
- tan
```
(tan, code)
```
Tangent function. Code must resolve to a single numeric value (angle in radians). Returns the tangent of the value. **Note:** This function does not work well in nuXmv models. Use primarily for Python/Haskell/C++ generation.

---
- ln
```
(ln, code)
```
Natural logarithm. Code must resolve to a single positive numeric value. Returns the natural logarithm (base e) of the value. **Note:** This function does not work well in nuXmv models. Use primarily for Python/Haskell/C++ generation.

---
- eq
```
(eq, code1, code2)
```
Equality comparison. Each code statement must resolve to exactly one value of compatible types. Returns true if code1 equals code2, false otherwise. Example: `(eq, x, 5)` returns true if x equals 5.

---
- neq
```
(neq, code1, code2)
```
Inequality comparison. Each code statement must resolve to exactly one value of compatible types. Returns true if code1 does not equal code2, false otherwise. Example: `(neq, x, 5)` returns true if x is not equal to 5.

---
- lte
```
(lte, code1, code2)
```
Less than or equal comparison. Each code statement must resolve to exactly one numeric value. Returns true if code1 is less than or equal to code2. Example: `(lte, x, 10)` returns true if x ≤ 10.

---
- gte
```
(gte, code1, code2)
```
Greater than or equal comparison. Each code statement must resolve to exactly one numeric value. Returns true if code1 is greater than or equal to code2. Example: `(gte, x, 0)` returns true if x ≥ 0.

---
- lt
```
(lt, code1, code2)
```
Less than comparison. Each code statement must resolve to exactly one numeric value. Returns true if code1 is strictly less than code2. Example: `(lt, x, 10)` returns true if x < 10.

---
- gt
```
(gt, code1, code2)
```
Greater than comparison. Each code statement must resolve to exactly one numeric value. Returns true if code1 is strictly greater than code2. Example: `(gt, x, 0)` returns true if x > 0.

---
- neg
```
(neg, code)
```
Negation (arithmetic negative). Code must resolve to a single numeric value. Returns the negative of the value. Example: `(neg, 5)` returns -5, and `(neg, -3)` returns 3.

---
- add
```
(add, code1, code2, ...)
```
Addition. Each code statement must resolve to one or more numeric values. Requires at least 2 values total. Returns the sum of all values. Example: `(add, 1, 2, 3)` returns 6.

---
- sub
```
(sub, code1, code2)
```
Subtraction. Each code statement must resolve to exactly one numeric value. Returns code1 minus code2. Example: `(sub, 10, 3)` returns 7.

---
- mult
```
(mult, code1, code2, ...)
```
Multiplication. Each code statement must resolve to one or more numeric values. Requires at least 2 values total. Returns the product of all values. Example: `(mult, 2, 3, 4)` returns 24.

---
- idiv
```
(idiv, code1, code2)
```
Integer division. Each code statement must resolve to exactly one integer value. Returns the integer quotient of code1 divided by code2 (truncated toward zero). Example: `(idiv, 7, 2)` returns 3.

---
- mod
```
(mod, code1, code2)
```
Modulo (remainder). Each code statement must resolve to exactly one integer value. Returns the remainder when code1 is divided by code2. Example: `(mod, 7, 3)` returns 1.

---
- rdiv
```
(rdiv, code1, code2)
```
Real division. Each code statement must resolve to exactly one numeric value. Returns the real (floating-point) quotient of code1 divided by code2. Example: `(rdiv, 7, 2)` returns 3.5.

---
- floor
```
(floor, code)
```
Floor function. Code must resolve to a single numeric value. Returns the largest integer less than or equal to the value. Example: `(floor, 3.7)` returns 3, `(floor, -2.3)` returns -3. **Note:** This function does not work well in nuXmv models.

---
- count
```
(count, condition, code1, code2, ...)
```
Count function. The condition is a boolean expression that can reference a special variable within the count context. Counts how many of the provided code values satisfy the condition. Returns an integer count. This is an advanced function - consult examples for proper usage.

---

## meta\_code:
meta\_code is structured identically to code, but must be capable of being evaluated during compilation. As such, meta\_code cannot rely on variables, but can rely on constants. meta\_code is used in loops (which are unrolled by the compiler) and in other places that must be computed at compile time (e.g., the size of an array).
