# evidence/ — machine-checked Coq evidence, cloned and re-verified in place

> Rule: a `.v` file lives here ONLY if it re-compiles in THIS repo on this
> machine, with its axiom profile recorded un-softened. Provenance is declared;
> these are snapshots — the canonical development continues in the source repo.

| File | Provenance (canonical) | Snapshot date | What it proves |
|------|------------------------|---------------|----------------|
| `RD.v` | `research_universal_solver/formal/RD.v` | 2026-07-19 | The Information-DNA object stratum: RD1–RD9 as Inductive D + theorems (RD3/RD4), commutative semiring, total order, semiring+order isomorphism D ≅ ℕ, equational transfer RD↔PA (deep-embedded term language) |
| `URCF_RD_All.v` | `research_universal_solver/formal/URCF_RD_All.v` | 2026-07-19 | The consolidated URCF/RD verified foundations (≈678 Theorem/Lemma declarations) |
| `UPL_Sorites.v` | this repo, `code/UPL_Sorites.v` (v1.0) | — | the book's own formal floor (sorites core, monotone scope) — kept in `code/`, listed here for the inventory |
| `DRL_General_Legendre.v` | this repo (NEW 2026-07-19) | — | general-N Legendre D-cancellation: any nodes/heterogeneous/abstract graph+potential (covers H_nl), axiom-free, list induction |
| `DRL_Discrete.v` | this repo (NEW, ultracode 2026-07-19) | — | DRL: T1 EL-identity iff (damped/anti-damped), T2 Legendre D-cancellation, T3 leapfrog D=0 invariant — 3-ring scope; axioms: sig_forall_dec + functional_extensionality (declared) |

## Re-verification (executed 2026-07-19, Coq 8.20.1, this machine)

```
cd evidence && coqc RD.v && coqc URCF_RD_All.v    # both exit 0
```

**Axiom profile (from `Print Assumptions` output, recorded honestly):**

- The **discrete core** (RD object stratum: semiring, order, ℕ-isomorphism,
  PA-transfer; and the bulk of URCF_RD_All) reports
  `Closed under the global context` — **axiom-free**.
- **Some theorems are NOT axiom-free**: sections touching classical/ℝ readouts
  depend on `Classical_Prop.classic`, `FunctionalExtensionality.
  functional_extensionality_dep`, and `ClassicalDedekindReals.sig_forall_dec` /
  `sig_not_dec` (standard-library classical axioms).

**Doctrine note (`Dr`).** This split is not an embarrassment — it is the thesis
made visible in the proof assistant: the DNA-generated discrete core closes with
no borrowed axioms, while the continuum layer (ℝ as stratified readout,
ROM-Ω.8) *must* borrow classical axioms to exist. The axiom profile IS the
borrowed-vs-derived ledger, machine-generated.

## Citation rule

Citing a theorem from these files as `Th_coqc` requires: (a) it compiles here,
(b) its own `Print Assumptions` is clean OR the borrowed axioms are stated
alongside the citation. A bare "machine-checked" with hidden classical axioms is
an overclaim.
