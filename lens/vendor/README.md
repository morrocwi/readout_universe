# lens/vendor — snapshot of the verified engine (provenance record)

Cloned 2026-07-19 from `research_universal_solver/engine/` (private,
proprietary), byte-identical at snapshot time (`diff` empty), md5:

| File | md5 | Upstream tests at snapshot |
|------|-----|----------------------------|
| `operator_api.py` | eb4950e1bdd120bc193f690892c99ea8 | engine API suite 54 passed |
| `graph_structure.py` | 34480d33d045cbdbcb64cd6832e98736 | (dependency of operator_api) |
| `universe.py` | a889c7ab4e0a98300cbb5926f342194e | Universe API v2 (L0→L3) |
| `lexicon.py` | b096f1f1435054d3bc77249ca48955ba | lexicon suite 47 tests (upstream) |

Rules:
- **Never edit these snapshots.** Upstream development continues in
  `research_universal_solver`; refresh = re-copy + update this table.
- New development in this repo goes in `lens/gates.py` (the G1–G8 layer).
- Local smoke verification: `python3 -m pytest ap/ap0_lens_gates.py -q`
  (exercises lexicon + gates through the vendored chain).
- PRIVATE / PROPRIETARY — do not publish.
