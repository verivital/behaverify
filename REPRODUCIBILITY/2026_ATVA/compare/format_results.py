#!/usr/bin/env python3
"""Render Table 2, Table 3, and Section 4.3 from the JSON/CSV intermediates
written by the run_table*.sh scripts.

Reads:
    <out>/table2_avg.csv
    <out>/table3_behaverify.json
    <out>/table3_bt2fiacre.json
    <out>/section43_behaverify.json

Writes:
    stdout       -- the three formatted tables
    <out>/results.txt  -- same content
"""
from __future__ import annotations
import csv
import io
import json
import pathlib
import sys


def _read_json(p):
    return json.loads(p.read_text()) if p.exists() else None


def _fmt_table(rows, headers):
    """Plain ASCII table renderer."""
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(str(x)) for x in c) for c in cols]
    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    lines = [sep,
             "| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, widths)) + " |",
             sep]
    for r in rows:
        lines.append("| " + " | ".join(f"{x:<{w}}" for x, w in zip(r, widths)) + " |")
    lines.append(sep)
    return "\n".join(lines)


def render_table2(out_dir):
    p = out_dir / "table2_avg.csv"
    if not p.exists():
        return "[Table 2] (not run; missing table2_avg.csv)"
    with p.open(newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return "[Table 2] (empty)"
    headers, data = rows[0], rows[1:]
    return ("Table 2: BehaVerify Fastforwarding vs Naive (averaged over 3 runs, "
            "5 min per-instance timeout)\n"
            + _fmt_table(data, headers))


def render_table3(out_dir):
    bv = _read_json(out_dir / "table3_behaverify.json")
    bt = _read_json(out_dir / "table3_bt2fiacre.json")
    if bv is None and bt is None:
        return "[Table 3] (not run)"

    def _fmt(x):
        if x is None:
            return "-"
        if isinstance(x, float):
            return f"{x:.2f}"
        return str(x)

    def _bt_prep(entry):
        """BT2Fiacre 'Prep' = btf->fcr + frac (.fcr->.net/.ltl).
        Returns 'TIMEOUT' if any included stage timed out / failed."""
        if not entry:
            return None
        stages = ("btf_to_fcr", "frac")
        timeouts = set(entry.get("timeouts") or [])
        if timeouts & set(stages):
            return "TIMEOUT"
        s = sum((entry.get(k + "_sec") or 0) for k in stages)
        return s if s else None

    def _bt_check(entry):
        """BT2Fiacre 'Check Height' = sift + selt."""
        if not entry:
            return None
        stages = ("sift", "selt")
        timeouts = set(entry.get("timeouts") or [])
        if timeouts & set(stages):
            return "TIMEOUT"
        if {"btf_to_fcr", "frac"} & timeouts:
            return "TIMEOUT"
        s = sum((entry.get(k + "_sec") or 0) for k in stages)
        return s if s else None

    def _bt_states(entry, key):
        if not entry:
            return None
        if entry.get("timeouts"):
            return "TIMEOUT"
        return entry.get(key)

    headers = ["Task", "BV drone3", "BV droneNew",
               "BT2F drone3", "BT2F drone4 (~droneNew)"]
    bv = bv or {"drone3": {}, "droneNew": {}}
    bt = bt or {"drone3": {}, "drone4_~droneNew": {}}
    bt3, bt4 = bt.get("drone3", {}), bt.get("drone4_~droneNew", {})

    rows = [
        ["Prep (sec)",
         _fmt(bv["drone3"].get("prep_sec")),
         _fmt(bv["droneNew"].get("prep_sec")),
         _fmt(_bt_prep(bt3)),
         _fmt(_bt_prep(bt4))],
        ["Check Height (sec)",
         _fmt(bv["drone3"].get("check_height_sec")),
         _fmt(bv["droneNew"].get("check_height_sec")),
         _fmt(_bt_check(bt3)),
         _fmt(_bt_check(bt4))],
        ["Reach. states (log2)",
         _fmt(bv["drone3"].get("reach_log2")),
         _fmt(bv["droneNew"].get("reach_log2")),
         _fmt(_bt_states(bt3, "reach_log2")),
         _fmt(_bt_states(bt4, "reach_log2"))],
        ["Total states (log2)",
         _fmt(bv["drone3"].get("total_log2")),
         _fmt(bv["droneNew"].get("total_log2")),
         _fmt(_bt_states(bt3, "total_log2")),
         _fmt(_bt_states(bt4, "total_log2"))],
    ]
    note = ("\n  BT2Fiacre uses 'set default_prop on' (matches the paper's "
            "Makefile rule);\n"
            "  per-stage timeout BT2F_TIMEOUT (default 1800 s).")
    return ("Table 3: BehaVerify drone3 / droneNew  vs  BT2Fiacre drone3 / drone4\n"
            "(BT2Fiacre's drone4 is a reactive reformulation -- analogous to "
            "BehaVerify's droneNew)\n"
            + _fmt_table(rows, headers) + note)


def render_section43(out_dir):
    p = out_dir / "section43_behaverify.json"
    if not p.exists():
        return "[Section 4.3] (not run)"
    data = json.loads(p.read_text())
    rows = []
    for stem in ("MarsRover", "TrainControl"):
        e = data.get(stem, {})
        rows.append([
            stem,
            ", ".join(e.get("verdicts") or []) or "-",
            f"{e['wall_sec']:.2f}" if e.get("wall_sec") is not None else "-",
        ])
    return ("Section 4.3: BehaVerify on BT2BIP examples (INVAR specs)\n"
            + _fmt_table(rows, ["Example", "Verdicts", "Wall (sec)"])
            + "\n  Note: BT2BIP itself is not bundled in this image -- only the "
              "BehaVerify-side\n  reproduction is shown. The paper reports BT2BIP "
              "timed out on LTL specs of the\n  larger trees while BehaVerify "
              "completed verification.")


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/out")
    buf = io.StringIO()

    print(file=buf)
    print("=" * 78, file=buf)
    print("BehaVerify ATVA 2026 -- Table 2 / Table 3 / Section 4.3 reproduction", file=buf)
    print("=" * 78, file=buf)
    print(file=buf)
    print(render_table2(out), file=buf)
    print(file=buf)
    print(render_table3(out), file=buf)
    print(file=buf)
    print(render_section43(out), file=buf)
    print(file=buf)
    print("=" * 78, file=buf)
    print("Raw intermediates in:", out, file=buf)
    print("=" * 78, file=buf)

    sys.stdout.write(buf.getvalue())
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.txt").write_text(buf.getvalue())


if __name__ == "__main__":
    main()
