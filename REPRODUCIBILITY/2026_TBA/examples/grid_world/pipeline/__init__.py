"""
pipeline — compositional verification pipeline for grid-world NSBTs.

Stages:
    wrap_contract_request  → verify A/G contracts via alpha-beta-CROWN
    convert_contracts_to_smv  → convert .tree + contracts to a contract-based nuXmv SMV
    run_nuxmv_verification    → run nuXmv and parse INVARSPEC / CTLSPEC verdicts
    write_pipeline_report     → write pipeline_report.json and print summary

Public surface used by run_compositional_pipeline.py:
    from pipeline.resolve_pipeline_paths  import setup
    from pipeline.wrap_contract_request   import run_contracts, skip_contracts
    from pipeline.convert_contracts_to_smv import run_smv_generation
    from pipeline.run_nuxmv_verification  import run_nuxmv
    from pipeline.write_pipeline_report   import write_report
"""
