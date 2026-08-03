"""Omega_all — a minimal, genuinely executable runner for the 8-step
Translation Protocol loop (v2/TRANSLATION_PROTOCOL.md) and a subset of the
G1-G13 gate table (v2/POSITION.md).

This package does NOT claim to implement all 13 gates. Only the gates with
real logic behind them are implemented (see gates.py IMPLEMENTED_GATES);
every other gate exists as a named stub that honestly reports
"NOT_IMPLEMENTED" rather than fabricating a verdict.
"""

from .schemas import Issue, Quantity, TranslationRow, ExtractionResult

__all__ = ["Issue", "Quantity", "TranslationRow", "ExtractionResult"]
