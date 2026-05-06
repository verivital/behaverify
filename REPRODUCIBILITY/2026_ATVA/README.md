# ATVA 2026 Reproducibility

**To reproduce results, read [`compare/README.md`](compare/README.md).** It contains the two-command Docker workflow, expected runtimes, output file descriptions, and troubleshooting. Everything else in this folder exists to support that workflow.

---

## Folder Overview

| Folder | Contents |
|---|---|
| [`compare/`](compare/) | Self-contained Docker harness that reproduces Tables 2 & 3 and Section 4.3 in one image; start here |
| [`scripts/`](scripts/) | Shell scripts called by `compare/` to generate SMV models and run nuXmv timing sweeps |
| [`examples/BT2Fiacre/`](examples/BT2Fiacre/) | Drone3 and droneNew `.tree` sources for Table 3 (BehaVerify vs. BT2Fiacre comparison) |
| [`examples/BT2BIP/`](examples/BT2BIP/) | MarsRover and TrainControl `.tree` sources for Section 4.3 (BehaVerify vs. BT2BIP comparison) |
| [`examples/EncodingComparison/`](examples/EncodingComparison/) | Binary-tree benchmark sources (N = 1..10) for Table 2 (fastforwarding vs. naive ablation) |
| [`examples/NetworkExample/`](examples/NetworkExample/) | NSBT repo example with trained ONNX networks, used for the network verification experiment |
| [`examples/DrunkenDrone/`](examples/DrunkenDrone/) | DrunkenDrone `.tree` source used for Figure 1 |
| [`examples/MoVe4BT/`](examples/MoVe4BT/) | MoVe4BT comparison example sources, processed by `scripts/` |
| [`src/`](src/) | Frozen BehaVerify source snapshot; `scripts/` calls `src/dsl_to_nuxmv.py` directly |
| [`metamodel/`](metamodel/) | Frozen BehaVerify DSL grammar (`behaverify.tx`), referenced by `src/dsl_to_nuxmv.py` |
| [`requirements/`](requirements/) | Python dependency list installed by `compare/Dockerfile` |
