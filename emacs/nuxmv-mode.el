;;; nuxmv-mode-el -- Major mode for editing nuXmv files

;; Author: Serena Aura Serbinowska
;; Created: 2023-08-04
;; Last Edit: 2023-08-04
;; Keywords: nuXmv major-mode

;;; Commentary:
;;
;; heavily based on this tutorial: https://www.emacswiki.org/emacs/ModeTutorial

;;; Code:
(defvar nuxmv-mode-hook nil)
(defvar nuxmv-mode-map
  (let ((nuxmv-mode-map (make-keymap)))
    (define-key nuxmv-mode-map "\C-j" 'newline-and-indent)
    nuxmv-mode-map)
  "Keymap for nuXmv major mode.")

(add-to-list 'auto-mode-alist '("\\.smv\\'" . nuxmv-mode))

(defconst nuxmv-font-lock-keywords-1
  (list
   '("\\<\\(MODULE\\)\\>" . font-lock-warning-face))
  "Minimal highlighting expressions for nuXmv mode.")

(defconst nuxmv-font-lock-keywords-2
  (append nuxmv-font-lock-keywords-1
		  (list
		   '("\\<\\(CONSTANTS\\|DEFINE\\|F\\(?:ROZENVAR\\|UN\\)\\|I?VAR\\)\\>" . font-lock-variable-name-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defconst nuxmv-font-lock-keywords-3
  (append nuxmv-font-lock-keywords-2
		  (list
		   '("\\<\\(array\\|boolean\\|clock\\|integer\\|real\\|\\(?:un\\)?signed word\\)\\>" . font-lock-type-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defconst nuxmv-font-lock-keywords-4
  (append nuxmv-font-lock-keywords-3
		  (list
		   '("\\<\\(!=\\|->\\|<\\(?:->\\|[<=]\\)\\|>[=>]\\|A[FGX]\\|CONSTARRAY\\|E[FGX]\\|READ\\|WRITE\\|abs\\|bool\\|co\\(?:s\\|unt\\)\\|ex\\(?:p\\|tend\\)\\|floor\\|in\\|ln\\|m\\(?:ax\\|in\\|od\\)\\|pi\\|resize\\|s\\(?:i\\(?:gned\\|n\\|zeof\\)\\|wcost\\)\\|t\\(?:an\\|oint\\|ypeof\\)\\|u\\(?:n\\(?:ion\\|signed\\)\\|wconst\\)\\|word1\\|x\\(?:n?or\\)\\|[!&*+/<-?FGHOS-VXYZ|-]\\)\\>" . font-lock-function-name-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defconst nuxmv-font-lock-keywords-5
  (append nuxmv-font-lock-keywords-4
		  (list
		   '("\\<\\(ASSIGN\\|COMPASSION\\|FAIRNESS\\|IN\\(?:IT\\|VAR\\)\\|JUSTICE\\|TRANS\\|case\\|esac\\|\\(?:ini\\|nex\\)t\\)\\>" . font-lock-keyword-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defconst nuxmv-font-lock-keywords-6
  (append nuxmv-font-lock-keywords-5
		  (list
		   '("\\<\\(\\(?:CTL\\|INVAR\\|LTL\\)?SPEC\\)\\>" . font-lock-builtin-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defconst nuxmv-font-lock-keywords-7
  (append nuxmv-font-lock-keywords-6
		  (list
		   '("\\<\\(\\(?:FALS\\|TRU\\)E\\)\\>" . font-lock-constant-face)))
  "Additional Keywords to highlight in nuXmv mode.")

(defvar nuxmv-font-lock-keywords nuxmv-font-lock-keywords-7
  "Default highlighting expressions for nuXmv mode.")


;;(buffer-substring-no-properties (line-beginning-position) (line-end-position))

(defun nuxmv-indent-line ()
  "Indent current line as nuXmv code."
  (interactive)
  (beginning-of-line)  ; moves us to the start of the line.
  (if (bobp)  ; true if at start of buffer
      (indent-line-to 0)  ; First line is always non-indented
    
    (let ((indent-level 0) (case-count 0))
      (beginning-of-line)  ; moves us to the start of the line.
      (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "MODULE" (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (setq indent-level 0) ; if we start with MODULE, indent to 0. ELSE, do below
	(if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) (or "CONSTANTS" "DEFINE" "VAR" "IVAR" "FROZENVAR" "FUN" "ASSIGN" "TRANS" "INIT" "FAIRNESS" "JUSTICE" "COMPASSION" "INVAR") (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (setq indent-level 1) ; if we start with assign, or var, or w/e. indent to 1. else, do below
	  (save-excursion  ; we will save our current location
	    (let ((still-searching t))  ; this will be used to track if we are done looping
	      (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "esac" (zero-or-more blank) ";" (zero-or-more not-newline) line-end))) (setq case-count (- case-count 1)) nil) ; esac on current line is worth 1 indent level
	      (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "case" (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (setq case-count (+ case-count 1)) nil) ; case on current line is worth 1 indent level
	      (while still-searching  ; loop
		(forward-line -1)  ; go to the start of previous line.
		(if (bobp) (setq still-searching nil))  ; we will have to stop the loop if we're at the start.
		(if (looking-at "^[[:blank:]]*$") nil  ; if we're looking at a line with nothing in it, do nothing. otherwise, see below.
		  (progn
		    (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) (or "CONSTANTS" "DEFINE" "VAR" "IVAR" "FROZENVAR" "FUN" "ASSIGN" "TRANS" "INIT" "FAIRNESS" "JUSTICE" "COMPASSION" "INVAR") (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (progn (setq still-searching nil) (setq indent-level 2))
		      (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "MODULE" (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (progn (setq still-searching nil) (setq indent-level 1)) nil)
		      )
		    (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "case" (optional (sequence (one-or-more blank) (zero-or-more not-newline))) line-end))) (setq case-count (+ case-count 2)) nil) ; case on previous lines is worth 2 indent levels
		    (if (looking-at (rx (sequence line-start (optional (sequence (zero-or-more not-newline) (one-or-more blank))) "esac" (zero-or-more blank) ";" (zero-or-more not-newline) line-end))) (setq case-count (- case-count 2)) nil) ; esac on previous lines is worth 2 indent levels
		    )
		  )  ; END if looking at
		)  ; END while
	      )  ; END let still searching
	    )  ; END save-excursion
	  ) ; END crazy if
	) ; END module if
      (setq indent-level (* 4 (+ indent-level case-count)))
      (if (< indent-level 0) (indent-line-to 0) (indent-line-to indent-level))  ; run indent command, don't try to negative indent.
      )  ; END let indent level
    )  ; END if bobp
  )  ; END function

(defun nuxmv-indent-all-lines ()
  "Indent everyline in the buffer."
  (interactive)
  (save-excursion
    (goto-char (point-min))
    (let ((still-moving t))
      (while still-moving
	(forward-line)
	(if (eobp) (setq still-moving nil))
	(nuxmv-indent-line)
	)
      )
    )
  )

(defvar nuxmv-mode-syntax-table
  (let ((nuxmv-mode-syntax-table (make-syntax-table)))
	
    ; This is added so entity names with underscores can be more easily parsed
	(modify-syntax-entry ?_ "w" nuxmv-mode-syntax-table) ; mark _ as a word character
	(modify-syntax-entry ?\' "\"" nuxmv-mode-syntax-table) ; mark ' as a string
	(modify-syntax-entry ?\" "\"" nuxmv-mode-syntax-table) ; mark " as a string
	(modify-syntax-entry ?\- ". 12" nuxmv-mode-syntax-table) ; mark - as punctuation, also 1st token of comment start and 2nd token of comment end
	(modify-syntax-entry ?\n ">" nuxmv-mode-syntax-table) ; mark newline as comment ender
	nuxmv-mode-syntax-table)
  "Syntax table for nuxmv-mode.")
  
(defun nuxmv-mode ()
  (interactive)
  (kill-all-local-variables)
  (use-local-map nuxmv-mode-map)
  (set-syntax-table nuxmv-mode-syntax-table)
  ;; Set up font-lock
  (set (make-local-variable 'font-lock-defaults) '(nuxmv-font-lock-keywords))
  ;; Register our indentation function
  (set (make-local-variable 'indent-line-function) 'nuxmv-indent-line)
  (setq major-mode 'nuxmv-mode)
  (setq mode-name "nuXmv")
  (run-hooks 'nuxmv-mode-hook))

(provide 'nuxmv-mode)

;;; nuxmv-mode.el ends here
