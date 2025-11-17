# BehaVerify TODO List

This document catalogs all TODOs, FIXMEs, and planned improvements found throughout the BehaVerify codebase.

**Last Updated:** 2025-11-17

---

## Table of Contents

1. [Documentation TODOs](#documentation-todos) - ✅ COMPLETED
2. [Core Functionality TODOs](#core-functionality-todos)
3. [Code Generation TODOs](#code-generation-todos)
4. [Optimization TODOs](#optimization-todos)
5. [Monitor TODOs](#monitor-todos)
6. [Validation & Type Checking TODOs](#validation--type-checking-todos)
7. [Example & Tutorial TODOs](#example--tutorial-todos)
8. [Low Priority / Unused Variations](#low-priority--unused-variations)

---

## Documentation TODOs

### ✅ COMPLETED - Tutorial Documentation
**Status:** RESOLVED (2025-11-17)

- ~~`tutorial_examples/README.md:39` - Fill in behavior tree introduction~~ ✅
- ~~`tutorial_examples/README.md:47` - Fill in node statuses explanation~~ ✅

**Resolution:** Added comprehensive explanations for:
- What behavior trees are and their purpose
- Detailed explanation of all four node statuses (Success, Running, Failure, Invalid)

---

## Core Functionality TODOs

### High Priority

#### Grammar Validation & Type Checking (`src/behaverify/check_grammar.py`)

**Lines 40-47:**
```python
# TODO : function category (TL/INVAR/reg) - DONE?
# TODO : node_types (idk what this means)
# TODO : instant declarations
# TODO : array updates
# TODO : read at/node_name in functions
# TODO : confirm enumerations are being enforced
# todo : make sure loop variables don't conflict
# todo : make sure define variables are deterministicly updated.
```
**Priority:** HIGH
**Impact:** Core validation functionality
**Status:** Pending investigation - some may already be done

**Line 168:**
```python
# TODO: add a check here which confirms that the node actually uses the local variable.
```
**Priority:** MEDIUM
**Impact:** Improves validation accuracy

**Line 171:**
```python
# TODO: double check, we should make sure we're in a node doing this, and not from invar, and that the node uses the variable
```
**Priority:** MEDIUM
**Impact:** Prevents validation errors

**Line 173:**
```python
# todo: confirm read_at and trace_num are correct.
```
**Priority:** MEDIUM
**Impact:** Temporal logic validation

**Line 210:**
```python
# TODO: think about this.
```
**Priority:** LOW
**Impact:** Needs context investigation

**Line 859:**
```python
# TODO: make sure local variables are always referened with a node identifier here.
```
**Priority:** MEDIUM
**Impact:** Variable scoping correctness

---

#### Node Creator (`src/behaverify/node_creator.py`)

**Line 301:**
```python
# TODO: explain why this doesn't have the root condition.
```
**Priority:** LOW
**Impact:** Documentation/code clarity

---

#### Common Utilities (`src/behaverify/behaverify_common.py`)

**Line 599:**
```python
# TODO: add a check to see if a node can even be run.
```
**Priority:** MEDIUM
**Impact:** Runtime optimization and validation

**Line 923:**
```python
# TODO: update so it hits
```
**Priority:** MEDIUM
**Impact:** Needs context

**Line 966:**
```python
# TODO: update so it hits all decorators that can do this.
```
**Priority:** MEDIUM
**Impact:** Decorator handling completeness
**Context:** Currently only handles running_is decorator, should handle all decorators that can undo running status

---

## Code Generation TODOs

### C++ Code Generation (`src/behaverify/dsl_to_cpp.py`)

#### Critical Issues

**Line 66, 78:**
```python
# TODO: adjust
```
**Priority:** HIGH
**Impact:** C++ generation correctness

**Line 221, 246, 252:**
```python
# TODO: fix this. Going to have to overhaul this.
# TODO: Fix this.  Going to have to overhaul this.
# TODO: Fix this. Going to have to overhaul this.
```
**Priority:** HIGH
**Impact:** Major refactoring needed for C++ generation

**Line 276, 312:**
```python
# TODO: make this actually work in the general case. Right now, we're just assuming that the variable name will be used.
```
**Priority:** HIGH
**Impact:** Variable handling robustness

**Line 289, 290:**
```python
# TODO: as with check_code
# TODO: add longif
```
**Priority:** MEDIUM
**Impact:** Feature completeness

**Line 314:**
```python
# TODO: this doesn't work if a variable is a define or anything like that.
```
**Priority:** HIGH
**Impact:** Define variable support in C++

**Line 344:**
```python
# TODO: Upate this. Not updating this until I confirm things without the environment working.
```
**Priority:** MEDIUM
**Impact:** Environment variable handling

**Line 437:**
```python
# TODO: fix long if
```
**Priority:** MEDIUM
**Impact:** Conditional expression handling

**Line 489:**
```python
# TODO: fix array update
```
**Priority:** HIGH
**Impact:** Array manipulation in C++

**Line 939, 940:**
```python
# TODO: as with action
# TODO: add longif
```
**Priority:** MEDIUM
**Impact:** Feature parity

**Line 962, 964, 965, 966:**
```python
# TODO: make this actually work in the general case. Right now, we're just assuming that the variable name will be used.
# TODO: this doesn't work if a variable is a define or anything like that.
# TODO: currently assuming sync action node.
# TODO: currently doesn't work with local variables.
```
**Priority:** HIGH
**Impact:** Multiple C++ generation limitations that need addressing

**Line 1591:**
```python
# TODO: check if these are actually correct. They might be somewhat off (specifically the library ones)
```
**Priority:** MEDIUM
**Impact:** Library integration verification

---

### nuXmv Code Generation (`src/behaverify/dsl_to_nuxmv.py`)

**Line 2047:**
```python
# todo: fix this so we can include meta functions as the value of repeat.
```
**Priority:** MEDIUM
**Impact:** Feature enhancement for repeat constructs

---

### Python Code Generation (`src/behaverify/dsl_to_python.py`)

**Line 665:**
```python
# todo: consider optimizing this for constant index. No reason to compute everything when we know the index.
```
**Priority:** LOW
**Impact:** Performance optimization (see Optimization section)

---

## Optimization TODOs

### Array Indexing Optimization

**Locations:**
- `src/behaverify/dsl_to_python.py:665`
- `src/behaverify/dsl_to_cpp.py:709`

**Description:** When array index is constant (known at compile time), generate optimized code that directly accesses the specific element instead of computing all elements.

**Priority:** LOW
**Impact:** Performance improvement for array operations
**Benefit:** Reduced runtime overhead, especially for nuXmv verification

**Implementation Notes:**
- Already supports `constant_index` tag in DSL
- Need to implement optimization in code generators
- Most beneficial for nuXmv where state space reduction matters

---

## Monitor TODOs

### DSL Monitor Creation (`src/behaverify/monitor/create_dsl_monitor.py`)

**Line 63:**
```python
# # TODO FINISH THIS
```
**Priority:** MEDIUM
**Impact:** Incomplete monitor generation feature
**Status:** Needs investigation to determine what functionality is missing

---

## Validation & Type Checking TODOs

### Summary of Validation Gaps

The following validation features are noted as potentially missing or incomplete across multiple files:

1. **Function Categories** - Distinguish between temporal logic (TL), invariant (INVAR), and regular functions
2. **Node Types** - Additional validation for node type constraints
3. **Instant Declarations** - Support or validation for instant variable declarations
4. **Array Updates** - Proper validation of array update operations
5. **read_at/node_name in functions** - Validation for temporal and node-specific references
6. **Enumeration Enforcement** - Ensure enumeration type constraints are properly checked
7. **Local Variable Usage** - Verify local variables are actually used by declaring nodes
8. **Loop Variable Conflicts** - Ensure loop variables don't shadow or conflict
9. **Define Variable Determinism** - Ensure define variables are updated deterministically

**Files Affected:**
- `src/behaverify/check_grammar.py` (active codebase)
- `REPRODUCIBILITY/2024_VMCAI/src/check_model.py` (research snapshot)
- Various files in `src/behaverify/variations/unused/` (deprecated)

**Priority:** MEDIUM to HIGH (depending on actual gaps)
**Action Required:** Audit each item to determine if already implemented or still needed

---

## Example & Tutorial TODOs

### Tutorial Example (`examples/tutorial.tree`)

**Line 229:**
```python
# local means local (specific to the nodes that use it). (TODO: These are missing from the tutorial currently).
```
**Priority:** LOW
**Impact:** Tutorial completeness
**Action:** Add local variable examples to tutorial

### ANSR Examples (`examples/ANSR_revised/*/bt.py`)

**Multiple files contain:**
```python
# ToDo: [message definition, etc.]
```
**Priority:** LOW
**Impact:** Example code cleanup
**Files:**
- `examples/ANSR_revised/modified_python/bt.py:259, 274`
- `examples/ANSR_revised/with_cost_graph/bt.py:387, 402`
- `examples/ANSR_revised/without_cost_graph/bt.py:368, 383`

### A* Network Example

**File:** `examples/ANSR_behaverify_A_star_net/a_star_files/template_keep_out.tree:184`
```
#{TODO: NOT DONE }#
```
**Priority:** LOW
**Impact:** Example completion

---

## Low Priority / Unused Variations

### Deprecated Code Variations

The following directories contain historical/experimental code variations that are no longer actively maintained:

- `src/behaverify/variations/unused/s_var/`
- `src/behaverify/variations/unused/depth/`
- `src/behaverify/variations/unused/func/`
- `src/behaverify/variations/unused/norm/`
- `src/behaverify/variations/unused/no_internal/`
- `src/behaverify/variations/unused/aut_s/`
- `src/behaverify/variations/unused/aut/`
- `src/behaverify/variations/unused/basic/old/`

These directories contain numerous TODOs similar to those in the main codebase.

**Priority:** VERY LOW
**Action:** Consider archiving or removing these directories if they are no longer needed
**Impact:** Code maintenance burden

### REPRODUCIBILITY Snapshots

The `REPRODUCIBILITY/` directory contains snapshots of code from various research publications. TODOs in these files are historical and likely should not be modified to maintain reproducibility.

**Files:**
- `REPRODUCIBILITY/2024_VMCAI/src/*.py` (multiple files)
- `REPRODUCIBILITY/2022_SEFM/examples/**/*.py` (multiple files)

**Priority:** VERY LOW (preserve as-is for reproducibility)
**Action:** Do not modify unless explicitly updating reproducibility materials

---

## Recommended Action Plan

### Phase 1: Investigation & Triage (1-2 weeks)

1. **Audit Core Validation TODOs** (`check_grammar.py`)
   - Determine which validation features are actually missing
   - Create issues for confirmed gaps
   - Document which TODOs are already resolved

2. **Assess C++ Generation Status**
   - Determine scope of C++ generation overhaul needed
   - Identify critical vs. nice-to-have fixes
   - Create detailed technical plan

3. **Clean Up Obsolete Code**
   - Decide fate of `variations/unused/` directories
   - Archive or remove if no longer needed
   - Update documentation if keeping

### Phase 2: High Priority Fixes (4-6 weeks)

1. **C++ Generation Critical Fixes**
   - Fix define variable support (line 314, 964)
   - Fix array updates (line 489)
   - Fix general variable handling (lines 276, 312, 962)
   - Add local variable support (line 966)

2. **Core Validation Improvements**
   - Add missing validation checks identified in Phase 1
   - Improve local variable usage validation
   - Enhance loop variable conflict detection

3. **Monitor Completion**
   - Finish incomplete monitor generation feature
   - Add tests for monitor functionality

### Phase 3: Medium Priority Enhancements (6-8 weeks)

1. **Feature Completeness**
   - Add longif support to C++ generation
   - Implement meta functions in repeat constructs (nuXmv)
   - Complete decorator handling improvements

2. **Documentation & Examples**
   - Add local variable tutorial examples
   - Clean up example code TODOs
   - Improve inline code documentation

### Phase 4: Optimizations (ongoing)

1. **Constant Index Optimization**
   - Implement for Python generation
   - Implement for C++ generation
   - Benchmark performance improvements

2. **Node Reachability Analysis**
   - Implement runtime node reachability checking
   - Optimize tree execution based on reachability

---

## Contributing

When working on TODOs from this list:

1. **Create an Issue** - Reference the TODO line number and file
2. **Add Tests** - Include test cases for the fix
3. **Update This File** - Mark TODO as complete or in-progress
4. **Document Changes** - Update relevant documentation

---

## Statistics

- **Total TODOs Found:** ~150+ (including duplicates in variations/)
- **Active Codebase TODOs:** ~40
- **Documentation TODOs:** 2 (COMPLETED ✅)
- **High Priority:** ~15-20
- **Medium Priority:** ~15-20
- **Low Priority:** ~10-15
- **Deprecated/Historical:** ~100+

---

*This TODO list was generated by comprehensive grep analysis of the BehaVerify repository on 2025-11-17.*
