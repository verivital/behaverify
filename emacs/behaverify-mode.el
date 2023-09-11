;;; behaverify-mode-el -- Major mode for editing BehaVerify files

;; Author: Serena Aura Serbinowska
;; Last Edit: 2023-09-11
;; Keywords: BehaVerify major-mode

;;; Commentary:
;;
;; heavily based on this tutorial: https://www.emacswiki.org/emacs/ModeTutorial

;;; Code:
(defvar behaverify-mode-hook nil)
(defvar behaverify-mode-map
  (let ((behaverify-mode-map (make-keymap)))
    (define-key behaverify-mode-map "\C-j" 'newline-and-indent)
    behaverify-mode-map)
  "Keymap for BehaVerify major mode.")

(add-to-list 'auto-mode-alist '("\\.tree\\'" . behaverify-mode))

(defconst behaverify-font-lock-keywords-1
  (list
   '("\\<\\(actions\\|c\\(?:hecks\\|on\\(?:figuration\\|stants\\)\\)\\|en\\(?:d_\\(?:actions\\|c\\(?:hecks\\|on\\(?:figuration\\|stants\\)\\)\\|en\\(?:umerations\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)\\|umerations\\|vironment_\\(?:checks\\|update\\)\\)\\|s\\(?:\\(?:pecification\\|ub_tree\\)s\\)\\|t\\(?:\\(?:ick_prerequisit\\|re\\)e\\)\\|variables\\)\\>" . font-lock-warning-face))
  "Minimal highlighting expressions for BehaVerify mode.")

(defconst behaverify-font-lock-keywords-2
  (append behaverify-font-lock-keywords-1
		  (list
		   '("\\<\\(action\\|c\\(?:heck\\|omposite\\)\\|decorator\\|en\\(?:d_\\(?:action\\|c\\(?:heck\\|omposite\\)\\|decorator\\|environment_check\\|insert\\|sub_tree\\)\\|vironment_check\\)\\|insert\\|sub_tree\\)\\>" . font-lock-variable-name-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defconst behaverify-font-lock-keywords-3
  (append behaverify-font-lock-keywords-2
		  (list
		   '("\\<\\(X_is_Y\\|arguments\\|c\\(?:hild\\(?:ren\\)?\\|onstant_index\\)\\|end_\\(?:arguments\\|child\\(?:ren\\)?\\|\\(?:local\\|read\\|write\\)_variables\\)\\|in\\(?:stant\\|verter\\)\\|local_variables\\|p\\(?:arallel\\|er_index\\|olicy\\)\\|r\\(?:ange\\|ead_variables\\)\\|s\\(?:e\\(?:lector\\|quence\\)\\|uccess_on_\\(?:all\\|one\\)\\)\\|w\\(?:ith_\\(?:\\(?:partial\\|true\\)_memory\\)\\|rite_variables\\)\\|[XY]\\)\\>" . font-lock-type-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defconst behaverify-font-lock-keywords-4
  (append behaverify-font-lock-keywords-3
		  (list
		   '("\\<\\(BOOLEAN\\|DEFINE\\|ENUM\\|FROZENVAR\\|INT\\|VAR\\|bl\\|en\\(?:d_\\(?:initial_values\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)\\|v\\)\\|initial_values\\|local\\|re\\(?:\\(?:ad_environ\\|turn_state\\)ment\\)\\|update\\|variable\\(?:_statement\\)?\\|write_environment\\)\\>" . font-lock-function-name-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defconst behaverify-font-lock-keywords-5
  (append behaverify-font-lock-keywords-4
		  (list
		   '("\\<\\(CTLSPEC\\|INVARSPEC\\|LTLSPEC\\|assign\\|c\\(?:ase\\|ondition\\)\\|end_\\(?:CTLSPEC\\|INVARSPEC\\|LTLSPEC\\|assign\\|c\\(?:ase\\|ondition\\)\\|index_of\\|result\\)\\|index_of\\|result\\)\\>" . font-lock-keyword-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defconst behaverify-font-lock-keywords-6
  (append behaverify-font-lock-keywords-5
		  (list
		   '("\\<\\(a\\(?:bs\\|ctive\\|ddition\\|lways_\\(?:finally\\|globally\\|next\\|until\\)\\|nd\\)\\|co\\(?:s\\|unt\\)\\|division\\|e\\(?:qu\\(?:al\\|ivalent\\)\\|x\\(?:ists_\\(?:finally\\|globally\\|next\\|until\\)\\|p\\)\\)\\|f\\(?:ailure\\|inally\\(?:_bounded\\)?\\)\\|g\\(?:lobally\\(?:_bounded\\)?\\|reater_than\\(?:_or_equal\\)?\\)\\|historically\\(?:_bounded\\)?\\|i\\(?:mplies\\|ndex\\)\\|l\\(?:ess_than\\(?:_or_equal\\)?\\|n\\)\\|m\\(?:ax\\|in\\|od\\|ultiplication\\)\\|n\\(?:e\\(?:gative\\|xt\\)\\|ot\\(?:_\\(?:equal\\|previous_not\\)\\)?\\)\\|o\\(?:nce\\(?:_bounded\\)?\\|r\\)\\|previous\\|r\\(?:elease\\(?:_bounded\\)?\\|unning\\)\\|s\\(?:in\\(?:ce\\(?:_bounded\\)?\\)?\\|u\\(?:btraction\\|ccess\\)\\)\\|t\\(?:an\\|riggered\\(?:_bounded\\)?\\)\\|until\\(?:_bounded\\)?\\|x\\(?:n?or\\)\\)\\>" . font-lock-builtin-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defconst behaverify-font-lock-keywords-7
  (append behaverify-font-lock-keywords-6
		  (list
		   '("\\<\\(False\\|True\\|failure\\|hypersafety\\|runnning\\|success\\)\\>" . font-lock-constant-face)))
  "Additional Keywords to highlight in BehaVerify mode.")

(defvar behaverify-font-lock-keywords behaverify-font-lock-keywords-7
  "Default highlighting expressions for BehaVerify mode.")


;;(buffer-substring-no-properties (line-beginning-position) (line-end-position))

;; behaverify-tab-witdh is set in your user file.

(defun behaverify-indent-line ()
  "Indent current line as BehaVerify code."
  (interactive)
  (beginning-of-line)  ; moves us to the start of the line.
  (if (bobp)  ; true if at start of buffer
      (indent-line-to 0)  ; First line is always non-indented
    (let ((indent-level 0) (modify-indent-level 0))
      (beginning-of-line)  ; moves us to the start of the line.
      (if (looking-at "^[[:blank:]]*}.*$") (setq modify-indent-level -1) nil)  ; if we have spaces then }, we would like that } to indent itself back.
      (save-excursion  ; we will save our current location
	(let ((still-searching t))  ; this will be used to track if we are done looping
	  (while still-searching  ; loop
	    (forward-line -1)  ; go to the start of previous line.
	    (if (bobp) (setq still-searching nil))  ; we will have to stop the loop if we're at the start.
	    (if (looking-at "^[[:blank:]]*$") nil  ; if we're looking at a line with nothing in it, do nothing. otherwise, see below.
	      (let ((num-open (how-many "{" (line-beginning-position) (line-end-position)))  ; the number of { in the line
		    (num-closed (how-many "}" (line-beginning-position) (line-end-position))))  ; the number of } in the line
		; (message "num-open = %d" num-open)
		(setq still-searching nil)  ; done searching
		(if (looking-at "^[[:blank:]]*}.*$") (setq modify-indent-level (+ 1 modify-indent-level)))  ; if the prior line also shifted back 1 as a ___} line, don't double it
		(setq indent-level (+ (current-indentation) (* 4 (+ (- num-open num-closed) modify-indent-level))))  ; compute indent level
		)  ; END progn
	      )  ; END if looking at
	    )  ; END while
	  )  ; END let still searching
	)  ; END save-excursion
      (if (< indent-level 0) (indent-line-to 0) (indent-line-to indent-level))  ; run indent command, don't try to negative indent.
      )  ; END let indent level
    )  ; END if bobp
  )  ; END function

(defun behaverify-indent-all-lines ()
  "Indent everyline in the buffer."
  (interactive)
  (save-excursion
    (goto-char (point-min))
    (let ((still-moving t))
      (while still-moving
	(forward-line)
	(if (eobp) (setq still-moving nil))
	(behaverify-indent-line)
	)
      )
    )
  )

(defvar behaverify-mode-syntax-table
  (let ((behaverify-mode-syntax-table (make-syntax-table)))
	
    ; This is added so entity names with underscores can be more easily parsed
	(modify-syntax-entry ?_ "w" behaverify-mode-syntax-table) ; mark _ as a word character
	(modify-syntax-entry ?\' "\"" behaverify-mode-syntax-table) ; mark ' as a string
	(modify-syntax-entry ?\" "\"" behaverify-mode-syntax-table) ; mark " as a string
	(modify-syntax-entry ?\# ". 14" behaverify-mode-syntax-table) ; mark # as punctuation, also 1st token of comment start and 2nd token of comment end
	(modify-syntax-entry ?{ "( 2" behaverify-mode-syntax-table) ; mark { as an open bracket and the 2nd token of a comment start
	(modify-syntax-entry ?} ") 3" behaverify-mode-syntax-table) ; mark } as a close bracket, and the 1st token of a comment end
	behaverify-mode-syntax-table)
  "Syntax table for behaverify-mode.")
  
(defun behaverify-mode ()
  (interactive)
  (kill-all-local-variables)
  (use-local-map behaverify-mode-map)
  (set-syntax-table behaverify-mode-syntax-table)
  ;; Set up font-lock
  (set (make-local-variable 'font-lock-defaults) '(behaverify-font-lock-keywords))
  ;; Register our indentation function
  (set (make-local-variable 'indent-line-function) 'behaverify-indent-line)
  (setq major-mode 'behaverify-mode)
  (setq mode-name "BehaVerify")
  (run-hooks 'behaverify-mode-hook))

(provide 'behaverify-mode)

;;; behaverify-mode.el ends here
