# ACAS Xu PGD-Disabled Contracts Disclaimer

While there exists a `disabled_pgd/` subfolder within the ACAS Xu contracts, this subfolder is deliberately empty. We have demonstrated that TIMEOUT contracts resolve to UNSAT when enabling the PGD attack in [2026_03_25_pgd_unsat_acas_report.md](../../../../../reports/Acas_Xu_closed_loop/2026_03_25_pgd_unsat_acas_report.md).

A demonstration comparing PGD-disabled and PGD-enabled results can be made with the pre-computed `grid_world` contracts.

Once again, running PGD-disabled on ACAS Xu contracts, even in parallel, can take hours and will hit the timeout limit before finishing, as they are UNSAT contracts.
