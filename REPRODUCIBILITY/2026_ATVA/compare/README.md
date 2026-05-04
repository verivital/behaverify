# BehaVerify vs BT2Fiacre vs BT2BIP — single-image comparison harness

Self-contained Docker image that reproduces, end-to-end, the three
quantitative results in the BehaVerify ATVA tool paper:

| Section / Table        | What this image runs                                      |
|------------------------|-----------------------------------------------------------|
| Table 2 (Sec 4.1)      | BehaVerify FF vs naive ablation, N = 1..10, **3-run average**, 5 min per-instance timeout |
| Table 3 (Sec 4.2)      | BehaVerify drone3 + droneNew  AND  BT2Fiacre drone3 + drone4 (full bt2fiacre → frac → tina pipeline) |
| Section 4.3            | BehaVerify on BT2BIP's MarsRover + TrainControl examples  |

Pinned versions (frozen so the comparison stays repeatable):

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

## Build and run (two commands)

From the **BehaVerify repo root** (so the local source is in the build
context):

```bash
# 1. Build the image (downloads pinned LAAS + nuXmv tarballs, clones BT2Fiacre).
docker build -f REPRODUCIBILITY/2026_ATVA/compare/Dockerfile -t behaverify-compare .

# 2. Run everything. Mounts an output folder so per-run intermediates
#    + final results.txt survive on the host.
mkdir -p REPRODUCIBILITY/2026_ATVA/compare/output
docker run --rm \
    -v "$(pwd)/REPRODUCIBILITY/2026_ATVA/compare/output:/out" \
    behaverify-compare
```

The single line that does everything inside the container is:

```bash
/home/bv/run_all.sh   # baked in as the image's CMD
```

It runs Table 2 (3-run avg), Table 3 (both tools), Section 4.3 (BehaVerify
side), then renders the formatted tables.

## Output

| Where                         | What                                                   |
|-------------------------------|--------------------------------------------------------|
| **stdout**                    | Final formatted tables                                 |
| `output/results.txt`          | Same content as stdout (for archival / sharing)        |
| `output/table2_avg.csv`       | Per-N FF vs naive averages across 3 runs               |
| `output/table2_run_{1,2,3}/`  | Snapshot of the four `*-Concise` files per run         |
| `output/table3_behaverify.json` | Prep / Check Height / Reach / Total per drone        |
| `output/table3_bt2fiacre.json`  | Per-stage BT2Fiacre timings + state-space sizes      |
| `output/section43_behaverify.json` | MarsRover / TrainControl verdicts + wall time     |
| `output/*.log`                | Raw stdout/stderr from each underlying experiment      |

## What "exact instance" means

- BehaVerify is COPYed into the image from the host's working tree (filtered
  by `.dockerignore`). Every `docker build` snapshots the current HEAD so the
  Tables stay tied to a specific code revision.
- BT2Fiacre is pinned to a specific commit SHA in the Dockerfile (build
  arg `BT2FIACRE_SHA`). Override at build time if needed:
  `docker build --build-arg BT2FIACRE_SHA=<sha> -f .../Dockerfile -t behaverify-compare .`
- Tina, Hippo, nuXmv are pinned by version number in the same way.

## How BT2Fiacre is invoked (matches paper's measurement)

The BT2Fiacre pipeline is invoked exactly as the paper's harness does
(cross-checked with the `2026_FM/comparison/bt2fiacre/run_verification.sh`
reference implementation in another build of this repo):

```
bt2fiacre -c "set tina_compact on" -c "set tick Node" -c "set default_prop off" \
          -c "load bt drone3.btf" -c "save fiacre /tmp/drone3.fcr"
frac -tts /tmp/drone3.fcr /tmp/drone3.tts
sift /tmp/drone3.tts/drone3.net -kts /tmp/drone3.ktz -stats
selt /tmp/drone3.ktz /tmp/drone3.tts/drone3.ltl -b
```

Two knobs control how closely this reproduces the paper's
"BT2Fiacre TIMEOUT" cell:

| Env var                  | Default | Effect                                                                 |
|--------------------------|---------|------------------------------------------------------------------------|
| `BT2F_TIMEOUT`           | `300`   | Per-stage cap in seconds (5 min, matching Table 2's instance cap)      |
| `BT2F_PERSISTENT_SETS`   | `0`     | When `1`, passes `-P` to `sift` (persistent-sets reduction)            |

- **Default** (`BT2F_PERSISTENT_SETS=0`): reproduces the paper's slow
  workload. The reference comparison report shows that without `-P` the
  drone3 state space does not finish even at 90 min — at our 5 min cap
  it cleanly TIMEOUTs in the `sift` stage.
- **Fast path** (`BT2F_PERSISTENT_SETS=1`): adds Tina's persistent-sets
  reduction. The full pipeline finishes in <1 s with ~5 markings — useful
  for sanity-checking the toolchain works end-to-end, but **does not**
  reflect the paper's measurement.

Override either at run time:

```bash
docker run --rm \
    -e BT2F_TIMEOUT=1800 -e BT2F_PERSISTENT_SETS=1 \
    -v "$(pwd)/REPRODUCIBILITY/2026_ATVA/compare/output:/out" \
    behaverify-compare
```

## Run on a subset only

The component scripts are individually invocable inside the container:

```bash
docker run --rm -v "$(pwd)/.../output:/out" behaverify-compare /home/bv/run_table2.sh    /out
docker run --rm -v "$(pwd)/.../output:/out" behaverify-compare /home/bv/run_table3.sh    /out
docker run --rm -v "$(pwd)/.../output:/out" behaverify-compare /home/bv/run_section43.sh /out
docker run --rm -v "$(pwd)/.../output:/out" behaverify-compare python3 /home/bv/format_results.py /out
```

## Expected runtime

On a modern Threadripper-class host (single-CPU, no GPU work), the full
`run_all.sh`:

- Table 2 — three independent timing runs of N=1..10. The 5 min timeout
  fires for naive at N >= 7..8, so the upper bound is ~3 × (N=1..6 fast +
  4 × 5 min) = ~60 min. In practice ~35–45 min.
- Table 3 — BehaVerify side ~5–10 min (translation + nuXmv INVAR);
  BT2Fiacre side ~30 sec total.
- Section 4.3 — reuses Table 3's MarsRover / TrainControl runs; near-zero
  marginal cost.

Plan ~50–60 min wall-clock for a clean run.
