from copy import deepcopy

import pytest

from native_logic.kernel import (
    Atom,
    ClaimIR,
    ClaimValidationError,
    Tier,
    Verdict,
    atom_unifies,
    is_variable,
    solve_claim,
    unescape_literal,
)


BASE = {
    "claim_id": "test-claim",
    "question": "Does the agent have bounded freedom?",
    "scope": "one retained step",

    "translation": [
        {
            "foreign_term": "freedom",
            "native_term": "bounded policy freedom",
            "tier": "definition",
            "bridge_class": "native_definition",
        }
    ],

    "ontology_generable": True,

    "premises": [
        {
            "atom": {
                "predicate": "alternatives",
                "arguments": ["agent", "t1"],
            },
            "tier": "Dr",
            "source": "test",
        },
        {
            "atom": {
                "predicate": "accessible",
                "arguments": ["agent", "t1"],
            },
            "tier": "Dr",
            "source": "test",
        },
        {
            "atom": {
                "predicate": "selects",
                "arguments": ["agent", "t1"],
            },
            "tier": "definition",
            "source": "test",
        },
    ],

    "rules": [
        {
            "id": "R1",
            "antecedents": [
                {
                    "predicate": "alternatives",
                    "arguments": ["?a", "?t"],
                },
                {
                    "predicate": "accessible",
                    "arguments": ["?a", "?t"],
                },
                {
                    "predicate": "selects",
                    "arguments": ["?a", "?t"],
                },
            ],
            "consequent": {
                "predicate": "bounded_freedom",
                "arguments": ["?a", "?t"],
            },
            "tier": "Dr",
            "source": "native rule",
        }
    ],

    "target": {
        "predicate": "bounded_freedom",
        "arguments": ["agent", "t1"],
    },

    "context": {
        "candidate_distinctions": ["a", "b"],
        "grammar_compatible": True,

        "required_retained": ["a", "b"],
        "retained": ["a", "b"],

        "required_accessible": ["a", "b"],
        "accessible": ["a", "b"],

        "metric_nonnegative": True,
        "identity_lock_ok": True,
        "declared_obstruction": False,

        "lens_ok": True,
        "lens_distortion": 0.0,
        "lens_tolerance": 0.1,
    },

    "falsifier": "Produce bounded freedom without the required conditions.",
    "not_checked": [],
}


def solve(data):
    return solve_claim(ClaimIR.from_dict(data))


def test_positive_control_derives_target_as_dr():
    result = solve(deepcopy(BASE))

    assert result.derived is True
    assert result.verdict == Verdict.SUPPORTED_AS_DR
    assert result.tier == Tier.DR
    assert all(g.type_p for g in result.gates)
    assert all(g.status.value == "PASS" for g in result.gates)


def test_a1_negative_control_dissolves_no_distinction():
    data = deepcopy(BASE)
    data["context"]["candidate_distinctions"] = ["same", "same"]

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.DISSOLVED
    assert result.gates[0].status.value == "FAIL"


def test_a4_negative_control_is_underdetermined():
    data = deepcopy(BASE)
    data["context"]["accessible"] = ["a"]

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.UNDERDETERMINED


def test_a7_contradiction_does_not_explode():
    data = deepcopy(BASE)

    data["premises"].append(
        {
            "atom": {
                "predicate": "accessible",
                "arguments": ["agent", "t1"],
                "negated": True,
            },
            "tier": "Dr",
            "source": "contradictory test fact",
        }
    )

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.OBSTRUCTED
    assert "fact and negation" in result.explanation.lower()


def test_non_rd_generable_question_is_dissolved():
    data = deepcopy(BASE)
    data["ontology_generable"] = False

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.DISSOLVED
    assert result.gates == []


def test_missing_rule_chain_returns_open():
    data = deepcopy(BASE)
    data["rules"] = []

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.OPEN
    assert result.tier == Tier.OPEN


def test_open_load_bearing_rule_caps_conclusion_open():
    data = deepcopy(BASE)
    data["rules"][0]["tier"] = "Open"

    result = solve(data)

    assert result.derived is True
    assert result.verdict == Verdict.OPEN
    assert result.tier == Tier.OPEN


def test_lens_distortion_blocks_inference():
    data = deepcopy(BASE)
    data["context"]["lens_distortion"] = 0.5
    data["context"]["lens_tolerance"] = 0.1

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.OBSTRUCTED


def test_a7_catches_contradiction_derived_purely_by_rules():
    """
    A7 must not be a pre-chain-only snapshot. A rule chain can derive
    an atom and its negation with no contradiction present in the raw
    premises; a further rule can then use both as antecedents and
    "derive" an arbitrary target (ex falso quodlibet). The kernel must
    refuse to certify this, not report all-gates-PASS/SUPPORTED_AS_DR.
    """
    data = deepcopy(BASE)

    data["rules"] = [
        {
            "id": "R-MID-POS",
            "antecedents": [
                {"predicate": "alternatives", "arguments": ["?a", "?t"]},
            ],
            "consequent": {"predicate": "mid", "arguments": ["?a", "?t"]},
            "tier": "Dr",
            "source": "test",
        },
        {
            "id": "R-MID-NEG",
            "antecedents": [
                {"predicate": "alternatives", "arguments": ["?a", "?t"]},
            ],
            "consequent": {
                "predicate": "mid",
                "arguments": ["?a", "?t"],
                "negated": True,
            },
            "tier": "Dr",
            "source": "test",
        },
        {
            "id": "R-EXFALSO",
            "antecedents": [
                {"predicate": "mid", "arguments": ["?a", "?t"]},
                {
                    "predicate": "mid",
                    "arguments": ["?a", "?t"],
                    "negated": True,
                },
            ],
            "consequent": {
                "predicate": "bounded_freedom",
                "arguments": ["?a", "?t"],
            },
            "tier": "Dr",
            "source": "test",
        },
    ]

    result = solve(data)

    assert result.derived is False
    assert result.verdict == Verdict.OBSTRUCTED
    a7 = [g for g in result.gates if g.gate_id == "RAR-A7"][0]
    assert a7.status.value == "FAIL"
    assert "derived via rule chain" in " ".join(a7.evidence).lower()


def test_rule_with_unbound_consequent_variable_is_rejected():
    """
    A consequent variable that no antecedent binds must not silently
    become a literal placeholder string in a derived fact.
    """
    data = deepcopy(BASE)

    data["rules"][0]["consequent"]["arguments"] = ["?a", "?unbound"]

    with pytest.raises(ClaimValidationError) as excinfo:
        solve(data)

    assert "unbound" in str(excinfo.value) or "?unbound" in str(
        excinfo.value
    )


def test_rar_bridge_ceiling_caps_a_formally_closed_chain_at_dr():
    """
    Even a fully Th_coqc-tiered, formally-closed premise/rule chain
    must resolve no higher than Dr, because the RAR gates themselves
    are declared philosophical bridges. This pins Verdict.DERIVED's
    unreachability through solve_claim as intentional and tested,
    not an accidental side effect of GateSpec.tier defaults.
    """
    data = deepcopy(BASE)

    data["premises"] = [
        {
            "atom": {"predicate": "seed", "arguments": ["agent", "t1"]},
            "tier": "Ax",
            "source": "test",
            "formal_closed": True,
        }
    ]
    data["rules"] = [
        {
            "id": "R1",
            "antecedents": [
                {"predicate": "seed", "arguments": ["?a", "?t"]},
            ],
            "consequent": {
                "predicate": "bounded_freedom",
                "arguments": ["?a", "?t"],
            },
            "tier": "Th_coqc",
            "source": "test",
            "formal_closed": True,
        }
    ]

    result = solve(data)

    assert result.derived is True
    assert result.tier == Tier.DR
    assert result.verdict == Verdict.SUPPORTED_AS_DR
    assert "ceiled" in result.explanation.lower()


def test_is_variable_distinguishes_plain_from_escaped_leading_question_mark():
    assert is_variable("?a") is True
    assert is_variable("??a") is False
    assert is_variable("plain") is False
    assert is_variable("??") is False


def test_unescape_literal_undoes_the_double_prefix_only():
    assert unescape_literal("??foo") == "?foo"
    assert unescape_literal("plain") == "plain"
    assert unescape_literal("?a") == "?a"


def test_atom_unifies_treats_escaped_literal_as_ground_not_variable():
    pattern = Atom("p", ("??foo",))
    matching_fact = Atom("p", ("??foo",))
    different_fact = Atom("p", ("?foo",))

    assert atom_unifies(pattern, matching_fact, {}) == {}
    assert atom_unifies(pattern, different_fact, {}) is None


def test_atom_unifies_binds_a_variable_to_an_escaped_literal_value_unchanged():
    pattern = Atom("p", ("?x",))
    fact = Atom("p", ("??foo",))

    substitution = atom_unifies(pattern, fact, {})

    assert substitution == {"?x": "??foo"}
    # The bound value stays in canonical escaped form -- round-tripping it
    # through instantiate() into a new atom must not re-decode it, so a
    # later re-match of that derived atom against another pattern still
    # sees the escaped form consistently, not a variable-looking "?foo".
    derived = Atom("q", ("?x",)).instantiate(substitution)
    assert derived.arguments == ("??foo",)
    assert is_variable(derived.arguments[0]) is False
    # unescape_literal is the display-only inverse, applied once at the
    # boundary when a human-readable value is actually wanted.
    assert unescape_literal(substitution["?x"]) == "?foo"
