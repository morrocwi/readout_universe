"""Bridge/adapter between omega.claim_ir.Claim and native_logic.kernel.ClaimIR.

These two shapes serve different purposes and this module does not pretend
otherwise:

  - omega.claim_ir.Claim is ONE tier-audited claim record produced by a
    translation/bridge-audit pass (omega/gates.py::step1_translate,
    step4_bridge_audit). It carries a tier and bridge_class that were
    already decided by that pass -- this module never re-derives or
    upgrades them.

  - native_logic.kernel.ClaimIR is a full (Gamma, phi) proof-kernel input:
    a premise set, a rule set, a target atom, and RAR gate context
    (native_logic.kernel.GateContext) that decides whether the eight RAR
    gates (A1..A8) pass. None of that is present on an omega.Claim -- the
    target atom, the gate context, and the falsifier are proof-kernel-
    specific concerns that only the caller (who knows what question is
    being put to the kernel) can supply honestly.

So `omega_claims_to_native_ir` does exactly one thing: it turns a list of
omega.Claim into native_logic Facts (one per Claim, tier and bridge_class
carried over verbatim -- never upgraded, never invented) and a minimal
translation table derived from those same claims, and it REQUIRES the
target atom, the RAR gate context, and the falsifier as explicit arguments.
It never fabricates a default for any of those three -- a fabricated
default there would silently decide gate PASS/FAIL (RAR-A1..A8 all read
straight off `context`) or silently decide what the kernel is even being
asked to prove (`target`), which is exactly the kind of silent tier/verdict
laundering this whole codebase's tier discipline exists to prevent.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from omega.claim_ir import Claim

from .kernel import (
    Atom,
    ClaimIR,
    Fact,
    GateContext,
    Rule,
    Tier,
    TranslationTerm,
)

# The set of tier strings native_logic.kernel.Tier can actually represent.
# omega.schemas.TIER_TAGS is NOT a subset of this: omega has "fit_calibrated"
# and native_logic does not. We never map "fit_calibrated" onto some nearby
# native tier by guesswork -- that would be exactly the silent-upgrade
# omega/claim_ir.py's own docstring forbids, just committed on this side of
# the boundary instead. An omega.Claim carrying a tier native_logic cannot
# represent must fail loudly, not be coerced.
_NATIVE_TIER_VALUES = {tier.value for tier in Tier}

# bridge_class has no dedicated field on native_logic.kernel.Fact /
# TranslationTerm carries it as a bare str, but Fact does not have a
# bridge_class slot at all. We carry it over verbatim by folding it into
# the Fact's `source` string (the one free-text field Fact has) rather than
# dropping it -- "carried over verbatim" means the value survives the
# crossing intact and inspectable, not that we invent a new schema field
# for it on this side.


def _native_tier(tier: str, *, where: str) -> Tier:
    if tier not in _NATIVE_TIER_VALUES:
        raise ValueError(
            f"omega Claim tier {tier!r} ({where}) has no representation in "
            f"native_logic.kernel.Tier {sorted(_NATIVE_TIER_VALUES)!r} -- "
            "refusing to guess a mapping (that would silently upgrade or "
            "downgrade the claim across the omega -> native_logic boundary)."
        )
    return Tier(tier)


def _fact_source(claim: Claim) -> str:
    """Build the Fact.source string for one omega.Claim.

    Encodes claim id, bridge_class (verbatim, or "None" if the claim carried
    none), and dependencies so a reader of the resulting ClaimIR can trace a
    Fact back to the exact omega.Claim it came from without this adapter
    inventing a new schema field to hold that information.
    """

    deps = ",".join(claim.dependencies) if claim.dependencies else "none"
    return (
        f"omega:{claim.id}"
        f"|predicate={claim.predicate}"
        f"|bridge_class={claim.bridge_class}"
        f"|dependencies={deps}"
    )


def _claim_to_fact(claim: Claim) -> Fact:
    """One Fact per omega.Claim. Tier is carried over verbatim -- this
    function performs no upgrade, no downgrade, and no re-audit; the tier
    was already decided by omega/gates.py and arrives on `claim.tier`.
    """

    atom = Atom(
        predicate=claim.predicate,
        arguments=tuple(str(a) for a in claim.arguments),
        negated=False,
    )
    tier = _native_tier(claim.tier, where=f"claim {claim.id!r}")

    return Fact(
        atom=atom,
        tier=tier,
        source=_fact_source(claim),
        # omega.Claim carries no notion of "formally closed" (Coq-checked
        # closure of the derivation). Defaulting to False rather than True
        # is the conservative, non-fabricating choice: an unknown closure
        # status must never be read by the kernel as "closed", since
        # Fact.formal_closed feeds cap_tier()/forward_chain() and a wrong
        # True here could let a conclusion keep Th_coqc it never earned.
        formal_closed=False,
        load_bearing=True,
    )


def _claim_to_translation_term(claim: Claim) -> TranslationTerm:
    """One minimal TranslationTerm per omega.Claim, built only from fields
    the Claim actually carries -- no invented native_term when the source
    claim has none.
    """

    tier = _native_tier(claim.tier, where=f"claim {claim.id!r} (translation)")
    bridge_class = claim.bridge_class if claim.bridge_class is not None else "OPEN"

    if claim.predicate == "TRANSLATED" and len(claim.arguments) >= 2:
        foreign_term = str(claim.arguments[0])
        native_term = str(claim.arguments[1])
    elif claim.arguments:
        # NO_DICTIONARY_ENTRY, BRIDGE, or any other predicate: the claim
        # names exactly one term and does not assert a distinct native
        # rendering of it. Using the same string for both sides (instead of
        # inventing a translation the claim never made) keeps this honest.
        foreign_term = str(claim.arguments[0])
        native_term = str(claim.arguments[0])
    else:
        foreign_term = claim.id
        native_term = claim.id

    return TranslationTerm(
        foreign_term=foreign_term,
        native_term=native_term,
        tier=tier,
        bridge_class=bridge_class,
    )


def omega_claims_to_native_ir(
    claims: List[Claim],
    question: str,
    target_predicate: str,
    context: Dict[str, Any],
    *,
    falsifier: str,
    target_arguments: Sequence[str] = (),
    target_negated: bool = False,
    scope: str = "",
    claim_id: str = "",
    rules: Optional[List[Rule]] = None,
    ontology_generable: bool = True,
    not_checked: Optional[List[str]] = None,
) -> ClaimIR:
    """Convert a list of omega.claim_ir.Claim into one native_logic ClaimIR.

    Required, no-default arguments (do not call this with fabricated
    stand-ins for these -- they decide the kernel's PASS/FAIL, not this
    adapter):

      target_predicate / target_arguments / target_negated
          -- together they ARE the target atom (Gamma |- phi's phi).
             omega.Claim has no notion of "what is being proven"; only the
             caller putting a question to the proof kernel knows that.
      context
          -- a dict shaped like native_logic.kernel.GateContext's fields
             (candidate_distinctions, grammar_compatible, required_retained,
             retained, required_accessible, accessible, metric_nonnegative,
             identity_lock_ok, declared_obstruction, lens_ok,
             lens_distortion, lens_tolerance). This directly decides RAR
             gates A1..A8 (run_rar_gates in kernel.py) -- fabricating any
             field here fabricates a gate result.
      falsifier
          -- the stated falsifier for this claim (ClaimIR.falsifier;
             validate_claim() requires it to be non-empty). omega.Claim
             carries no falsifier field, so there is no source value to
             carry over -- only the caller can state it.

    What this function does NOT do:
      - It does not upgrade or downgrade any Claim.tier or Claim.bridge_class
        (see `_native_tier`, `_claim_to_fact`).
      - It does not invent rules. `rules` defaults to an empty list; pass
        the actual inference rules for the question being asked.
      - It does not decide ontology_generable from the claims; that is a
        proof-kernel-level judgement about the RD-generated ontology, not
        something an omega.Claim list implies. Default True is only a
        convenience for the common case; pass False explicitly when it's
        known false.

    Returns a native_logic.kernel.ClaimIR with:
      - premises: one Fact per input Claim (via `_claim_to_fact`).
      - translation: one TranslationTerm per input Claim (via
        `_claim_to_translation_term`) -- a minimal table, not a re-run of
        omega's own dictionary lookup.
    """

    if not question.strip():
        raise ValueError("omega_claims_to_native_ir: question must be non-empty")
    if not falsifier.strip():
        raise ValueError(
            "omega_claims_to_native_ir: falsifier is required and must be "
            "non-empty -- it is a proof-kernel concern omega.Claim does not "
            "carry, so it cannot be defaulted."
        )
    if not target_predicate.strip():
        raise ValueError(
            "omega_claims_to_native_ir: target_predicate is required -- the "
            "target atom is what the kernel is being asked to prove and "
            "cannot be inferred from the omega.Claim list."
        )

    premises = [_claim_to_fact(c) for c in claims]
    translation = [_claim_to_translation_term(c) for c in claims]

    target = Atom(
        predicate=target_predicate,
        arguments=tuple(str(a) for a in target_arguments),
        negated=target_negated,
    )

    gate_context = GateContext.from_dict(context)

    resolved_claim_id = claim_id or (
        "native:" + "-".join(question.strip().lower().split())[:60]
    )

    return ClaimIR(
        claim_id=resolved_claim_id,
        question=question,
        scope=scope,
        translation=translation,
        ontology_generable=ontology_generable,
        premises=premises,
        rules=list(rules) if rules is not None else [],
        target=target,
        context=gate_context,
        falsifier=falsifier,
        not_checked=list(not_checked) if not_checked is not None else [],
    )


__all__ = ["omega_claims_to_native_ir"]
