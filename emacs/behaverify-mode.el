(defvar behaverify-mode-hook nil)

(defvar behaverify-mode-map
  (let ((map (make-keymap)))
    (define-key map "\C-j" 'newline-and-indent)
    map)
  "Keymap for BehaVerify major mode")

(add-to-list 'auto-mode-alist '("\\.tree\\'" . behaverify-mode))

