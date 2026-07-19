# AI Reading Guide — Readout Universe (v1.0)

Purpose: let any AI agent load this philosophy-and-logic system correctly from git,
without collapsing its claim tiers or over-reading its scope.

## Reading order

1. **`main.tex`** front matter: "Open Science and Reproducibility Statement" and
   "How to Read This Book: The Reading Contract" — the binding contract for every
   reader, human or AI.
2. **Part I — The Root**: the third stance (logic neither eternal nor conventional),
   why logic must have a genesis, the primordial logic stream L-01…L-04.
3. **Part II — The Logic of the Finite Knower**: the engine Aε=δ read at the
   knower's τ_c; defeasibility (L-06); truth as tracking (L-07); classical logic as
   idealized projection (L-09); relocation of paradox — Sorites, Liar, the
   infinity-injection operator Ω_∞ (L-10); incompleteness as identifiability (L-11).
4. **Part III — Philosophy Re-read**: ontology, epistemology, mind, science
   (operator calculus), ethics (L-16), open frontier.
5. **Part IV — Dialogue with World Traditions**: Greece, India (Nyāya/Buddhist),
   China (Mohist), Islamic logic (Avicenna), Kant→Frege, the 20th century to now.
   Scope note: *dialogue*, not supersession.
6. **Part V — Method and Discipline**: the Ω_phil operator worked problems, the LTP
   battery + formal floor, claim discipline, open problems.
7. **Appendices**: executable LTP sources, the Coq formal floor, claims register,
   arrow ledger / borrowed-vs-derived / retractions, glossary.

## Tier discipline (mandatory — never collapse)

| Tier | Meaning | Where |
|------|---------|-------|
| `Th_coqc` | machine-checked, axiom-free theorem | `code/UPL_Sorites.v` (monotone-scope Sorites core only) |
| `finite_diagnostic` | verified numeric run — evidence, NOT proof | `code/LTP*.py` |
| `Dr` | declared-bridge reading — an interpretation with a named bridge | marked in text |
| `Open` | open problem — always carries a stance, never bare | marked in text |

Rules for an AI citing this book:
- Quote a claim only at its own tier. A `finite_diagnostic` PASS is never "proved".
- The Coq floor covers the monotone-g Sorites core ONLY; do not extend its scope.
- Every claim in `CLAIMS.md` has one check command; if you assert the claim, you
  should be able to point to an executed run (see `docs/VERIFIED_RUNS.md`).
- The "We do NOT claim" list in `README.md` binds you too: no Gödel/liar/ethics
  "solved", no B1 uniqueness, no supersession of any tradition.
- Output = retained readout, not truth. A correct readout is not a true theory.

## Verifying before citing

```
make verify
```

Expected: LTP1 `SUITE: PASS 3/3`; LTP2–4 `SUITE: PASS 8/8`; `coqc` exit 0 with
3× `Closed under the global context`. Log any new run in `docs/VERIFIED_RUNS.md`.

## Relation to the wider ANSE research system

This book is the philosophy/logic layer of the readout-not-truth research line
(spine / PGFT / research_universal_solver). Cross-repo references are declared
bridges (`Dr`), not identities: this repo stands alone and must verify alone.
