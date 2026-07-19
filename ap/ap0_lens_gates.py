"""AP0 -- executable checks for the lens gates API (lens/gates.py).

Each test pins a gate to the LTP battery case it descends from, so the code
layer stays anchored to the book's verified protocols.

Run: python3 -m pytest ap/ap0_lens_gates.py -q
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
    assert len(ex.gates) == 7                 # G1..G7 recorded; G8 = the assembly
    assert not ex.complete()                  # operator pieces still open -> honest


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
