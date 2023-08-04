
(regexp-opt '("MODULE") t)

"\\(MODULE\\)"

;;"\\(actions\\|c\\(?:\\(?:heck\\|onstant\\)s\\)\\|en\\(?:d_\\(?:actions\\|c\\(?:\\(?:heck\\|onstant\\)s\\)\\|environment_\\(?:checks\\|update\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)"

;; END OF 1
;; font-lock-preprocessor-face

(regexp-opt '("CONSTANTS" "DEFINE" "VAR" "IVAR" "FROZENVAR" "FUN") t)

"\\(CONSTANTS\\|DEFINE\\|F\\(?:ROZENVAR\\|UN\\)\\|I?VAR\\)"

;; END OF 2
;; font-lock-variable-name-face

(regexp-opt '("integer" "real" "boolean" "array" "unsigned word" "signed word" "clock") t)

"\\(array\\|boolean\\|clock\\|integer\\|real\\|\\(?:un\\)?signed word\\)"

;; END OF 3
;; font-lock-type-face

(regexp-opt '("pi" "abs" "max" "min" "sin" "cos" "exp" "tan" "ln" "!" "&" "|" "xor" "xnor" "->" "<->" "=" "!=" ">" "<" "<=" ">=" "-" "+" "*" "/" "mod" ">>" "<<" "word1" "bool" "toint" "count" "swcost" "uwconst" "signed" "unsigned" "sizeof" "floor" "extend" "resize" "union" "in" "?" "READ" "WRITE" "CONSTARRAY" "typeof" "EG" "EX" "EF" "AG" "AX" "AF" "U" "X" "G" "F" "V" "Y" "Z" "H" "O" "S" "T") t)

"\\(!=\\|->\\|<\\(?:->\\|[<=]\\)\\|>[=>]\\|A[FGX]\\|CONSTARRAY\\|E[FGX]\\|READ\\|WRITE\\|abs\\|bool\\|co\\(?:s\\|unt\\)\\|ex\\(?:p\\|tend\\)\\|floor\\|in\\|ln\\|m\\(?:ax\\|in\\|od\\)\\|pi\\|resize\\|s\\(?:i\\(?:gned\\|n\\|zeof\\)\\|wcost\\)\\|t\\(?:an\\|oint\\|ypeof\\)\\|u\\(?:n\\(?:ion\\|signed\\)\\|wconst\\)\\|word1\\|x\\(?:n?or\\)\\|[!&*+/<-?FGHOS-VXYZ|-]\\)"

;;"\\(BOOLEAN\\|VAR\\|bl\\|en\\(?:d_\\(?:initial_values\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)\\|v\\)\\|initial_values\\|local\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)"

;; END OF 4
;; font-lock-function-name-face

(regexp-opt '("ASSIGN" "TRANS" "INIT" "FAIRNESS" "JUSTICE" "COMPASSION" "INVAR" "next" "init" "case" "esac") t)

"\\(ASSIGN\\|COMPASSION\\|FAIRNESS\\|IN\\(?:IT\\|VAR\\)\\|JUSTICE\\|TRANS\\|case\\|esac\\|\\(?:ini\\|nex\\)t\\)"

;; END OF 5
;; font-lock-keyword-face

(regexp-opt '("LTLSPEC" "CTLSPEC" "SPEC" "INVARSPEC" ) t)

"\\(\\(?:CTL\\|INVAR\\|LTL\\)?SPEC\\)"

;; END OF 6
;; font-lock-builtin-face

(regexp-opt '("TRUE" "FALSE") t)

"\\(\\(?:FALS\\|TRU\\)E\\)"

;;"\\(False\\|True\\|failure\\|runnning\\|success\\)"

;; END OF 7
;; font-lock-constant-face


(regexp-opt '("CONSTANTS" "DEFINE" "VAR" "IVAR" "FROZENVAR" "FUN" "ASSIGN" "TRANS" "INIT" "FAIRNESS" "JUSTICE" "COMPASSION" "INVAR") t)



