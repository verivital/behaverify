# ATVA 2026 Reproducibility

**Archived artifact:** https://doi.org/10.5281/zenodo.20280547

## Description of the Content of the Artifact:
The artifact provides a self-contained Docker image that reproduces, end-to-end, the three quantitative results in the BehaVerify ATVA tool paper:

| Section / Table        | What this image runs                                      |
|------------------------|-----------------------------------------------------------|
| Table 2 (Sec 4.1)      | BehaVerify FF vs naive ablation, N = 1..10, **3-run average**, 5 min per-instance timeout |
| Table 3 (Sec 4.2)      | BehaVerify drone3 + droneNew  AND  BT2Fiacre drone3 + drone4 (full bt2fiacre → frac → tina pipeline) |
| Section 4.3            | BehaVerify on BT2BIP's MarsRover + TrainControl examples  |

## Recommended Resource Requirements:
All experiments used a 6-core, 12-thread i7-10750H Intel CPU with a 16GB RAM on x86-64 Linux. ARM is untested. Plan for a 3 hour wall-clock for a clean run for the full evaluation. The runtime estimate breakdown is provided under the subsection "Full Evaluation: Expected Runtime" later in the README.

## Installation Instructions:
Download `behaverify-compare.tar.gz` from https://doi.org/10.5281/zenodo.20280547, then load the pre-built image (recommended):

```bash
docker load < behaverify-compare.tar.gz
```

Alternatively, build from source (requires internet access, ~4 min):

```bash
docker build -f compare/Dockerfile -t behaverify-compare .
```

The Dockerfile image uses these dependencies (frozen so the comparison stays repeatable):

| Tool       | Version    | Source                                            |
|------------|------------|---------------------------------------------------|
| BehaVerify | local HEAD | the working tree at build time (`COPY` into image) |
| BT2Fiacre  | `70be4269` | `git://redmine.laas.fr/laas/users/felix/bt2fiacre.git` |
| Tina       | 4.0.0      | `https://projects.laas.fr/tina/`                  |
| Hippo (frac) | 2.7.1    | `https://projects.laas.fr/hippo/`                 |
| nuXmv      | 2.1.0      | `https://nuxmv.fbk.eu/`                           |

> BT2BIP itself is not bundled. The paper's Section 4.3 reports the
> verdict-only comparison (both tools agree on falsity); only the
> BehaVerify side is reproduced here. The output table includes the
> verdicts and BehaVerify wall time.

## Instructions for the Smoke Test:
Run this before the full evaluation to confirm the tool chain works end-to-end
(~3–5 min, no GPU or special hardware required):

```bash
mkdir -p compare/output
docker run --rm \
    -v "$(pwd)/compare/output:/out" \
    behaverify-compare /home/bv/run_smoke.sh /out
```

What it runs and why it is fast:

| Component | What | Why fast |
|---|---|---|
| Table 2 | N=1..3, **1** timing run, 30s timeout | All three instances are sub-second |
| Table 3 | BT2Fiacre/drone3 with persistent-sets (`-P`) | Reduces state space to ~5 markings; finishes in < 5s per stage |
| Sec 4.3 | BehaVerify on MarsRover / TrainControl (normal) | nuXmv finds counterexample immediately |

Expected output (exact timings vary by host and run; structure must match):

```
==========================================================================
BehaVerify ATVA 2026 SMOKE TEST
==========================================================================
...
============================================================
SMOKE TEST RESULTS
============================================================

Table 2 (N=1-3, 1 run, 30s timeout). Expected: all values < 1s
 N    CTL-FF  CTL-Naive    LTL-FF  LTL-Naive
 1      0.01       0.02      0.02       0.03
 2      0.01       0.04      0.02       0.10
 3      0.01       0.11      0.06       0.15
(single-run timings; the full evaluation averages 3 runs, so values will differ slightly)

Table 3 BT2Fiacre smoke (drone3, -P). Expected: all stages < 5s
  btf_to_fcr     : <t>s
  frac           : <t>s
  sift           : <t>s
  selt           : <t>s

Section 4.3 (BehaVerify/BT2BIP). Expected: 'false' verdicts, ~0s wall time
  MarsRover      : verdicts=false, false  wall=0.00s
  TrainControl   : verdicts=false  wall=0.00s

============================================================
Smoke test PASSED. All tools executed without errors.
...
```

The smoke test for Table 3 uses BT2Fiacre's persistent-sets reduction (`-P`), so it finishes quickly. However, this is **not** the configuration reported in the paper.  The full evaluation (`run_all.sh`) omits `-P` and the BT2Fiacre columns correctly show TIMEOUT, matching Table 3.

## Instructions for the Full Evaluation:

```bash
# Run everything. Mounts an output folder so per-run intermediates
# + final results.txt survive on the host.
mkdir -p compare/output
docker run --rm \
    -v "$(pwd)/compare/output:/out" \
    behaverify-compare
```

The single line that does everything inside the container is:

```bash
/home/bv/run_all.sh   # baked in as the image's CMD
```

It runs Table 2 (3-run avg), Table 3 (both tools), Section 4.3 (BehaVerify side), then renders the formatted tables.

### Full Evaluation: Expected Runtime

Using the hardware outlined in the paper and the repository, the full `run_all.sh` should take roughly 3 hours in total:

- Table 2: Three independent timing runs of N=1..10. The timeout is set to 5 minutes. The 5 min timeout fires for CTL naive at N >= 8 and LTL naive at N >= 7. Assume other runs take on average 1 minute. Thus, the expected upper bound is 3 * (CTL N=1..7 \* 1 + 3\*5 + LTL N=1..6 \* 1 + 4\*5) = 143 minutes. In practice, the three runs take roughly 2 hours in total.
- Table 3: BehaVerify side takes around 30-35 minutes (translation + nuXmv INVAR);   BT2Fiacre side takes approximately 10 minutes total.
- Section 4.3: reuses Table 3's MarsRover / TrainControl runs; near-zero marginal cost.

Plan for a 3 hour wall-clock for a clean run.

### Full Evaluation: Expected Output

| Where                         | What                                                   |
|-------------------------------|--------------------------------------------------------|
| **stdout**                    | Final formatted tables                                 |
| `compare/output/results.txt`          | Same content as stdout (for archival / sharing)        |
| `compare/output/table2_avg.csv`       | Per-N FF vs naive averages across 3 runs               |
| `compare/output/table2_run_{1,2,3}/`  | Snapshot of the four `*-Concise` files per run         |
| `compare/output/table3_behaverify.json` | Prep / Check Height / Reach / Total per drone        |
| `compare/output/table3_bt2fiacre.json`  | Per-stage BT2Fiacre timings + state-space sizes      |
| `compare/output/section43_behaverify.json` | MarsRover / TrainControl verdicts + wall time     |
| `compare/output/*.log`                | Raw stdout/stderr from each underlying experiment      |

Expected output (exact timings vary by host and run; structure must match):

```

==============================================================================
BehaVerify ATVA 2026 -- Table 2 / Table 3 / Section 4.3 reproduction
==============================================================================

Table 2: BehaVerify Fastforwarding vs Naive (averaged over 3 runs, 5 min per-instance timeout)
+----+--------------------+-----------+--------------------+-----------+
| N  | CTL-Fastforwarding | CTL-Naive | LTL-Fastforwarding | LTL-Naive |
+----+--------------------+-----------+--------------------+-----------+
| 1  | 0.01               | 0.01      | 0.01               | 0.03      |
| 2  | 0.01               | 0.02      | 0.02               | 0.08      |
| 3  | 0.01               | 0.06      | 0.06               | 0.18      |
| 4  | 0.01               | 0.14      | 0.13               | 0.56      |
| 5  | 0.02               | 0.62      | 0.38               | 3.54      |
| 6  | 0.06               | 4.62      | 1.31               | 35.49     |
| 7  | 0.11               | 53.03     | 4.27               | TIMEOUT   |
| 8  | 0.24               | TIMEOUT   | 13.62              | TIMEOUT   |
| 9  | 0.57               | TIMEOUT   | 45.75              | TIMEOUT   |
| 10 | 2.24               | TIMEOUT   | 153.65             | TIMEOUT   |
+----+--------------------+-----------+--------------------+-----------+

Table 3: BehaVerify drone3 / droneNew  vs  BT2Fiacre drone3 / drone4
(BT2Fiacre's drone4 is a reactive reformulation -- analogous to BehaVerify's droneNew)
+----------------------+-----------+-------------+-------------+-------------------------+
| Task                 | BV drone3 | BV droneNew | BT2F drone3 | BT2F drone4 (~droneNew) |
+----------------------+-----------+-------------+-------------+-------------------------+
| Prep (sec)           | 0.73      | 1.14        | 0.21        | 0.24                    |
| Check Height (sec)   | 86.87     | 0.48        | TIMEOUT     | TIMEOUT                 |
| Reach. states (log2) | 22.83     | 16.53       | TIMEOUT     | TIMEOUT                 |
| Total states (log2)  | 51.52     | 39.97       | TIMEOUT     | TIMEOUT                 |
+----------------------+-----------+-------------+-------------+-------------------------+
  BT2Fiacre uses 'set default_prop on' (matches the paper's Makefile rule);
  per-stage timeout BT2F_TIMEOUT (default 1800 s).

Section 4.3: BehaVerify on BT2BIP examples (INVAR specs)
+--------------+--------------+------------+
| Example      | Verdicts     | Wall (sec) |
+--------------+--------------+------------+
| MarsRover    | false, false | 0.01       |
| TrainControl | false        | 0.01       |
+--------------+--------------+------------+
  Note: BT2BIP itself is not bundled in this image -- only the BehaVerify-side
  reproduction is shown. The paper reports BT2BIP timed out on LTL specs of the
  larger trees while BehaVerify completed verification.

==============================================================================
Raw intermediates in: /out
==============================================================================
```

## Full Evaluation: Additional Details
After running the full evaluation scripts, the remainder of the README will elaborate on the terms featured in the full evaluation output logs.

### What "exact instance" means

- BehaVerify is COPYed into the image from the host's working tree (filtered
  by `.dockerignore`). Every `docker build` snapshots the current HEAD so the
  Tables stay tied to a specific code revision.
- BT2Fiacre is pinned to a specific commit SHA in the Dockerfile (build
  arg `BT2FIACRE_SHA`). Override at build time if needed:
  `docker build --build-arg BT2FIACRE_SHA=<sha> -f .../Dockerfile -t behaverify-compare .`
- Tina, Hippo, nuXmv are pinned by version number in the same way.

### How BT2Fiacre is invoked (matches paper's measurement)

The BT2Fiacre pipeline is invoked exactly as the paper's harness does:

```
bt2fiacre -c "set tina_compact on" -c "set tick Node" -c "set default_prop off" \
          -c "load bt drone3.btf" -c "save fiacre /tmp/drone3.fcr"
frac -tts /tmp/drone3.fcr /tmp/drone3.tts
sift /tmp/drone3.tts/drone3.net -kts /tmp/drone3.ktz -stats
selt /tmp/drone3.ktz /tmp/drone3.tts/drone3.ltl -b
```

Two knobs control how closely this reproduces the paper's "BT2Fiacre TIMEOUT" cell:

| Env var                  | Default | Effect                                                                 |
|--------------------------|---------|------------------------------------------------------------------------|
| `BT2F_TIMEOUT`           | `300`   | Per-stage cap in seconds (5 min, matching Table 2's instance cap)      |
| `BT2F_PERSISTENT_SETS`   | `0`     | When `1`, passes `-P` to `sift` (persistent-sets reduction)            |

- **Default** (`BT2F_PERSISTENT_SETS=0`): reproduces the paper's slow workload. The reference comparison report shows that without `-P` the drone3 state space does not finish even at 90 min: at our 5 min cap it cleanly TIMEOUTs in the `sift` stage.
- **Fast path** (`BT2F_PERSISTENT_SETS=1`): adds Tina's persistent-sets reduction. The full pipeline finishes in under 1 second with roughly 5 markings: useful for sanity-checking the toolchain works end-to-end, but **does not** reflect the paper's measurement.

Override either at run time:

```bash
docker run --rm \
    -e BT2F_TIMEOUT=1800 -e BT2F_PERSISTENT_SETS=1 \
    -v "$(pwd)/compare/output:/out" \
    behaverify-compare
```

### Run on a subset only

The component scripts are individually invocable inside the container:

```bash
docker run --rm -v "$(pwd)/compare/output:/out" behaverify-compare /home/bv/run_table2.sh    /out
docker run --rm -v "$(pwd)/compare/output:/out" behaverify-compare /home/bv/run_table3.sh    /out
docker run --rm -v "$(pwd)/compare/output:/out" behaverify-compare /home/bv/run_section43.sh /out
docker run --rm -v "$(pwd)/compare/output:/out" behaverify-compare python3 /home/bv/format_results.py /out
```

---

## Running the GUI
The BehaVerify GUI can be used using the same script provided in the paper.

```python
python src/behaverify_gui.py
```

## BehaVerify Documentation: Reuse and Repurposing Beyond the Tool Paper Results
In addition to the artifact, BehaVerify has detailed documentation available on [https://verivital.github.io/behaverify/index.html](https://verivital.github.io/behaverify/index.html). There are starter guides for creating [custom trees in BehaVerify](https://verivital.github.io/behaverify/getting-started/first-model.html) and [various examples](https://verivital.github.io/behaverify/examples/index.html) to better understand the tool. We have also wrote an [API reference](https://verivital.github.io/behaverify/api/index.html) to facilitate reuse and repurposing.

## Folder Overview (Outside of Comparison Tests)

| Folder | Contents |
|---|---|
| [`compare/`](compare/) | Self-contained Docker harness that reproduces Tables 2 & 3 and Section 4.3 in one image |
| [`scripts/`](scripts/) | Shell scripts called by `compare/` to generate SMV models and run nuXmv timing sweeps |
| [`examples/BT2Fiacre/`](examples/BT2Fiacre/) | Drone3 and droneNew `.tree` sources for Table 3 (BehaVerify vs. BT2Fiacre comparison) |
| [`examples/BT2BIP/`](examples/BT2BIP/) | MarsRover and TrainControl `.tree` sources for Section 4.3 (BehaVerify vs. BT2BIP comparison) |
| [`examples/EncodingComparison/`](examples/EncodingComparison/) | Binary-tree benchmark sources (N = 1..10) for Table 2 (fastforwarding vs. naive ablation) |
| [`examples/NetworkExample/`](examples/NetworkExample/) | NSBT repo example with trained ONNX networks, used for the network verification experiment |
| [`examples/DrunkenDrone/`](examples/DrunkenDrone/) | DrunkenDrone `.tree` source used for Figure 1 |
| [`examples/MoVe4BT/`](examples/MoVe4BT/) | MoVe4BT comparison example sources, processed by `scripts/` |
| [`saved_images/`](saved_images/) | Shows the saved images for the Mars Rover and Train Control examples referenced in Section 4.3 |
| [`src/`](src/) | Frozen BehaVerify source snapshot; `scripts/` calls `src/dsl_to_nuxmv.py` directly |
| [`metamodel/`](metamodel/) | Frozen BehaVerify DSL grammar (`behaverify.tx`), referenced by `src/dsl_to_nuxmv.py` |
| [`requirements/`](requirements/) | Python dependency list installed by `compare/Dockerfile` |
