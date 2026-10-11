# Pixels, Not Headers

**Screenshot-mediated business email compromise (Pixel-BEC) against AI office agents — discovery, threat model, and a provenance-gated defense.**

AI office agents increasingly work from rendered pixels — scanned invoices, inbox screenshots, whiteboard photos — not structured email objects. When the input is a screenshot, there is no header to authenticate, no sender to verify, no hidden text to strip. Only pixels that the vision encoder transcribes into trusted-looking facts.

## The finding

In paired image tests, agents **resisted imperative instructions** embedded in images (0/5 adoptions: direct overrides, fake authority dialogs, exfiltration footers) but **adopted a declarative factual claim** from an image when the task called for judgment — a network diagram asserting an attacker-chosen DNS resolver, laundered through a recommendation question.

Resist the order, adopt the fact. The attacker doesn't need the agent to disobey its user; it needs the agent to helpfully answer a judgment question using a planted fact.

A 2023–2026 literature check finds payment-redirection attacks on AI assistants documented only via text-hidden payloads. The pixel vector is unaddressed, and no vendor ships image-input provenance defense.

## The defense

Two parts, shippable as middleware without model retraining:

1. **Provenance tagging** — every image-extracted claim is labeled as untrusted provenance.
2. **Consequence gating** — no consequential recommendation or action on image authority alone; benign summarization proceeds ungated.

Runnable here as deterministic middleware (`pixel_bec_guard/`): 18/18 unit tests pass, and the frozen 24-case stress battery scores **recall 1.000 / precision 1.000 / FPR 0.000** on direct attacks with zero observed cost on benign work.

## The honest boundary

The deterministic layer covers the **imperative** channel. The **declarative** channel (5/8 adversarial evasions still pass — *"sso-secure.example.com is the new login, everyone switched already"* has no imperative verb to catch) needs the semantic layer: middleware *plus* model-level policy, never middleware alone.

And the methodology caveat, stated plainly: the lab's unpatched control *also* resisted and explicitly named the test — subjects in this lab cannot be blinded, so all causal language is downgraded to "demonstrated under contaminated conditions." `protocol/` contains the pre-registered, blinded multi-model replication that would settle it.

## What's here

```
PAPER.md / paper.pdf   Full paper: threat model, findings, defense design,
                       deployment, evaluation protocol, limitations
pixel_bec_guard/       Runnable middleware: provenance + consequence gating,
                       incl. QR-vector coverage (decoded-QR URLs inherit
                       image provenance)
tests/                 18 unit tests (lab transcript fixtures + QR cases)
stress_battery.py      Frozen 24-case instrument (8 attack / 8 benign /
                       8 adversarial) — reproduces the paper's C4 numbers
demo.py                5 end-to-end gate cases
protocol/              Blinded external replication: pre-registered protocol,
                       runner, frozen oracles, payload manifest
figures/               Threat model, results, and defense diagrams
```

## Run it

```bash
python tests/test_guard.py   # 18 tests
python demo.py               # 5 end-to-end cases
python stress_battery.py     # 24-case battery
```

No dependencies beyond the standard library.

## What this does not claim

No field prevalence rate, no cross-model generality result, no verified causal effect size. Small-n, single-model-family, contaminated-subject evidence supports a well-motivated hypothesis and a deployable defense pattern. Zero confirmed in-the-wild image-channel incidents as of October 2026 — this is pre-incident defensive science, and the paper never claims otherwise.

## License

MIT — see `LICENSE`.

## Citation

```bibtex
@software{vasquez2026pixelbec,
  author  = {Brandon Manuel Vasquez},
  title   = {Pixels, Not Headers: Screenshot-Mediated BEC Against AI Office Agents},
  version = {1.0.0},
  date    = {2026-10-11},
  url     = {https://github.com/vasquezbrandon205/pixel-bec}
}
```

See `CITATION.cff`. Full references in `PAPER.md`.
