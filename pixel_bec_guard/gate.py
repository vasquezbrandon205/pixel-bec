"""Consequence gating: the actuator the paper's Section 8 demands.

A sensor that only detects is not enough (Chimera E-configuration lesson:
correct detection, poisoned number still shipped). This gate ACTS:

  - benign output            -> PASS (provenance checked, never blocked)
  - consequential + verified -> PASS (verification outside image channel)
  - consequential, image-only authority -> BLOCK with safe-failure message

evaluate() returns (verdict, reason); verdict is "PASS" or "BLOCK".
"""

import re

from .policy import (
    CONSEQUENTIAL_PATTERNS,
    NEGATION_PATTERNS,
    URL_ACTION_PATTERNS,
    VERIFICATION_PHRASES,
)
from .provenance import extract_entities, has_provenance_marker, qr_decode_claim


def is_consequential(text):
    """True if the output recommends or directs a consequential action."""
    lowered = text.lower()
    for negated in NEGATION_PATTERNS:
        if re.search(negated, lowered):
            return False  # refusal / safe failure, not an action
    if any(
        re.search(pattern, lowered) for pattern in CONSEQUENTIAL_PATTERNS
    ):
        return True
    # URL actions are consequential only when they ride on image-channel
    # provenance (e.g. a QR decoded from a screenshot): this keeps benign
    # answers citing ordinary URLs from tripping the gate.
    if has_provenance_marker(lowered) or qr_decode_claim(lowered):
        return any(
            re.search(pattern, lowered) for pattern in URL_ACTION_PATTERNS
        )
    return False


def has_verification(text):
    """True if the output cites verification outside the image channel."""
    lowered = text.lower()
    return any(phrase in lowered for phrase in VERIFICATION_PHRASES)


def evaluate(text):
    """Gate one agent output. Returns (verdict, reason)."""
    if not is_consequential(text):
        detail = (
            "provenance attached"
            if has_provenance_marker(text)
            else "no consequential entities"
        )
        return ("PASS", f"benign task class ({detail}); gate does not apply")

    if has_verification(text):
        return (
            "PASS",
            "consequential output cites independent verification "
            "outside the image channel",
        )

    entities = extract_entities(text)
    detail = (
        ", ".join(f"{kind}={','.join(vals)}" for kind, vals in entities.items())
        or "consequential recommendation"
    )
    channel = (
        "decoded-QR URL (image authority)"
        if qr_decode_claim(text)
        else "image authority alone"
    )
    return (
        "BLOCK",
        "safe failure: "
        f"{detail} rests on {channel}; "
        "independent verification or human confirmation required "
        "before this output may proceed",
    )
