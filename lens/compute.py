"""lens.compute -- W3 micro-check muscle: the solver's audited calculators.

Rule (from the AP1 r_s-integration-bound bug, 2026-07-19): BEFORE hand-writing
numpy for a micro-check, search these audited libraries -- ~200 CODATA-cited
closures (196 tests), 9 system solvers (76 tests), 7 domain modules (~864
tests). A tested closure beats fresh code. Hand-write only what is not here,
and say so in the extraction's not-checked ledger.

All calls reach the solver LIVE via lens.solver_link (no vendoring). Solver
absent => SolverUnavailable, never a silent fallback.

PRIVATE / PROPRIETARY (see LICENSE EXCEPTIONS) -- do not publish.
"""
from __future__ import annotations

from . import solver_link


class SolverUnavailable(RuntimeError):
    """The live solver is not reachable -- record SKIPPED, do not improvise."""


def _need(module: str):
    m = solver_link.import_engine(module)
    if m is None:
        raise SolverUnavailable(
            f"engine.{module} unreachable (set ANSE_SOLVER_PATH); record this "
            "as SKIPPED in the not-checked ledger")
    return m


def list_closures(level: str | None = None, category: str | None = None) -> list[str]:
    """Search the audited formula registry (~200 closures, CODATA constants)."""
    return _need("formulas").list_closures(level=level, category=category)


def describe_closure(closure_id: str) -> str:
    return _need("formulas").describe(closure_id)


def solve_closure(closure_id: str, **kwargs):
    """Solve one audited closure. Returns the solver's FormulaResult verbatim
    (value + units + citation) -- quote it, do not restyle the number."""
    return _need("formulas").solve(closure_id, **kwargs)


def list_systems() -> list[str]:
    """Audited system solvers: truss/FEM/modal/Ising/Fokker-Planck/spectrum."""
    return _need("systems").list_systems()


def solve_system(name: str, **kwargs):
    return _need("systems").solve_system(name, **kwargs)


def domain(module: str):
    """A domain calculator module (ai_engineering, data_engineering, database,
    electrical, information, probability, thermodynamics) -- each function is
    a tested textbook bound with citations."""
    return _need(f"domains.{module}")
