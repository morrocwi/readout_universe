"""lens.solver_link -- live link to the sibling research_universal_solver.

Anti-drift policy: beyond the four frozen snapshots in lens/vendor/, NOTHING
is vendored. Heavier capabilities (limits, equivalence, theorem index, MCP)
are reached LIVE in the sibling repo so they never go stale; when the solver
is absent every caller degrades to an honest PROMPT/SKIPPED -- never a fake.

PRIVATE / PROPRIETARY (see LICENSE EXCEPTIONS) -- do not publish.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_DEFAULT = Path("/home/yaoharee-lt/ANSE.ASIA/research_universal_solver")


def solver_path() -> Path | None:
    """Locate the solver: $ANSE_SOLVER_PATH first, then the default sibling."""
    for cand in (os.environ.get("ANSE_SOLVER_PATH"), _DEFAULT):
        if cand and Path(cand).joinpath("engine").is_dir():
            return Path(cand)
    return None


def import_engine(module: str):
    """Import engine.<module> from the live solver; None if unavailable."""
    root = solver_path()
    if root is None:
        return None
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import importlib
    try:
        return importlib.import_module(f"engine.{module}")
    except ModuleNotFoundError:
        return None          # genuinely absent module/solver
    except Exception:
        # solver present but the module failed to import -- surface it,
        # do NOT misreport as "solver unavailable" (reviewer NIT, PR #6)
        raise


def theorem_lookup(name: str) -> dict:
    """Resolve a claimed theorem name against the solver's machine-checked
    arc: THEOREM_INDEX.md + formal/*.v. Returns {found, index_hits, v_files}.
    A miss means the claim has NO Th_coqc backing -- auto-downgrade to Dr."""
    root = solver_path()
    if root is None:
        return {"found": None, "index_hits": [], "v_files": [],
                "note": "solver unavailable -- cannot verify; treat as UNVERIFIED"}
    if not re.fullmatch(r"[A-Za-z0-9_']+", name):
        return {"found": False, "index_hits": [], "v_files": [],
                "note": "invalid theorem identifier"}
    hits, vfiles = [], []
    # Match ONLY the index's name field (backtick-quoted, e.g. **Thm** `name`).
    # A bare-token match is not enough: fragments like 'row'/'Sum' occur as
    # function tokens inside OTHER theorems' statements (reviewer probe).
    tok = re.compile(rf"`{re.escape(name)}`")
    idx = root / "docs/root/THEOREM_INDEX.md"
    if idx.is_file():
        for i, line in enumerate(idx.read_text(errors="ignore").splitlines(), 1):
            if tok.search(line):
                hits.append(f"THEOREM_INDEX.md:{i}")
    formal = root / "formal"
    if formal.is_dir():
        # all Coq proof-introducing keywords this arc actually uses
        pat = re.compile(
            rf"\b(Theorem|Lemma|Corollary|Remark|Proposition|Fact|Example)\s+"
            rf"{re.escape(name)}(?![A-Za-z0-9_'])")
        for v in sorted(formal.glob("*.v")):
            try:
                if pat.search(v.read_text(errors="ignore")):
                    vfiles.append(v.name)
            except OSError:
                continue
    return {"found": bool(hits or vfiles), "index_hits": hits[:5],
            "v_files": vfiles[:5], "note": ""}
