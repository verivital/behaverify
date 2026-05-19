# ATVA 2026 Reproducibility

## Description of the content of the artifact:
The artifact provides a self-contained Docker image that reproduces, end-to-end, the three quantitative results in the BehaVerify ATVA tool paper:

**To reproduce results, please read [`compare/README.md`](compare/README.md).** It contains the two-command Docker workflow, expected runtimes, output file descriptions, and troubleshooting.

| Section / Table        | What this image runs                                      |
|------------------------|-----------------------------------------------------------|
| Table 2 (Sec 4.1)      | BehaVerify FF vs naive ablation, N = 1..10, **3-run average**, 5 min per-instance timeout |
| Table 3 (Sec 4.2)      | BehaVerify drone3 + droneNew  AND  BT2Fiacre drone3 + drone4 (full bt2fiacre → frac → tina pipeline) |
| Section 4.3            | BehaVerify on BT2BIP's MarsRover + TrainControl examples  |

## Installation instructions:
Docker image build and container run instructions for both the **"Smoke test"** and the **"Full run"** are available in in [`compare/README.md`](compare/README.md). Both tests require two lines each.


## Instructions for the smoke test:
Under subsection **"Smoke test"** in [`compare/README.md`](compare/README.md), run the two-line script to reproduce the smoke test.

## Instructions for the full evaluation:
Under subsection **"Full run"** in [`compare/README.md`](compare/README.md), run the two-line script to reproduce paper results.

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
