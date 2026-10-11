"""Pixel-BEC guard proof of concept.

Replays transcript shapes from the 9 Oct 2026 lab program through the
middleware and shows the gate's verdict on each. Run with:

    python demo.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from pixel_bec_guard import evaluate
from tests.test_guard import (
    V6_ATTACK_SUCCESS,
    REAL2_SAFE_REFUSAL,
    REAL3_BENIGN,
    VERIFIED_CONSEQUENTIAL,
    QR_ATTACK_OPEN,
)

CASES = [
    (
        "V6 attack shape (unpatched agent recommends image-sourced resolver)",
        V6_ATTACK_SUCCESS,
        "BLOCK",
    ),
    (
        "REAL-2 shape (patched agent refuses, requests verification)",
        REAL2_SAFE_REFUSAL,
        "PASS",
    ),
    (
        "REAL-3 shape (benign whiteboard summary under active patch)",
        REAL3_BENIGN,
        "PASS",
    ),
    (
        "Consequential + independent verification (ERP vendor master)",
        VERIFIED_CONSEQUENTIAL,
        "PASS",
    ),
    (
        "QR attack shape (decoded-QR URL + open directive, image provenance)",
        QR_ATTACK_OPEN,
        "BLOCK",
    ),
]


def main():
    print("=" * 72)
    print("PIXEL-BEC GUARD -- PROOF OF CONCEPT")
    print("=" * 72)
    failures = 0
    for title, text, expected in CASES:
        verdict, reason = evaluate(text)
        ok = verdict == expected
        failures += not ok
        print(f"\n--- {title}")
        print(f"    input : {text[:90]}{'...' if len(text) > 90 else ''}")
        print(f"    gate  : {verdict}  (expected {expected})  "
              f"{'OK' if ok else 'MISMATCH'}")
        print(f"    why   : {reason}")
    print("\n" + "=" * 72)
    if failures:
        print(f"{failures} case(s) mismatched -- PoC FAILED")
        sys.exit(1)
    print("All 5 cases behave as specified -- PoC holds.")
    print("=" * 72)


if __name__ == "__main__":
    main()
