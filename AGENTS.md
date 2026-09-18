# AGENTS.md - readout_universe

## What this repository is

Readout Universe is "A Philosophy and Logic for Grounding Claims": a small, machine-checkable
vocabulary (a "tier" per claim) plus a worked textbook and companion tools that use it throughout.
The governing stance is readout-not-truth: every claim this repository makes is tagged with a tier and
never allowed to collapse into a stronger one than its evidence supports. The v1.0 book (`main.tex`)
is frozen; v2.0-dev stays a candidacy, never a declared Theory of Everything, and only adds to v1.0.
Non-claims: `README.md`, "We do NOT claim" (e.g. it does not claim Goedel, the Liar, or ethics are solved).

## Read first

1. `README.md` - scope, principles, the "For AI readers" entry order, and "We do NOT claim".
2. `docs/AI_READING_GUIDE.md` - entry order, tier discipline, and what this book does not claim.
3. `philosophy.md` - the distilled epistemology and ontology, with a ledger of what is not claimed.
4. `claims.md` - one falsifiable claim per row, each with its own check command.

Loadable form of the tier discipline: `plugins/readout-universe/skills/readout-universe/SKILL.md`.

## Rules

- Tier discipline, never collapse: `Th_coqc`, `finite_diagnostic`, `Dr`, `Open`, `fit_calibrated`,
  `definition`. The README legend is a summary; if it and the legend in `logic.md` disagree, `logic.md` wins.
- No number enters the documentation without an executed run behind it (`docs/VERIFIED_RUNS.md`).
- v1.0 is frozen; v2 only adds and never silently edits what came before.
- `make verify` reproduces only the `Th_coqc` / `finite_diagnostic` slice; `Dr` / `Open` /
  `fit_calibrated` claims are read and audited, not run.
- Licence: MIT, except twelve named files under `ap/` that remain in the repository for
  provenance/context but are excluded from the MIT grant and remain all-rights-reserved. See the
  "PROPRIETARY EXCEPTIONS" section of `LICENSE` for the exact file list and terms.

## Programme map

This repository is one node of the Human-AI Readout Programme. Which repository answers which kind of
question, what to read first and which gate applies is kept in one place, the routing hub:
<https://github.com/morrocwi/main.hub> (start at its `AGENTS.md`, then `ROUTES.md`).
The hub holds pointers and pinned links only. It is a readout of one moment: when the hub and this
repository disagree, this repository wins.
