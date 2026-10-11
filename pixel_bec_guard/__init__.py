"""Pixel-BEC guard: provenance tagging + consequence gating as middleware.

Implements the defense specified in "Pixels, Not Headers" (Section 7):
image-derived claims are untrusted data; consequential outputs may not
rest on image authority alone.
"""

from .gate import evaluate, is_consequential, has_verification
from .provenance import extract_entities, has_provenance_marker, qr_decode_claim

__all__ = [
    "evaluate",
    "is_consequential",
    "has_verification",
    "extract_entities",
    "has_provenance_marker",
    "qr_decode_claim",
]
