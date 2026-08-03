# readout-universe (Claude Code skill)

This plugin packages the **readout-not-truth** discipline from
[Readout Universe — A Philosophy and Logic for Grounding Claims](https://github.com/morrocwi/readout_universe)
as a Claude Code skill.

Once loaded, it gives an agent a small, machine-checkable tier vocabulary
(`Th_coqc`, `finite_diagnostic`, `Dr`, `Open`, `fit_calibrated`,
`definition`) for stating exactly how well-supported a claim is — a physics
result, a software metric, a benchmark number, a philosophical argument, or
the agent's own prior output — instead of quietly rounding it up to
"proven." The skill teaches the stance and the tier discipline directly; it
does not replace the source repository, which remains the canonical,
frozen-v1.0 / actively-developed-v2 text.

## What's in the box

The skill itself (`skills/readout-universe/SKILL.md`) is a compact
trigger-and-checklist file: when to load it, the one core commitment
(readout-not-truth), the tier table, a pre-write checklist, and pointers
back into the full corpus for depth. It deliberately does not duplicate
`philosophy.md`, `logic.md`, or `paradoxes.md` — those stay in the main
repository as the source of truth.

## Full corpus

For the full book, the equation/operator ledger, and the worked paradox
stress-tests, see the main repository:
<https://github.com/morrocwi/readout_universe>

- `philosophy.md` — the epistemology and ontology in prose.
- `logic.md` — the same territory as a pure equation/operator ledger.
- `paradoxes.md` — five classic paradoxes run through the machinery, with
  an honest scoreboard of what resolves, what merely reframes, and what
  stays `[Open]`.
- `main.pdf` / `main.tex` — the frozen v1.0 book.

## Install

This plugin is distributed via the `yaoharee-lahtee-readout` marketplace
declared at the repository root (`.claude-plugin/marketplace.json`). See
that marketplace's install instructions (`/plugin marketplace add …` →
`/plugin install readout-universe@yaoharee-lahtee-readout`) for the exact
command.

## License

MIT — see [`LICENSE`](LICENSE) in this directory, copied verbatim from the
repository root license, which covers the whole repository with no
exceptions.
