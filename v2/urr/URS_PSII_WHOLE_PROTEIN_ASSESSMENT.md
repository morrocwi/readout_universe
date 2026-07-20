# Whole-PSII no-Hamiltonian solve — assessment

Assessed by the orchestrator, 2026-07-21, by re-running the solver and adding the two null
tests the report did not run.

## 1. What reproduces exactly, and what genuinely holds

Ran the solver on the supplied experimental XFEL structures (8EZ5 S₃-rich 2.09 Å → 8F4K S₀-rich
200 ms 2.16 Å). Every number reproduces:

| quantity | value |
|---|---:|
| common residue RD | 5,302 |
| contacts S₃ / S₀ | 27,660 / 27,665 |
| stable / lost / gained | 27,441 / 219 / 224 |
| stable fraction | 0.98411 |
| Cα RMSD | 0.1305 Å |
| median \|Δr\| | 0.0851 Å |

3/3 tests pass. The architectural claims hold on inspection: no Hamiltonian, no force field, no
MD, no synthetic coordinates; Ångström appears only in the encoder and the final decoder; the
native state carries RD alone. **This is real experimental data, and that matters — it is the
first URS application not run on a model the author constructed.**

The **98.41% stable fraction is robust.** It is dominated by a large stable core and is
insensitive to the threshold effects discussed below.

## 2. Null test 1 — the 443 changed contacts are at noise level

The report treats 219 lost + 224 gained = 443 contact changes as the signal. But the whole
observed motion is Cα RMSD 0.1305 Å with median displacement 0.0851 Å — at or below the
coordinate uncertainty of a 2.1 Å structure. Contacts sitting near the 8 Å cut will flip on
noise alone. The report notes threshold caution but never tests it.

So I perturbed the S₃ coordinates by random displacement of matched magnitude and counted flips:

| injected noise (median \|Δr\|) | contacts changed | as % of the 443 observed |
|---|---:|---:|
| 0.0445 Å | 233 | 53% |
| **0.0750 Å** | **369** | **83%** |
| 0.1148 Å | 584 | 132% |
| 0.1786 Å | 872 | 197% |

**Random displacement of the same size as the observed motion reproduces most of the contact
change.** The 443 changes are not established as distinguishable from threshold noise.

## 3. Null test 2 — there is no gradient from the OEC

The report's central interpretation is that a distinction current spreads from the OEC through
the contact graph into the rest of the protein. The raw per-shell histogram of changed residues
does look like a spreading wave: 27, 40, 63, 81, 88, 98, 88, 74, 61 …

But that is the shape of the **residue population** per shell, not of the change. Normalising by
how many residues sit at each graph distance:

| graph steps from OEC | residues | changed | fraction |
|---:|---:|---:|---:|
| 0 | 156 | 27 | 17.3% |
| 1 | 229 | 40 | 17.5% |
| 2 | 360 | 63 | 17.5% |
| 3 | 450 | 81 | 18.0% |
| 4 | 521 | 88 | 16.9% |
| 5 | 660 | 98 | 14.8% |
| 6 | 667 | 88 | 13.2% |
| 7 | 577 | 74 | 12.8% |
| 8 | 469 | 61 | 13.0% |
| 9 | 404 | 54 | 13.4% |
| 10 | 294 | 55 | 18.7% |
| 11–15 | 515 | 81 | 12.5–23.1% |
| **whole protein** | **5,302** | **810** | **15.3%** |

**Flat.** 17.3% adjacent to the OEC against 15.3% protein-wide, wandering without trend. There
is no gradient, so there is no evidence here of a current propagating outward from the OEC.

This is a base-rate error, and it is the reason the raw histogram is persuasive when the
underlying fraction is not. It is exactly the shape of mistake that makes a null result look
like a discovery.

## 4. What must be withdrawn, and what stands

**Withdraw:** the claim that a distinction current spreads from the OEC through the contact
graph to other layers of the protein. It is not supported by this data, and the null test above
shows why. Also withdraw any reading of the 443 changed contacts as measured structural change
until they are shown to exceed coordinate error.

**Keep:**
- the architecture demonstration — whole protein carried in one unit, no Hamiltonian, Å confined
  to encoder and decoder. That claim is about the representation and it is fully met.
- 98.41% retention, which is robust and is itself the interesting biophysical statement: the
  complex is *not* rebuilt across the S-state transition.
- the honest boundary already in the report: this solves structural information flow, not
  energies or rates, and both deposited states are S-state population mixtures.

## 5. What would make the current claim real

The test is available and cheap. Repeat the analysis with (a) a contact definition that is not a
hard threshold — a smooth weight, or a distance-change criterion instead of a crossing
criterion; (b) the deposited coordinate uncertainties, so each contact change carries a
significance; and (c) the same procedure applied to two structures known *not* to differ (two
refinements of the same state, or the two protomers of the dimer) as a negative control. If the
OEC-shell fraction rises above the protein-wide baseline under those conditions, the current is
real and now measured. If it stays flat, the honest result is that whole-complex Cα contact
topology does not resolve the S-state transition — which is a publishable negative and a
genuine constraint on what this method can see.
