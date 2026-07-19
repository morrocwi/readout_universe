"""AP0 -- executable checks for the lens gates API (lens/gates.py).

Each test pins a gate to the LTP battery case it descends from, so the code
layer stays anchored to the book's verified protocols.

Run: python3 -m pytest ap/ap0_lens_gates.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS block) -- do not publish.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lens import Issue, Quantity, run_gates
from lens.gates import (g2_infinity, g3_quantity_role, g5_identifiability,
                        g6_load_bearing, g7_readout_vs_readout)

# The LTP1/LTP3/LTP4 grammar (3 constraints over 4 propositions, rank 3)
A_FULL = [[1., -1., 0., 0.], [0., 1., -1., 0.], [0., 0., 1., -1.]]


def test_g1_calls_real_lexicon_and_g8_assembles():
    ex = run_gates(Issue(statement="the mass of a particle"))
    assert "τ_c" in ex.translation            # real lexicon output, not paraphrase
    assert len(ex.gates) == 10                # G1..G7 + G9..G11; G8 = the assembly
    assert not ex.complete()                  # operator pieces still open -> honest
    assert "SKIPPED" in ex.not_checked or "operator fills" in ex.not_checked


def test_g2_flags_injected_infinity():
    assert g2_infinity("assume the continuum of real number values").verdict == "FLAG"
    assert g2_infinity("a finite list of readouts").verdict == "PASS"


def test_g3_same_name_different_chain_is_flagged():
    iss = Issue(statement="s", quantities=[
        Quantity("H0", chain="CMB acoustic + flat-LCDM closure"),
        Quantity("H0", chain="Cepheid ladder direct")])
    assert g3_quantity_role(iss).verdict == "FLAG"        # the Hubble case
    iss2 = Issue(statement="s", quantities=[Quantity("H0", chain="CMB")])
    assert g3_quantity_role(iss2).verdict == "PASS"


def test_g5_reproduces_ltp4_null_space():
    iss = Issue(statement="s", grammar=A_FULL, query=[1., 1., 1., 1.])
    r = g5_identifiability(iss)
    assert r.verdict == "FLAG" and r.tier == "finite_diagnostic"
    assert "rank 3/4" in r.detail
    assert "STRUCTURALLY unanswerable" in r.detail        # query along (1,1,1,1)


def test_g5_full_rank_passes():
    iss = Issue(statement="s", grammar=[[1., 0.], [0., 1.]])
    assert g5_identifiability(iss).verdict == "PASS"


def test_g5_hypothesis_dims_both_branches():
    """Counting path: more hypothesis dims than record coords -> FLAG;
    fewer/equal -> PASS (not a PROMPT fall-through)."""
    q = [Quantity("Ep", "spectral fit"), Quantity("Eiso", "flux+z")]
    flag = g5_identifiability(Issue(statement="s", quantities=q, hypothesis_dims=3))
    ok = g5_identifiability(Issue(statement="s", quantities=q, hypothesis_dims=2))
    assert flag.verdict == "FLAG" and ok.verdict == "PASS"
    assert "no structural obstruction" in ok.detail


def test_g6_reproduces_ltp3_dichotomy():
    # query (b1-b2): row 3 idle -> PASS ; query (b3-b4): row 3 load-bearing -> FLAG
    idle = g6_load_bearing(Issue(statement="s", grammar=A_FULL,
                                 query=[1., -1., 0., 0.], discard_rows=[2]))
    load = g6_load_bearing(Issue(statement="s", grammar=A_FULL,
                                 query=[0., 0., 1., -1.], discard_rows=[2]))
    assert idle.verdict == "PASS" and load.verdict == "FLAG"


def test_g7_rejects_infinity_benchmarked_refutation():
    iss = Issue(statement="s",
                refutation_benchmark="compared against the continuum diffusion limit h -> 0")
    assert g7_readout_vs_readout(iss).verdict == "FLAG"


def test_g2_dual_guard_flags_injected_zero():
    """Zero side of the Guard (Z1-Z4): an exact zero is a non-readout too."""
    assert g2_infinity("model the electron as a point particle at T = 0").verdict == "FLAG"


def test_g9_theorem_hook_hits_and_misses():
    """Real arc lookup: a genuine theorem resolves; a fake name auto-downgrades.
    Tier is Dr (grep = referenced, NOT re-verified) per review 2026-07-19."""
    from lens.gates import g9_theorem_check
    hit = g9_theorem_check(Issue(statement="s", cited_theorems=["sqrt2_is_not_a_readout"]))
    assert hit.verdict == "PASS" and "FOUND" in hit.detail and hit.tier == "Dr"
    assert "grep-level" in hit.detail          # never reads as verification
    miss = g9_theorem_check(Issue(statement="s", cited_theorems=["totally_fake_theorem_xyz"]))
    assert miss.verdict == "FLAG" and "auto-downgrade" in miss.detail


def test_g9_no_substring_false_pass_and_keyword_coverage():
    """Review probes hardened: fragments ('row','Sum') must MISS; results
    proved via Remark/Example keywords must be FOUND."""
    from lens.solver_link import theorem_lookup
    assert theorem_lookup("row")["found"] is False        # fragment of row_u
    assert theorem_lookup("Sum")["found"] is False        # fragment of Sum_peel_*
    r = theorem_lookup("period4_and_period5_are_distinct")  # a real Coq Remark
    assert r["found"] is True and r["v_files"]


def test_g10_limit_certifies_decay():
    """Fitted-law verdict from the live limits engine on a clean 1/n decay."""
    from lens.gates import g10_limit
    n = list(range(1, 40))
    iss = Issue(statement="s", limit_series=([1.0/k for k in n], [float(k) for k in n]),
                limit_side="zero")
    r = g10_limit(iss)
    assert r.tier in ("finite_diagnostic", "Open")
    if r.tier == "finite_diagnostic":          # solver present on this machine
        assert "verdict=" in r.detail


def test_g11_semantics_hardened():
    """Review probes: fabricated closures PROMPT (nothing adjudicated);
    self-pair trivially equivalent; a real registered pair passes both ways;
    absence of registration is stated as UNDECIDED, never as inequivalence."""
    from lens.gates import g11_equivalence
    fake = g11_equivalence(Issue(statement="s",
                                 formula_pair=("nonexistent_closure_a", "nonexistent_closure_b")))
    assert fake.verdict == "PROMPT" and "unknown closure" in fake.detail
    real = g11_equivalence(Issue(statement="s",
                                 formula_pair=("van_t_hoff_equation", "clausius_clapeyron")))
    if real.verdict != "PROMPT":               # solver present on this machine
        assert real.verdict == "PASS" and "EQUIVALENT" in real.detail
        rev = g11_equivalence(Issue(statement="s",
                                    formula_pair=("clausius_clapeyron", "van_t_hoff_equation")))
        assert rev.verdict == "PASS"
        selfp = g11_equivalence(Issue(statement="s",
                                      formula_pair=("van_t_hoff_equation", "van_t_hoff_equation")))
        assert selfp.verdict == "PASS" and "trivially equivalent" in selfp.detail
