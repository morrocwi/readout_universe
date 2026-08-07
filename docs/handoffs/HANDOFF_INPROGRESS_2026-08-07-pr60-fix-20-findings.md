# HANDOFF (in-progress, written BEFORE ultracode Workflow launch)
# Fixing all 20 confirmed adversarial-review findings on PR #60

**Written:** 2026-08-07, at the founder's request: "ultracode แก้ไข high
medium low ได้เลย" (fix all confirmed findings, ultracode/multi-agent).

## Context

PR #60 (`https://github.com/morrocwi/readout_universe/pull/60`, branch
`docs/embodied-affect-ethics-and-causal-ethics-bridge`, currently at
commit `ee39c8c`, NOT merged) added philosophy.md §7.25-7.32 and logic.md
ETH-7..14. A rigorous 6-dimension adversarial-review Workflow
(`wf_ce24be04-bbc`, run 2026-08-07) found **20 findings, all 20 confirmed**
by independent 3-way verification (0 refuted). Full finding text is in
this conversation's history and in
`/tmp/user/1000/claude-1000/-home-yaoharee-lt-ANSE-ASIA-readout-universe/1bda08e8-9dbe-49f1-ad82-c2e0f4d83c71/tasks/w216xbsh2.output`
(the raw workflow JSON result).

## The 20 findings (grouped for fixing — see conversation for full text of each)

**HIGH**
1. §7.27/§7.32 domain cards cite the WRONG line range for §8's `q_social`
   entry (point to the PR's own §7.27 text instead — the PR shifted all
   downstream line numbers by ~650 lines and the citation used stale
   numbers). Fix: find q_social's REAL current line number in the file as
   it now stands and correct both citations.
2. §7.26 "three sources converging on one shared form" overstates
   independence — `InfoDecisionAgency_attempt`'s cusp-fold is a direct
   Coq-formalization reusing BIRCA's own repair equation (disclosed at
   `research_universal_solver/docs/root/AGENCY_VS_AGENCY_LIKE.md` §6.3
   line 494, just past the cited 482-492 range) — only 2 of 3 sources are
   genuinely independent.
3. §7.25/§7.26 silently drop named BIRCA spec items the research pass
   itself identified: `autonomic_respiratory_connectors` (birca's
   `spec/birca_universal_skill.yaml` lines 378-417 — Berntson 1991,
   Task Force 1996/Eckberg 1983 HRV/RSA, Grodins 1954/Khoo 1991
   chemoreflex-CO2, Schafer 1998 cardiorespiratory coupling), allostatic
   burden (`SYSTEM_PROMPT.md` line 176, `README.md` line 113) — never
   mentioned anywhere in the merged text, not even honestly reported
   absent.

**MEDIUM**
4. §7.25 domain card: `PHASE_V_LIFE_AND_HEALTH` cited as "lines 179-193"
   but the block actually only spans 179-186; 187-193 is a DIFFERENT
   block (`PHASE_VI_PLURALITY`).
5. §7.28 open question 7 merges two DIFFERENT BIRCA evaluations
   (`birca/README.md` row 106 "15-item adversarial suite" vs. row 116
   "real-scenario spot-check v1.7.0-v1.7.1" — the LATTER caught the
   Claude Haiku 4.5 dropped-disclosure defect, not the former) into one
   described result.
6. §7.29 defines "CG" (Causal Grammar paper) and promises "every entry
   below names the specific CE/CG equation it draws on" — but no entry in
   §7.29-7.32 ever actually cites anything CG-specific; only CE is used.
7. §7.27 states BIRCA's calm-anchor theorem's Coq-verification status as
   flatly settled ("a machine-checked, axiom-free Coq theorem") with no
   hedge, while §7.26 (same underlying object) correctly hedges it as
   self-reported/unverified pending an actual `coqc`/`Print Assumptions`
   check. Inconsistent within the same PR.
8. §7.30's ETH-9 falsifier-shaping paragraph lets CE's own mechanism-
   content (not just its symbols) reshape this book's falsifier criterion,
   which the existing "not the same formalism" disclaimer doesn't cover.
9. §7.25: "feedback marker" is described as a literal instantiation of
   `dR_H/dt` ("a concrete, single-instance version of"), while
   "escalation threshold" one sentence later is correctly hedged
   ("structurally analogous to, though not derived from"). Inconsistent.
10. §7.27 silently skips "Level 2 (person)" in its own three-level framing
    (jumps I→III) with no sentence explaining the skip (reason: already
    covered by pre-existing §7.21 — state this explicitly).

**LOW**
11. §7.25 quotes genesis_canon L06 as `"personal, not failure"` in
    quotation marks as if verbatim — the source's English quote field for
    L06 is actually the formula; "personal, not failure" is the PR
    author's own translation of the Thai gloss. Mark as translation, not
    quote.
12. §7.25 same pattern for L03: `"not yet a diagnosis"` is a translation
    of the Thai gloss, not the source's marked English quote field.
13. §7.27 calm-anchor fence quote silently changes "it is NOT" (source)
    to "This is NOT" inside quotation marks. Fix to exact quote.
14. §7.27 L_H inter-agent quote truncates before "F#_H —" without an
    ellipsis mark, unlike this entry's own convention elsewhere.
15. §7.30 domain card presents CE-20/21/24 as "invoked equations" for
    Ch.14, but Ch.14's text never labels equations with explicit (CE-XX)
    tags the way Ch.9 does — these are the PR author's own inference.
    Soften the framing.
16. §7.31 domain card equation list omits CE-12/CE-13, which ARE
    explicitly listed as "Invoked equations" for §9.4 (Jim-type paradox)
    in the actual source — add them.
17. §7.27 "Level 1 (body)" paragraph has 4 of the founder's required 5
    parts but never states "what to add and where" for Level 1
    specifically (only the section's closing summary gestures at it
    vaguely). Add a concrete next step.
18. §7.26 taxonomy item (need/desire/drive/habit/value/compulsion) gets
    only a single clause, no "what to add and where" — the synthesis
    doc's own coverage-table row 320 already drafted one (a short
    taxonomy paragraph naming a distinguishing axis like
    object-directedness or persistence) that was never carried into the
    merged text. Add it.

## Workflow plan (about to launch)

Phase "Draft fixes" — parallel agents (~13), each covering one or a small
cluster of related findings above, each independently locating the CURRENT
exact text in `philosophy.md`/`logic.md` (do NOT trust old line numbers —
they may have shifted; use unique anchor-phrase greps), verifying against
the real source files, and returning structured `{file, old_string,
new_string, note}` edit(s) — NOT editing the file directly (avoids
parallel-agent file-corruption risk).

I (the orchestrator, outside the workflow) then apply every returned edit
myself, sequentially, verifying each `old_string` is unique in the file
before applying via the Edit tool, then re-check pipe/bold-marker parity
and cross-references, then run one more adversarial verification pass
(fork or workflow) before committing + pushing to the PR branch.

Run ID: **to be filled in immediately after launch.**

## What NOT to do

- Do not let workflow agents call Edit/Write on philosophy.md or logic.md
  directly — they only draft; I apply.
- Do not merge PR #60 without re-verifying all 20 findings are actually
  resolved.
- Do not silently drop the autonomic/allostatic content again (finding 3)
  — this was already identified once during research and dropped once
  during merge; verify it survives this time.

## LAUNCHED

Run ID: `wf_8c8bc226-cdd`. Script:
`/tmp/user/1000/claude-1000/-home-yaoharee-lt-ANSE-ASIA-readout-universe/1bda08e8-9dbe-49f1-ad82-c2e0f4d83c71/scratchpad/wf_pr60_fixdraft.js`.
13 parallel drafting agents (one per finding-cluster), each returns
structured {file, old_string, new_string, note} edits WITHOUT touching
the file. Next step once complete: apply every returned edit myself via
Edit tool (verify old_string uniqueness first), re-check formatting/
cross-refs, run one more adversarial verification pass, then commit+push
to the existing PR #60 branch (`docs/embodied-affect-ethics-and-causal-ethics-bridge`).
