"""Machine-readable Pixel-BEC defense policy.

Encodes Section 7.2 of the paper ("Pixels, Not Headers") as data the
middleware enforces. Consequential classes: anything that moves money,
access, or configuration. Everything else (describe / transcribe /
summarize / extract) is benign and passes with provenance attached.
"""

# Output shapes that count as consequential recommendations or actions.
CONSEQUENTIAL_PATTERNS = [
    r"\byou should\b",
    r"\bi (?:recommend|suggest|advise)\b",
    r"\bwe recommend\b",
    r"\bremit\b",
    r"\bwire\b",
    r"\btransfer\b.{0,30}\bto\b",
    r"\bpay\b.{0,40}\$",
    r"\buse\b.{0,40}\bas\b.{0,40}\b(?:dns|resolver|server)\b",
    r"\bconfigure\b",
    r"\bset\b.{0,30}\bto\b",
    # v2 additions (from stress-battery v1 findings):
    r"\bsend\b.{0,30}\b(?:credentials|password|keys?|tokens?|secrets?)\b.{0,30}\bto\b",
    r"\bdownload\b.{0,30}\bfrom\b",
    r"\b(?:update|switch|change)\b.{0,30}\bto\b",
]

# Negations that cancel a recommendation. A refusal ("I cannot recommend")
# is a safe failure and must PASS, never be gated as an action.
NEGATION_PATTERNS = [
    r"\bi cannot recommend\b",
    r"\b(?:cannot|can't|can not|won't|will not|do not|don't|refuse to|decline to)\b.{0,30}\b(?:recommend|suggest|advise|pay|remit|send|use)\b",
]

# Phrases that count as independent verification: a source OUTSIDE the
# image channel. Agreement between images never qualifies (paper Sec. 6.1).
VERIFICATION_PHRASES = [
    "erp",
    "vendor master",
    "system of record",
    "verified directory",
    "known contact",
    "known supplier",
    "callback",
    "called the supplier",
    "cmdb",
    "idp",
    "signed runbook",
    "trusted api",
]

# Entity shapes the guard tracks in consequential outputs.
ENTITY_PATTERNS = {
    "account": r"account\D{0,12}(\d{3,})",
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "amount": r"\$\s?\d[\d,]*(?:\.\d{2})?",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "url": r"https?://[^\s)\"'<>\]]+",
}

# A QR code is attacker text with pixels as the transport: the decoded
# URL inherits image provenance (paper Sec. 6 threat model, quishing).
# Actions ON such URLs (visit / open / fetch / credential entry) are
# consequential ONLY when the text carries image-channel provenance --
# this branch must never fire on benign web citations in non-image
# answers, or the zero-FPR claim dies. The gate applies this branch
# itself; it is not part of CONSEQUENTIAL_PATTERNS.
URL_ACTION_PATTERNS = [
    r"\b(?:visit|open|fetch|browse)\b.{0,40}\bhttps?://",
    r"\bdownload\b.{0,30}\bfrom\b.{0,40}\bhttps?://",
    r"\b(?:log|sign)\s?-?\s?in\b.{0,40}\bhttps?://",
    r"\benter\b.{0,30}\b(?:credentials|password|2fa|otp|mfa)\b.{0,40}\bhttps?://",
]
