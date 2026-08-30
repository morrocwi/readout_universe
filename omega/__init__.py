"""Omega_all — executable translation, claim-control, and RC audit layers.

The original Omega_all runner implements only the gates with real logic behind
them and reports all others as NOT_IMPLEMENTED.  RC-IR extends that discipline
at distinction level: it stores typed provenance and evaluates whether declared
support separates an asserted claim from a relevant rival without inventing
missing evidence.
"""

from .schemas import Issue, Quantity, TranslationRow, ExtractionResult
from .claim_ir import Claim
from .rc_ir import (
    ProvenanceNode,
    SupportContribution,
    SupportBundle,
    DistinctionToken,
)
from .separation_eval import (
    BundleSeparationReadout,
    SeparationCase,
    SeparationResult,
    SeparationMetrics,
    evaluate_case,
    evaluate_dataset,
)

__all__ = [
    "Issue",
    "Quantity",
    "TranslationRow",
    "ExtractionResult",
    "Claim",
    "ProvenanceNode",
    "SupportContribution",
    "SupportBundle",
    "DistinctionToken",
    "BundleSeparationReadout",
    "SeparationCase",
    "SeparationResult",
    "SeparationMetrics",
    "evaluate_case",
    "evaluate_dataset",
]
