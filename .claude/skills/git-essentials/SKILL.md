---
name: git-essentials
description: Essential git workflow for readout_universe — load before any commit, push, rebase, or PR in this repo. Encodes the evidence-lives-on-the-branch rule (Gate Typing Law), re-verify-after-rebase from VERIFIED_RUNS, tier-tagged commit/PR language, and the plugin/marketplace versioning caveat.
---

# Git essentials — readout_universe

The core git-relevant law of this repo: **a claim's evidence must live on the branch that
carries the claim** — not in a PR description, a paper, a different repo, or a different
branch (`docs/GATE_TYPING_LAW.md`). Git discipline here is mostly about keeping evidence
and claim in the same tree.

## Evidence on the branch

- If a commit adds or strengthens a claim, the verifying artifact (script, gate output row
  in `docs/VERIFIED_RUNS.md`, test) goes in the **same branch, same PR** — ideally the same
  commit. A PR body is not evidence; the tree is.
- `docs/VERIFIED_RUNS.md` rows cite commands + exit codes actually run. Never append a row
  for a run you did not execute in this working tree.

## Re-verify after rebase (recorded precedent)

A verified state does not survive a rebase by assumption. Precedent in VERIFIED_RUNS: after
rebasing onto upstream commits pushed concurrently to the same branch, the verification
commands were **re-run** (`make verify-urr-coq` exit 0, `python3 -m pytest -q`) rather than
trusting the pre-rebase revision. Do the same: after any rebase/merge of a moving branch,
re-run the relevant verify commands before claiming green, and say so in the PR.

## Tier-tagged git language

Commits and PRs are claims. Tag them with the tier their evidence earns
(`Th_coqc` / `finite_diagnostic` / `Dr` / `Open` / `fit_calibrated` / `definition`) and
never round up — e.g. "syntax verified-against-precedent, not verified-by-execution"
(`docs/INSTALL_SKILL.md`) is the house style for honest limits. "CI green" is a
`finite_diagnostic` statement about one run, not a proof.

## Branch, push, PR mechanics

- Feature branch always; never push the default branch directly.
- `git fetch origin <branch>` for specific branches; `git push -u origin <branch>`; retry
  only network failures up to 4× with backoff (2s, 4s, 8s, 16s).
- After pushing, open a **draft PR** if none is open for the branch. PR body: commands run
  + exit codes, tier of each claim, and pointers to the in-branch evidence files.
- Merge only after review + green checks (precedent: solver PR merged "after adversarial
  audit APPROVE"). Never force-push a shared branch; when a branch is being rebased as it
  moves, re-run the checks rather than trusting a rev.

## Plugin/marketplace versioning

This repo ships a Claude Code plugin via `.claude-plugin/marketplace.json`
(`plugins/readout-universe/`). If a change touches the skill or plugin contents, bump the
plugin version in the same commit — the sibling repos' recorded failure mode is a plugin
version frozen while the repo moved on.
