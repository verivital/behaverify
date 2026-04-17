"""
pipeline — shared compositional verification infrastructure for 2026_TBA examples.

Package layout:
    neuro/               neural-network verifier backends (mirrors "symbolic/" for the neuro-symbolic split)
        crown/
            crown_verification.py   shared CROWN invocation, status normalization, config
        nnv/             NNV verifier (placeholder)
    symbolic/            symbolic model checker backends
        nuxmv/
            run_nuxmv_verification.py   nuXmv subprocess runner + verdict parser
        uclid5/          UCLID5 backend (placeholder)
    resolve_pipeline_paths.py   RSS helpers; grid-world path setup
    write_pipeline_report.py    generic JSON report writer + console summary

Usage pattern (from an example script):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # 2026_TBA/

    from pipeline.neuro.crown.crown_verification        import run_crown_verification, build_crown_config
    from pipeline.symbolic.nuxmv.run_nuxmv_verification import run_nuxmv
    from pipeline.write_pipeline_report              import write_report
"""
