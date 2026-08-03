# Installing the Readout Universe Claude Code Skill

This repository ships a Claude Code plugin (`readout-universe`) via a
`.claude-plugin/marketplace.json` at the repo root, packaging the tier
discipline (`Th_coqc` / `finite_diagnostic` / `Dr` / `Open` /
`fit_calibrated` / `definition`) as a loadable skill rather than requiring
you to clone the full repo and read files by hand.

**Verification note on the commands below:** the exact `/plugin`
sub-command syntax was cross-checked against this workstation's own local
plugin state (`~/.claude/plugins/known_marketplaces.json`,
`~/.claude/plugins/installed_plugins.json`) and the install instructions
published by two sibling marketplaces already installed here —
`yaoharee-lahtee-math` (`morrocwi/information-discrete-math`) and
`yaoharee-lahtee-skillme` (`morrocwi/skillme`), both of which use the same
`owner/repo` short form for `marketplace add`. This is a `finite_diagnostic`
check (local files read directly), not a `Th_coqc` one — no automated way to
execute the interactive `/plugin` command itself exists in this session, so
treat the syntax as verified-against-precedent, not verified-by-execution.

## Install

```
/plugin marketplace add morrocwi/readout_universe
/plugin install readout-universe@yaoharee-lahtee-readout
```

The first command registers this repository as a marketplace named
`yaoharee-lahtee-readout` (the name declared in
`.claude-plugin/marketplace.json`, not the repo name itself — that
distinction matters for the `install` line below). The second installs the
`readout-universe` plugin that marketplace publishes.

## Uninstall

```
/plugin uninstall readout-universe@yaoharee-lahtee-readout
```

Optionally, if you also want to drop the marketplace registration entirely
(e.g. no other plugin from this marketplace is in use):

```
/plugin marketplace remove yaoharee-lahtee-readout
```

## What loading the skill gets you

The skill is a **checklist for grounding claims**, not a substitute for the
book. Loading it puts the following in front of the model before it states
anything as settled:

- The **readout-not-truth** stance: treat any number, benchmark, or prior
  answer as a finite retained readout, not the thing-in-itself.
- The **six-tier vocabulary** for tagging exactly how well-supported a claim
  is — `Th_coqc` (machine-checked, axiom-free) / `finite_diagnostic`
  (executed numeric run) / `Dr` (declared-bridge / narrative reading) /
  `Open` (not established, but never bare — carries a stance and a
  falsifier) / `fit_calibrated` (fit to data, not derived) / `definition`
  (a stipulated object or gate) — and the discipline of never silently
  rounding a claim up to a stronger tier than its evidence supports.
- A prompt to say, plainly, whether a given statement was verified in front
  of you or is being relayed from a source, before presenting it as fact.

This is a **summary checklist**, not the full argument for any specific
theorem, equation, or paradox resolution in the corpus — it is meant to
change how claims get phrased, not to hand over the underlying derivations.

## Where to go for the full book/corpus

If the skill's summary isn't enough — you need the actual derivation, the
worked example, or the full tier legend with its edge cases — go to the
standalone reference documents this skill distills from, all in the repo
root:

- **[`../philosophy.md`](../philosophy.md)** — the epistemology and
  ontology in prose: why readout-not-truth, why the tier discipline, the
  Lens Law, the Position/Gate control layer, and an explicit ledger of what
  this system does **not** claim.
- **[`../logic.md`](../logic.md)** — the same territory as a pure
  equation/operator ledger, no narrative, every entry tagged with its
  source tier and a pointer back to the file with the full derivation.
  Canonical tier legend — if `logic.md` and any summary (including this
  file) ever disagree, `logic.md` wins.
- **[`../README.md`](../README.md)** — repository overview, "For AI
  readers" entry order, and how to reproduce the machine-checked core
  (`make verify`) yourself.
