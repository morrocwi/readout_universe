# Readout Universe — Philosophy and Logic (v1.0 → v2.0-dev "of Everything")

Open-science, reproducible textbook (83 pp.). Author: Yaoharee Lahtee
(ORCID 0009-0005-3861-0626), Open Civil Science Initiative. License: CC BY 4.0.

**v2.0-dev:** this repo is being elevated toward *The Philosophy and Logic of
Everything* — a tier-honest candidacy, never a declared ToE. The governing law of
v2 is the **Lens Law**: every problem, from any domain, is first TRANSLATED into
this book's information-philosophy language and solved inside its logic
(`v2/TRANSLATION_PROTOCOL.md` — Ω_all), with bridges to the machine-checked
physics/biology/AI corpus recorded per-domain in `v2/DOMAIN_LEDGER.md` and release
gates in `v2/ROADMAP_V2.md`. The v1.0 text in `main.tex` is frozen; v2 adds, it
never silently edits.

This repository is the canonical git home of the book so that **any AI or human
can read the full philosophy and logic system directly from source** — no PDF
extraction needed: the complete text lives in [`main.tex`](main.tex) (single file),
with the compiled book in `main.pdf`.

## For AI readers — start here

1. Read [`docs/AI_READING_GUIDE.md`](docs/AI_READING_GUIDE.md) — entry order, tier
   discipline, and what the book does NOT claim.
2. Read [`main.tex`](main.tex) — the full textbook (plain LaTeX, one file).
3. Read [`CLAIMS.md`](CLAIMS.md) — one falsifiable claim per row, each with its
   check command.

**Tier legend (never collapse):**
`Th_coqc` (machine-checked, axiom-free) ≠ `finite_diagnostic` (verified numeric run)
≠ `Dr` (declared-bridge reading) ≠ `Open` (always carries a stance, never bare).

## Reproduce every claim (~5 minutes)

```
make verify        # LTP1 (expect PASS 3/3), LTP2-4 (expect PASS 8/8),
                   # coqc UPL_Sorites.v (expect exit 0 + 3x "Closed under the global context")
make pdf           # builds main.pdf from main.tex (pdflatex x2)
make all           # verify + pdf
```

Requirements: Python 3 + numpy; Coq (8.18+; 8.20.1 verified — see
[`docs/VERIFIED_RUNS.md`](docs/VERIFIED_RUNS.md)); TeX Live (pdflatex).

Found a genuine falsification? That is the book working as designed — report it.

## For AI operators — the APIs, where they are, how to call them (v2)

Everything below runs from the repo root with `sys.path.insert(0, '.')`.
Verify the whole stack first: `python3 -m pytest -q` (must be all-green).

**1. The gates — `lens/gates.py` (Ω_all G1–G13, 8-piece Extraction):**
```python
from lens import Issue, Quantity, run_gates
ex = run_gates(Issue(statement="...", quantities=[Quantity("h", chain="...")]))
for g in ex.gates: print(g.gate, g.verdict, g.tier, g.detail)
```
Computable gates compute (`finite_diagnostic`): G5 null-space (LTP4), G6
load-bearing discard (LTP3), G10 limit certificate, G11 formula equivalence,
G13 timescale atlas. Judgment gates return `PROMPT` — answer them, never skip.
Full field list of `Issue` and the W1–W7 workflow: `skill/readout-lens/SKILL.md`.

**2. Numerical computation — `lens/compute.py` (USE BEFORE hand-writing numpy):**
```python
from lens import compute
compute.list_closures(category="kinematics")        # 231 audited closures
compute.solve_closure("acceleration", dv=10.0, t=2.0)  # value+units+citation
compute.describe_closure("acceleration")            # required args per closure
compute.list_systems()                              # 9 solvers: truss/FEM/modal/Ising/...
compute.domain("thermodynamics")                    # 7 domain calculator modules
```
Raises `SolverUnavailable` when the live solver is absent → record SKIPPED in
the extraction's not-checked ledger; never improvise the number.

**3. Verified operator + lexicon (vendored snapshots) — `lens/vendor/`:**
```python
from lens.vendor.operator_api import Operator       # OP1–OP6, two-axis tier
from lens.vendor.lexicon import translate_to_philosophy, translate_to_world
```
Provenance + md5 + known gotchas: `lens/vendor/README.md` (never edit snapshots).

**4. Live solver link — `lens/solver_link.py`:** G9–G13 and `compute` reach the
sibling `research_universal_solver` LIVE (override path with env
`ANSE_SOLVER_PATH`). Its three MCP servers (`operator`/`universe`/`arc` — incl.
`coq_verify` and `arc_search` over 292 Coq files) are documented in
`skill/readout-lens/SKILL.md` §Live solver link.

**5. The Claude Code skill — `skill/readout-lens/`:** drives W1–W7 against the
APIs above. Install `bash skill/install.sh [--global]`; details `skill/INSTALL.md`.

**6. Executed case studies — `ap/`:** AP0 (gate anchors), AP1 (Hubble), AP2
(FXT), AP3 (DESI) — every numerical claim in the docs has its pytest here;
runs logged in `docs/VERIFIED_RUNS.md`.

## Repository layout

```
main.tex                              full textbook source (single file, canonical)
main.pdf                              compiled book (83 pp.)
CLAIMS.md                             falsifiable-claims register (C1–C7)
Makefile                              verify / pdf / all
code/LTP1_logic_as_residual_flow.py   finite_diagnostic protocol 1  (C1–C3)
code/LTP2_3_4_battery.py              finite_diagnostic protocols 2–4 (C4–C6)
code/UPL_Sorites.v                    Th_coqc formal floor, axiom-free (C7)
docs/AI_READING_GUIDE.md              how an AI should read this system
docs/VERIFIED_RUNS.md                 executed verification log (dated, per machine)
v2/                                   the lens doctrine (DNA, Lens Law, Doctrine of
                                      Quantity, Position, Forced-Identification thesis)
lens/                                 the lens as code: gates.py (G1–G13) ·
                                      compute.py (audited calculators) ·
                                      solver_link.py (live) · vendor/ (snapshots)
ap/                                   executed case studies (pytest; ap0–ap3)
skill/readout-lens/                   installable Claude Code skill (W1–W7)
evidence/                             in-repo Coq evidence (RD.v, URCF_RD_All.v)
```
Note: `lens/`, `skill/`, `ap/` are proprietary (LICENSE EXCEPTIONS), not CC BY.

## We do NOT claim

`finite_diagnostic` = proof; Coq scope beyond monotone g; B1 uniqueness;
Gödel/liar/ethics solved; supersession of any tradition in Part IV;
machine-independent timings.
