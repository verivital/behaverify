(regexp-opt '("configuration" "end_configuration" "enumerations" "end_enumerations"  "constants" "end_constants" "variables" "end_variables" "environment_update" "end_environment_update" "checks" "end_checks" "environment_checks" "end_environment_checks" "actions" "end_actions" "sub_trees" "end_sub_trees" "tree" "end_tree" "tick_prerequisite" "end_tick_prerequisite" "specifications" "end_specifications") t)

"\\(actions\\|c\\(?:hecks\\|on\\(?:figuration\\|stants\\)\\)\\|en\\(?:d_\\(?:actions\\|c\\(?:hecks\\|on\\(?:figuration\\|stants\\)\\)\\|en\\(?:umerations\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)\\|umerations\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)"


;;"\\(actions\\|c\\(?:\\(?:heck\\|onstant\\)s\\)\\|en\\(?:d_\\(?:actions\\|c\\(?:\\(?:heck\\|onstant\\)s\\)\\|environment_\\(?:checks\\|update\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)"

;; END OF 1
;; font-lock-preprocessor-face

(regexp-opt '("composite" "end_composite" "decorator" "end_decorator" "check" "end_check" "action" "end_action" "environment_check" "end_environment_check" "sub_tree" "end_sub_tree" "insert" "end_insert") t)

"\\(action\\|c\\(?:heck\\|omposite\\)\\|decorator\\|en\\(?:d_\\(?:action\\|c\\(?:heck\\|omposite\\)\\|decorator\\|environment_check\\|insert\\|sub_tree\\)\\|vironment_check\\)\\|insert\\|sub_tree\\)"

;; END OF 2
;; font-lock-variable-name-face

(regexp-opt '("parallel" "selector" "sequence" "X_is_Y" "inverter" "arguments" "end_arguments" "read_variables" "end_read_variables" "write_variables" "end_write_variables" "local_variables" "end_local_variables" "policy" "success_on_all" "success_on_one" "with_partial_memory" "with_true_memory" "instant" "constant_index" "range" "per_index" "children" "end_children" "child" "end_child" "X" "Y") t)

"\\(X_is_Y\\|arguments\\|c\\(?:hild\\(?:ren\\)?\\|onstant_index\\)\\|end_\\(?:arguments\\|child\\(?:ren\\)?\\|\\(?:local\\|read\\|write\\)_variables\\)\\|in\\(?:stant\\|verter\\)\\|local_variables\\|p\\(?:arallel\\|er_index\\|olicy\\)\\|r\\(?:ange\\|ead_variables\\)\\|s\\(?:e\\(?:lector\\|quence\\)\\|uccess_on_\\(?:all\\|one\\)\\)\\|w\\(?:ith_\\(?:\\(?:partial\\|true\\)_memory\\)\\|rite_variables\\)\\|[XY]\\)"

;; END OF 3
;; font-lock-type-face

(regexp-opt '("variable" "end_variable" "variable_statement" "end_variable_statement" "initial_values" "end_initial_values" "update" "end_update" "write_environment" "end_write_environment" "read_environment" "end_read_environment" "return_statement" "end_return_statement" "bl" "env" "local" "array" "VAR" "FROZENVAR" "DEFINE" "BOOLEAN" "INT" "ENUM") t)

"\\(BOOLEAN\\|DEFINE\\|ENUM\\|FROZENVAR\\|INT\\|VAR\\|array\\|bl\\|en\\(?:d_\\(?:initial_values\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)\\|v\\)\\|initial_values\\|local\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)"

;;"\\(BOOLEAN\\|VAR\\|bl\\|en\\(?:d_\\(?:initial_values\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)\\|v\\)\\|initial_values\\|local\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)"

;; END OF 4
;; font-lock-function-name-face

(regexp-opt '("assign" "end_assign" "index_of" "end_index_of" "case" "end_case" "result" "end_result" "condition" "end_condition" "LTLSPEC" "end_LTLSPEC" "CTLSPEC" "end_CTLSPEC" "INVARSPEC" "end_INVARSPEC") t)

"\\(CTLSPEC\\|INVARSPEC\\|LTLSPEC\\|assign\\|c\\(?:ase\\|ondition\\)\\|end_\\(?:CTLSPEC\\|INVARSPEC\\|LTLSPEC\\|assign\\|c\\(?:ase\\|ondition\\)\\|index_of\\|result\\)\\|index_of\\|result\\)"

;; END OF 5
;; font-lock-keyword-face

(regexp-opt '("abs" "max" "min" "sin" "cos" "exp" "tan" "ln" "eq" "neq" "lt" "gt" "lte" "gte" "neg" "add" "sub" "mult" "idiv" "rdiv" "floor" "mod" "count" "index" "not" "and" "or" "xor" "xnor" "implies" "equivalent" "active" "success" "running" "failure" "next" "globally" "globally_bounded" "finally" "finally_bounded" "until" "until_bounded" "release" "release_bounded" "previous" "not_previous_not" "historically" "historically_bounded" "once" "once_bounded" "since" "since_bounded" "triggered" "triggered_bounded" "exists_globally" "exists_next" "exists_finally" "exists_until" "always_globally" "always_next" "always_finally" "always_until") t)

"\\(a\\(?:bs\\|ctive\\|dd\\|lways_\\(?:finally\\|globally\\|next\\|until\\)\\|nd\\)\\|co\\(?:s\\|unt\\)\\|e\\(?:q\\(?:uivalent\\)?\\|x\\(?:ists_\\(?:finally\\|globally\\|next\\|until\\)\\|p\\)\\)\\|f\\(?:ailure\\|inally\\(?:_bounded\\)?\\|loor\\)\\|g\\(?:lobally\\(?:_bounded\\)?\\|te?\\)\\|historically\\(?:_bounded\\)?\\|i\\(?:div\\|mplies\\|ndex\\)\\|l\\(?:te\\|[nt]\\)\\|m\\(?:ax\\|in\\|od\\|ult\\)\\|n\\(?:e\\(?:xt\\|[gq]\\)\\|ot\\(?:_previous_not\\)?\\)\\|o\\(?:nce\\(?:_bounded\\)?\\|r\\)\\|previous\\|r\\(?:div\\|elease\\(?:_bounded\\)?\\|unning\\)\\|s\\(?:in\\(?:ce\\(?:_bounded\\)?\\)?\\|u\\(?:b\\|ccess\\)\\)\\|t\\(?:an\\|riggered\\(?:_bounded\\)?\\)\\|until\\(?:_bounded\\)?\\|x\\(?:n?or\\)\\)"

;; END OF 6
;; font-lock-builtin-face

(regexp-opt '("hypersafety" "use_reals" "True" "False" "success" "runnning" "failure") t)

"\\(False\\|True\\|failure\\|hypersafety\\|runnning\\|\\(?:succes\\|use_real\\)s\\)"

;;"\\(False\\|True\\|failure\\|runnning\\|success\\)"

;; END OF 7
;; font-lock-constant-face
