# commands/

This directory contains command files for symbolic model checkers used by the
compositional verification pipeline. Each subdirectory corresponds to one checker.

The pipeline is designed to be checker-agnostic: swapping the symbolic verification
step means pointing `--nuxmv-cmd` (or the equivalent flag for another checker) at
a different subdirectory here, with no changes to the pipeline scripts themselves.

---

## Structure

```
commands/
├── nuxmv_commands/       # nuXmv command files (current default)
│   ├── command_invar         # check_invar only (compositional pipeline default)
│   ├── command_all_invar     # check_invar with internal timing (monolithic benchmark)
│   └── command_combo_invar_ctl  # check_invar + check_ctlspec (grid world monolithic)
└── (future checkers)     # e.g. uclid5_commands/, ic3_commands/
```

---

## nuXmv command files

| File | Used by | Purpose |
|---|---|---|
| `command_invar` | compositional pipeline (default `--nuxmv-cmd`) | Runs `go` + `check_invar` + `quit`. Output: `-- invariant ... is true/false` |
| `command_all_invar` | monolithic benchmark scripts | Adds `time` and `usage` + `show_property` for internal timing. Output format differs from `command_invar` — uses `[Invar  True  ...]` table |
| `command_combo_invar_ctl` | grid world monolithic pipeline | Runs both `check_invar` and `check_ctlspec` in one nuXmv session |

---

## Adding a new symbolic checker

1. Create a subdirectory: `commands/<checker>_commands/`
2. Add command/script files that invoke the checker and produce parseable output
3. Update the pipeline's verdict parser to handle the new output format
4. Pass the new command file via the appropriate CLI flag
