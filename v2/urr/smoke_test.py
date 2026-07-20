#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
(ROOT / "results").mkdir(exist_ok=True)
report = ROOT / "results" / "smoke_report_repro.json"

proc = subprocess.run(
    [
        sys.executable,
        str(ROOT / "urr_reference_runner.py"),
        str(ROOT / "example_ring.yaml"),
        "--output",
        str(report),
    ],
    check=False,
    text=True,
    capture_output=True,
)

print(proc.stdout)
if proc.stderr:
    print(proc.stderr, file=sys.stderr)

if not report.exists():
    raise SystemExit("FAIL: report was not created")

data = json.loads(report.read_text(encoding="utf-8"))
assert data["claim"]["verdict"] == "PASS", data
assert data["claim"]["tier"] == "finite_diagnostic", data
assert data["dynamics"]["reader_el_residual_max"] < 1e-8, data
assert data["dynamics"]["mirror_el_residual_max"] < 1e-8, data
assert data["tape"]["total_conservation_error"] < 1e-12, data
assert data["information"]["status"] == "COMPUTED", data
assert data["meta"]["native_only"] is True, data

print("PASS: URR native smoke test")
