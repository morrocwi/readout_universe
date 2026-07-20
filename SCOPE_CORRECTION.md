# Proposed PR title/body correction for PR #23 (NOT applied)

> This is a PROPOSAL ONLY. Nothing in this file has been applied to the
> live GitHub PR title or body. The founder should review and, if agreed,
> paste the text below into the PR manually (or ask an agent to do so via
> `gh pr edit`). No git/gh mutation was performed by the agent that wrote
> this file.

## Why a correction is proposed

The current PR title says AP19 "derives 2 and trace-square response 4"
and the body calls it "the sharpest remaining Paper III falsifier." Both
overstate what the file does:

- The repo's own frontier document `v2/MYSTERY_LADDER.md` names the
  (2s)^2 paramagnetic law as an Open item whose falsifier explicitly
  requires deriving it "จากโครงสร้าง channel บนกราฟ" (from the channel
  structure on the graph) using the repo's graph/spectral engine
  (AP9-AP12).
- AP19 does not use that engine. It is a standalone finite SU(2)
  Yang-Mills background-field toy computation -- real algebra, but a
  different, borrowed machinery (essentially the known Nielsen 1981 /
  't Hooft g=2 result for a non-Abelian gauge boson, already cited by
  kinship in AP11).
- The PR author already retracted the strong reading in a PR comment:
  > "its self-interaction unit is borrowed through the non-Abelian
  > curvature expansion. Do not treat or merge it as the foundational
  > closure."

That retraction is the correct, operative status. The proposed text below
makes the PR title/body match it.

---

## Proposed corrected title

> AP19: finite-diagnostic Yang-Mills toy -- self-interaction supplies one
> more curvature unit (multiplier 2, response 4); does NOT close the
> (2s)^2 graph-derivation falsifier

(Old title for comparison: "AP19: derive spin-1 curvature multiplier and
response power")

## Proposed corrected body

```
## What this is

A finite, seed-independent algebraic fact in a toy SU(2) adjoint
Yang-Mills model: the background-curvature x [a_x, a_y] self-interaction
term contributes exactly ONE more copy of the same curvature operator as
the linearized field-strength term, giving a multiplier of 2 and a
normalized trace-square response ratio of 4 (vector vs. spin-1/2). This
holds to ~1e-11 (numeric TOL) across many random backgrounds -- pinned in
the repo across seeds 1,2,3,4,5,7,42,100,999, and separately by a direct
test of the underlying so(3) Lie-homomorphism identity
[ad_u, ad_v] = ad_{u x v}, which is the actual reason the multiplier is
forced to be exactly 2 rather than fitted.

## What this is NOT

- NOT a derivation from this repo's graph/spectral engine (AP9-AP12).
  MYSTERY_LADDER.md's (2s)^2 open item explicitly requires the derivation
  to come "from the channel structure on the graph" -- AP19 does not
  touch that engine at all. This PR does not close that falsifier.
- NOT a from-scratch derivation of the non-Abelian curvature expansion or
  the Lie/commutator structure it uses -- that machinery is standard
  Yang-Mills background-field theory, already known (kinship: Nielsen
  1981 / 't Hooft g=2 result for a charged vector boson, already cited in
  AP11). This file borrows it, verifies the multiplier numerically, and
  is explicit about the borrowing in the module docstring.
- NOT independently cross-validated on normalization: the term weights
  (1/2, 1/2, 1 in background-Feynman gauge) were chosen with the known
  target (AP11's atom(2) = 11/3 = (2*1)^2 - 1/3) already in view, and
  have not been checked against a textbook background-field computation.
  This is a declared open item, not a hidden weakness -- the SHAPE of the
  result (two equal curvature units) is forced by the so(3) identity
  above; the absolute normalization is not independently confirmed.

## Author's own retraction (operative status)

Quoting the author's PR comment, which supersedes the original title/body
framing:

> "its self-interaction unit is borrowed through the non-Abelian curvature
> expansion. Do not treat or merge it as the foundational closure."

## Tests

7 tests in `ap/ap19_spin1_weizenbock.py`, including two added to pin the
genericity of the multiplier-2 result (multi-seed check) and the
so(3) Lie-homomorphism identity that is the actual mechanism. Full repo
suite: 73 passed.
```
