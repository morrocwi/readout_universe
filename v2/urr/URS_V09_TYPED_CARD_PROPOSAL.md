# URS–RDT v0.9 Information-Native — assessment, and why the card needs a type

Assessed by the orchestrator, 2026-07-21, by running the supplied code and checking every
number against physics.

## 1. What v0.9 gets right, and it is the answer to a question asked earlier today

Earlier in this session the founder asked for *"an equation that needs no physical adapter at
all, except a card saying what each variable means in that domain."* v0.9 is that architecture,
built: the native layer carries exactly one unit,

    1 RD := one retained-distinction record

and joule, eV, volt, mole, metre and second appear **only** in a calibration map applied to the
final answer. I grepped the solver for physical units outside the calibration/decoder functions
and found none — the claim holds as stated. 3/3 tests pass.

The sharpest sentence in v0.9 is `RD ≠ bit ≠ joule` until a calibration map is declared, because
one distinction has no fixed energy content. That is the correct generalisation of what this
session established piecemeal: `M` is a card entry because it fixes what *retained* means, `K`
is a card entry because it is the unit of distinction. v0.9 gives both a home and a type.

## 2. The worked example is physically correct — verified independently

| quantity | reported | checked |
|---|---|---|
| photons per O₂ | 8 RD | Z-scheme: 2 H₂O → 4 e⁻, each excited twice (PSII + PSI) → 8. Textbook theoretical minimum; measured ~9–10 |
| optical energy | 1387.266 kJ/mol | 4×680 nm + 4×700 nm gives **1387.261** — matches to 5 decimals, so the map uses PSII at 680 and PSI at 700 |
| chemical work | 474.322 kJ/mol | ΔG(glucose)/6 ≈ 478; consistent |
| efficiency | 34.19% | 474.322/1387.266 = 34.19% ✓ |

Nothing here is fudged. The arithmetic and the biology both check out.

## 3. But the counting result is recovered, not discovered

The 8 : 1 answer follows entirely from the stoichiometry — four oxidising equivalents, two
photosystems each. **Any** bookkeeping that counts 4 lineages × 2 excitations returns 8. So the
RD layer *reproduces* a textbook number, which is a consistency check on the representation,
not a new result. That is exactly the right thing to demonstrate at this stage and should be
described as such: the point is that the native layer can carry the computation in one unit,
not that it found something new.

## 4. The finding that matters: the card is currently allowed to contain physics

`urs_information_native_photosynthesis.py` lines 51–52:

    psii_wavelength_m = 680e-9
    psi_wavelength_m  = 700e-9

Those are not unit conversions. They are **empirical facts about chlorophyll** — which pigment
absorbs where — sitting inside the "calibration map". Likewise ΔG(glucose) in the chemical-work
decoder.

So the architecture's headline — *no physical adapter, only a card* — is true only if the card
may contain arbitrary physical content. And if it may, then **"adapter-free" has been achieved
by renaming the adapter to "card"**. The distinction only has teeth if the card is constrained.

## 5. Proposal: type the card

Split card entries into two kinds, labelled differently, because they carry completely different
risk:

**Type U — unit / convention.** A declaration with no empirical content. Wrong only if
inconsistent. Examples from this session: `K` (the unit of distinction, since `forced_into_DW_minus_W`
fixes L_R's *form* and never its scale); `M` (which meaning of *retained* is intended —
forgetting versus returning); the choice of what quantity `ρ` conserves.
**Nothing measured can falsify a Type U entry.**

**Type P — physical content.** An empirical claim imported into the map. Wrong if the world is
otherwise. Examples here: 680 nm, 700 nm, ΔG(glucose) = 2870 kJ/mol.
**Every Type P entry is a falsifiable borrow and needs a citation, exactly like any other
borrowed equation** (this project's own kinship rule).

The payoff is immediate and checkable: for the photosynthesis run, the native layer is Type U
throughout and the entire empirical exposure sits in three Type P numbers. That is a genuinely
strong claim — *the empirical surface of this calculation is three numbers* — and it is far
more defensible than "no adapter", because it is true and it is auditable.

It also predicts where errors will come from. A Type U mistake shows up as an internal
inconsistency the exact-quotient gate can catch. A Type P mistake shows up only against
experiment, and no amount of internal auditing will find it.

## 6. Recommendation

Adopt v0.9's single-unit native layer — it delivers what was asked for and the demonstration is
sound. But require every calibration map to declare its entries as **U** or **P**, with
citations mandatory on P. Without that, the card is an adapter with a better name; with it, the
claim becomes precise, small, and true.
