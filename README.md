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

## The lens as code + installable skill (v2)

- `lens/gates.py` — Ω_all G1–G8 forcing gates as a callable API (identifiability
  null-space, LTP3 load-bearing test, quantity-by-role guard, Ω_∞ screen) →
  produces the 7-piece `Extraction`; built ON `lens/vendor/` (snapshot of the
  verified operator/universe/lexicon engine, provenance in `lens/vendor/README.md`).
- `skill/readout-lens/` — Claude Code skill driving the W1–W7 issue workflow
  against the API. Install: `bash skill/install.sh [--global]`, details in
  `skill/INSTALL.md`. Verify: `python3 -m pytest -q`.

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
```

## We do NOT claim

`finite_diagnostic` = proof; Coq scope beyond monotone g; B1 uniqueness;
Gödel/liar/ethics solved; supersession of any tradition in Part IV;
machine-independent timings.
