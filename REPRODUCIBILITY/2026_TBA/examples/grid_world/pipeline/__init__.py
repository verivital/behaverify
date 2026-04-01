"""
pipeline — compositional verification pipeline for grid-world NSBTs.

Stages:
    contracts  → verify A/G contracts via alpha-beta-CROWN
    smv        → convert .tree + contracts to a contract-based nuXmv SMV
    nuxmv      → run nuXmv and parse INVARSPEC / CTLSPEC verdicts
    report     → write pipeline_report.json and print summary

Public surface used by run_compositional_pipeline.py:
    from pipeline.utils     import setup
    from pipeline.contracts import run_contracts, skip_contracts
    from pipeline.smv       import run_smv_generation
    from pipeline.nuxmv     import run_nuxmv
    from pipeline.report    import write_report
"""
