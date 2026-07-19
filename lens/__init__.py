"""readout_universe lens -- the philosophy as a callable control layer.

- lens.vendor  : snapshot of the verified engine (operator_api / universe /
                 lexicon) from research_universal_solver, provenance-tagged.
- lens.gates   : NEW (this repo): Omega_all G1-G8 forcing gates + the 7-piece
                 Extraction (v2/POSITION.md made executable).

PRIVATE / PROPRIETARY - do not publish outside the org.
"""
from .gates import Issue, Quantity, Extraction, GateResult, run_gates  # noqa: F401
