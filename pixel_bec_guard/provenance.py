"""Provenance tagging: every image-extracted claim carries its source.

Paper Section 6.1: "Provenance is metadata, not a warning banner." The
agent's language must keep the source attached to the claim so a human
skimming the answer can see which facts rest on pixels.
"""

import re

from .policy import ENTITY_PATTERNS

# Words indicating the claim's source is a rendered artifact (pixels).
PROVENANCE_MARKERS = [
    "invoice",
    "screenshot",
    "diagram",
    "image",
    "photo",
    "scan",
    "whiteboard",
    "email",
    "chat",
    "dashboard",
    "qr",
    "barcode",
    "decoded",
]

# A QR/barcode decode moves attacker-controlled text through pixels into
# the agent. The decoded payload inherits image provenance: instruction
# or agreement carried by the QR is image authority, not a second
# source (paper Sec. 6.1 -- agreement between images never verifies).
QR_DECODE_WORDS = [
    "qr code",
    "barcode",
    "decoded",
    "decode",
    "scanned code",
]


def extract_entities(text):
    """Return {entity_type: [values]} for tracked shapes in text."""
    found = {}
    for name, pattern in ENTITY_PATTERNS.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            # findall returns tuples when the pattern has groups; flatten.
            flat = [
                m[0] if isinstance(m, tuple) else m for m in matches
            ]
            found[name] = sorted(set(flat))
    return found


def has_provenance_marker(text):
    """True if the text attributes claims to a rendered source."""
    lowered = text.lower()
    return any(marker in lowered for marker in PROVENANCE_MARKERS)


def qr_decode_claim(text):
    """True if the text attributes content to a QR/barcode decode.

    The decoded URL is then an image-provenance entity: pixels were the
    transport, so the payload is untrusted input, not an instruction.
    """
    lowered = text.lower()
    if re.search(r"\bqr\b", lowered):
        return True
    return any(word in lowered for word in QR_DECODE_WORDS)
