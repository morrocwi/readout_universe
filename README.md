# Readout Universe

**A Philosophy and Logic for Grounding Claims** — v1.0 → v2.0-dev

This project is for anyone who has to state a claim — a physics result, a
software metric, a philosophical argument — and wants a disciplined way to
say exactly how well-supported it is, instead of quietly rounding it up to
"proven." It gives you a small, machine-checkable vocabulary for that
(a "tier" per claim) plus a worked textbook and companion tools that use it
throughout. What you get out of it: a way to write claims that a skeptical
reader — human or another AI — can audit at a glance, and a concrete corpus
(theorems, code, five classic paradoxes) showing the method actually applied.

The governing stance is **readout-not-truth**: every claim this repository
makes is tagged with a tier (`Th_coqc`, `finite_diagnostic`, `Dr`, `Open`,
`fit_calibrated`, `definition`) and never allowed to collapse into a
stronger one than its evidence supports.

| | |
|---|---|
| **Author** | Yaoharee Lahtee ([ORCID 0009-0005-3861-0626](https://orcid.org/0009-0005-3861-0626)) |
| **Publisher** | Open Civil Science Initiative |
| **License** | Text (book, `philosophy.md`, `logic.md`, `paradoxes.md`, `v2/`): [CC BY 4.0](LICENSE) · `lens/`, `skill/`, `ap/` are proprietary — see LICENSE exceptions |
| **Status** | v1.0 book frozen (`main.tex`) · v2.0-dev in active development |

**Contents:** [What this repository is](#what-this-repository-is) ·
[Principles](#principles) · [For AI readers](#for-ai-readers--start-here) ·
[Reproduce every claim](#reproduce-every-claim-5-minutes) ·
[For AI operators — the APIs](#for-ai-operators--the-apis-v2) ·
[Repository layout](#repository-layout) ·
[We do NOT claim](#we-do-not-claim) · [Citation](#citation)

---

## What this repository is

The v1.0 book (`main.tex`, 83 pages, compiled in `main.pdf`) is a frozen,
complete text — no PDF extraction is needed to read it; the canonical
source is plain LaTeX in a single file.

v2.0-dev elevates the project's ambition — applying the same tier-honest
method across domains — while staying a candidacy, never a declared Theory
of Everything. Its governing rule is the **Lens Law** — every problem, from any domain, is
first *translated* into this book's information-philosophy language and
solved inside that translation (`v2/TRANSLATION_PROTOCOL.md`, the `Ω_all`
protocol), with bridges to the machine-checked physics/biology/AI corpus
recorded per-domain in `v2/DOMAIN_LEDGER.md` and release gates tracked in
`v2/ROADMAP_V2.md`. v1.0 is frozen; v2 only adds — it never silently edits
what came before.

Three distilled, standalone reference documents sit alongside the book,
each cross-linked to the other two and to the source `.md` files they
summarize:

- **[`philosophy.md`](philosophy.md)** — the epistemology and ontology in
  prose: why readout-not-truth, why the tier discipline, the Lens Law, the
  Position/Gate control layer, the ontological claim of one retained root,
  and an explicit ledger of what this system does **not** claim.
- **[`logic.md`](logic.md)** — the same territory as a pure equation/
  operator ledger: no narrative, every entry tagged with its source tier
  and a pointer back to the file that carries the full derivation.
- **[`paradoxes.md`](paradoxes.md)** — a worked stress-test: five classic
  paradoxes (Liar, Sorites, Ship of Theseus, Newcomb, Zeno) run directly
  through the machinery above, with an honest scoreboard of what actually
  resolves, what merely reframes, and what stays `[Open]`.

## Principles

1. **Position — a control layer, not a knowledge store.** Domain expertise
   is now a commodity; the real asset is the *operator that forces
   direction* — Gates G1–G13 force the right question, in the right order,
   and forbid drifting into a field's own blind spots (`v2/POSITION.md`).
2. **The Lens Law.** Every problem is translated into this book's
   information-philosophy language (Information DNA: `RD1`–`RD9` +
   `RAR A1`–`A8`) before it is solved — arguing in a foreign vocabulary past
   step 1 is disallowed (`v2/TRANSLATION_PROTOCOL.md`).
3. **Readout-not-truth, with a tier discipline that is enforced, not just
   declared.** Every claim carries `Th_coqc` / `finite_diagnostic` / `Dr` /
   `Open` / `fit_calibrated` / `definition`, and no number enters the
   documentation without an executed run standing behind it
   (`docs/VERIFIED_RUNS.md`); every change goes through adversarial review.
4. **Philosophy leads, equations follow — and closure claims are checked,
   narrowly.** The equations this lens has actually produced:
   - **Φ_FI** = `1 − V*(C∖π)/V*(C)` — the attribution fraction of
     inter-chain tension to a named posit (`v2/EQUATION_FI.md`, AP4).
   - **DRL** (Discrete Retention Lagrangian) — `RD4` forces a reader/record
     pair, from which a damping term can be derived from the action (Coq:
     an Euler–Lagrange iff at 3-ring, with two classical axioms declared
     over ℝ and axiom-free over ℚ in the solver's own formalization). The
     charge structure and D-cancellation close **axiom-free at general-N**
     (`DRL_General_Legendre.v` — a separate theorem, kept distinct), plus
     conservation of pairing across the whole nonlinear family
     (`v2/DISCRETE_RETENTION_LAGRANGIAN.md`, AP5/6/8). Imported into
     `research_universal_solver`'s own equation ledger, where the D-term
     was reclassified from a borrowed assumption to a narrowly-derived
     result after independent review (see that repo's own ledger/CHANGELOG
     for the audit trail; not reproduced here since it isn't publicly
     reachable from this repo).
   - **The tape layer** — an append-only record that realizes `RD4` in
     dynamics, plus a bridge `γ ↔ D/M` into DRL
     (`v2/APPEND_ONLY_RECORD.md`, AP7).
   - **Forced-Identification thesis** — a shared structural pattern across
     several live physics crises (`v2/FORCED_IDENTIFICATION.md`, n=4).
5. **Every new result is `[Open]` until it survives external, independent
   review.** Kinship to prior work is always disclosed (Bateman, CTP,
   collision models, and others), and a falsifier is attached to every
   claim, in the file that states it.

## For AI readers — start here

1. **[`docs/AI_READING_GUIDE.md`](docs/AI_READING_GUIDE.md)** — entry order,
   tier discipline, and what this book does not claim.
2. **[`philosophy.md`](philosophy.md)** and **[`logic.md`](logic.md)** — the
   distilled, standalone core (fastest path to the whole system).
3. **[`main.tex`](main.tex)** — the full textbook, plain LaTeX, one file.
4. **[`claims.md`](claims.md)** — one falsifiable claim per row, each with
   its own check command.
5. **[`paradoxes.md`](paradoxes.md)** — see the machinery actually applied
   to hard problems, honestly scored.

**Tier legend (never collapse), the six most common tags:** `Th_coqc`
(machine-checked, axiom-free) ≠ `finite_diagnostic` (executed numeric run —
evidence, not proof) ≠ `Dr` (declared-bridge / narrative reading) ≠ `Open`
(not established, but never bare — always carries a stance and a falsifier)
≠ `fit_calibrated` (fit to data, not derived) ≠ `definition` (a stipulated
object or gate). **This is a summary, not the full set** — [`logic.md`'s
legend](logic.md#0-the-root) is canonical and also defines `Ax`, `Th`, and
`exact_algebra`, which appear in its ledger tables; if the two ever
disagree, `logic.md` wins.

## Reproduce every claim (~5 minutes)

```sh
make verify   # LTP1 (expect PASS 3/3), LTP2-4 (expect PASS 8/8),
              # coqc UPL_Sorites.v (expect exit 0 + 3x "Closed under the global context")
make pdf      # builds main.pdf from main.tex (pdflatex x2)
make all      # verify + pdf
```

**Requirements:** `make verify` needs Python 3 + NumPy and Coq (8.18+;
8.20.1 verified — see [`docs/VERIFIED_RUNS.md`](docs/VERIFIED_RUNS.md));
`make pdf` needs a TeX Live distribution (`pdflatex`). The pytest suite
(`ap/`, exercised via `lens/`) additionally needs SciPy and SymPy — see
[`requirements.txt`](requirements.txt) for exact version pins, and run it
with `python3 -m pytest -q`.

Found a genuine falsification? That is this system working as designed —
please report it.


## Repository layout

```
main.tex, main.pdf        full textbook (canonical source + compiled, 83 pp.)
philosophy.md              distilled epistemology/ontology, standalone
logic.md                   distilled equation/operator ledger, standalone
paradoxes.md                worked stress-test against 5 classic paradoxes
claims.md                   falsifiable-claims register (C1-C7)
scope_correction.md         a recorded self-correction to an earlier scope claim
urr_native_system.md        entry point for the native URR-C calculation layer
EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md
                             root-to-Standard-Model equation stream (imported,
                             synced to the sibling repo's own canonical copy)
Makefile                    verify / pdf / all
.github/workflows/          CI: pins the verified Coq version, runs scripts/ci_verify.sh

code/                        Th_coqc + finite_diagnostic protocols (C1-C7)
  LTP1_logic_as_residual_flow.py     protocol 1 (C1-C3)
  LTP2_3_4_battery.py                 protocols 2-4 (C4-C6)
  UPL_Sorites.v                        formal floor, axiom-free (C7)
  UPL_Sorites_OneReversal.v            one-reversal extension (Th_coqc)

docs/                         AI_READING_GUIDE.md, VERIFIED_RUNS.md,
                              GATE_TYPING_LAW.md, handoffs/

v2/                            the lens doctrine + equations: Information DNA,
                              Lens Law, Doctrine of Quantity, Position, Phi_FI,
                              DRL, Append-Only Record, Forced-Identification,
                              Domain Ledger, Roadmap, urr/ (URR-C 0.4)


ap/                             executed case studies (pytest; AP0-AP21)
evidence/                       in-repo Coq evidence (RD.v, URCF_RD_All.v,
                                DRL_Discrete.v, DRL_General_Legendre.v)
gates/                          gate-typing support files
scripts/                        maintenance and build scripts
```


**Naming convention:** root-level primary documentation is lowercase
(`philosophy.md`, `logic.md`, `paradoxes.md`, `claims.md`,
`scope_correction.md`, `urr_native_system.md`); standard project metadata
files keep their conventional GitHub casing (`README.md`, `LICENSE`).
`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md` is the
one deliberate exception — its name is a cross-repository contract with
`readout_genesis` and `research_universal_solver`, both of which reference
it by this exact filename, so it is not renamed. Case-study files under
`ap/`, `code/`, and `v2/` follow their own subdirectory-local conventions
and are out of scope for this rule.

## We do NOT claim

- `finite_diagnostic` results are proof.
- The Coq floor extends beyond its stated monotone scope.
- Uniqueness of any B1-style structural claim.
- Gödel, the Liar, or ethics are solved.
- Supersession of any tradition discussed in Part IV of the book.
- Machine-independent timings for any executed run.

## Citation

```bibtex
@misc{lahtee_readout_universe,
  author       = {Lahtee, Yaoharee},
  title        = {Readout Universe: The Philosophy and Logic of Everything},
  year         = {2026},
  howpublished = {\url{https://github.com/morrocwi/readout_universe}},
  note         = {ORCID: 0009-0005-3861-0626. Open Civil Science Initiative.
                   v1.0 text under CC BY 4.0.}
}
```
