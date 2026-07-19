---
name: readout-lens
description: "Use when any research/physics/science issue must be analyzed through the Readout Universe information-philosophy (RD/δ_R lens) — solving INSIDE our logic, not the foreign vocabulary. Runs the Ω_all forcing gates G1–G8 via the real lens API (lens/gates.py), produces the 7-piece maximal extraction, computes identifiability/null-space verdicts, and translates via the real lexicon. Triggers: 'วิเคราะห์ด้วยปรัชญาเรา', 'มองผ่านเลนส์', 'translate into our philosophy and solve', 'ปรัชญาบังคับทิศ', 'run the gates', analyzing an arXiv problem, any claim of tension/anomaly/new-class in a paper."
metadata:
  author: readout-universe
  version: "1.0.0"
  source_of_truth: "lens/gates.py + v2/POSITION.md (never re-derive gates by hand; call the API)"
---

# Readout Lens — solve everything inside our logic

You are operating the control layer of the Readout Universe philosophy. The
knowledge is commodity; your job is to FORCE the direction. Never argue in the
problem's native vocabulary past Step 1 (Lens Law, `v2/TRANSLATION_PROTOCOL.md`).

## Setup (once per session)

```bash
cd <readout_universe>          # repo root (this skill ships inside it)
python3 -m pytest -q           # must be green before trusting the API
```

## Workflow (= W1–W7 of v2/POSITION.md §4)

1. **INTAKE** — fetch the real record first (one arXiv abstract suffices to start).
2. **GATES** — build an `Issue` and run the real gates; quote their output verbatim:

```bash
python3 - <<'EOF'
import sys; sys.path.insert(0, '.')
from lens import Issue, Quantity, run_gates
iss = Issue(
    statement="<the problem, one paragraph>",
    quantities=[Quantity("<name>", chain="<calibration/derivation chain>"), ...],
    grammar=[[...], ...],          # rows of A if known  -> G5 computes null space
    query=[...],                   # direction asked about
    discard_rows=[...],            # what a bounded reading drops -> G6 LTP3 test
    hypothesis_dims=3,             # if grammar unknown
    instrument_change="<new instrument/threshold or ''>",
    refutation_benchmark="<what a claimed refutation compares against or ''>",
    cited_theorems=["<names the source claims are machine-checked>"],  # G9 live arc check
    limit_series=([samples...], [limit_vars...]), limit_side="zero",   # G10 LimitCertificate
    formula_pair=("<closure_a>", "<closure_b>"))                       # G11 equivalence registry
ex = run_gates(iss)
for g in ex.gates: print(f"{g.gate:22s} {g.verdict:6s} [{g.tier}] {g.detail}")
print("COMPLETE:", ex.complete(), "| overall tier:", ex.tier)
EOF
```

3. **FILL the operator pieces** the gates cannot compute (posit ledger with
   verdict classes, decisive-record ranking, falsifier of OUR reading, and the
   piece-8 not-checked ledger: every SKIPPED check + why) — the `Extraction`
   is done only when `ex.complete()` is True.
4. **MICRO-CHECK** — any numerical claim gets a ≤100-line assert script with a
   grammar sanity gate (reproduce a known value first), run via pytest, saved
   as `ap/apN_<slug>.py`. No executed run → no claim.
5. **VERDICT** — answer + tier + falsifier + next decisive record. Tier rules:
   computed = `finite_diagnostic`; interpreted = `Dr`; unfilled = `Open`. Never
   upgrade; never quote a bare number (cite operator + chain + role with it).
6. **REVIEW** — independent adversarial review before any merge/external claim
   (Bounded-Judge Law). 7. **LOG** — `docs/VERIFIED_RUNS.md` + PR.

## Vocabulary calls (never paraphrase from memory)

```bash
python3 -c "import sys; sys.path.insert(0,'.');
from lens.vendor.lexicon import translate_to_philosophy, translate_to_world
print(translate_to_philosophy('''<text>'''))"
```

## Compute calls (the verified operator, tier-honest envelopes)

```bash
python3 -c "import sys; sys.path.insert(0,'.');
from lens.vendor.operator_api import Operator
op = Operator([(0,1,1.0),(1,2,1.0),(2,0,1.0)])
r = op.info([1.,0.,0.]); print(r.value, r.structure_tier, r.value_tier)"
```

## Live solver link (G9–G11 + MCP)

G9–G11 reach the sibling `research_universal_solver` LIVE via
`lens/solver_link.py` (env `ANSE_SOLVER_PATH` overrides the default sibling
path). Solver absent → those gates report PROMPT/SKIPPED honestly; record it
in extraction piece 8 (not-checked ledger), never silently proceed.

Deeper interactive use: the solver ships three MCP servers already registered
in ITS `.mcp.json` (`operator` = OP1–OP6 compute, `universe` = L0→L3 readouts,
`arc` = `coq_verify` live Coq compile + `arc_search` over 292 formal files +
`dec_compute` exact-rational DEC). Open a session at the solver repo (or add
its `.mcp.json` entries to yours) to call them directly.

## Hard rules

- Read `docs/AI_READING_GUIDE.md` + `v2/POSITION.md` before first use.
- The gates' PROMPT verdicts are questions for YOU — answer them explicitly,
  never silently skip.
- Toy scope must be declared in every AP file header (see `ap/ap2_fxt_amati.py`
  for the canonical family-scope caveat pattern).
- PRIVATE/PROPRIETARY: never publish lens/vendor or this repo's content
  externally without founder approval.
