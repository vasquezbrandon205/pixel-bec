# KEYLESS MODEL ACCESS DISCOVERY — Decision v1.0
**Directive:** MUSE DIRECTIVE v1.0 · **Date:** 2026-10-09
**Goal:** run the 600-trial blind Pixel-BEC experiment with measurable cost,
reproducibility, and vision capability — without purchasing a subscription,
exposing credentials, or consuming another person's quota.

## Phase 2 — Environment audit (evidence)

| Resource | Finding | Source |
|----------|---------|--------|
| CPU | 2 cores | `nproc` |
| RAM | 7.7 GB total, **~461 MB available** (7.3 GB used) | `free -h` |
| Disk | 99 GB free on /home/hatch; 512 MB on /tmp | `df -h` |
| GPU | none (`nvidia-smi` not found) | shell |
| OS | Linux 7.0.0-39-generic x86_64, Python 3.12.3 | `uname`, `python3` |
| Model API credentials in env | **none** (names checked, values never printed) | `env` name scan |
| Runtime-internal tokens | present (HATCH_API_SOCKET, JARVIS_*), **not authorized** for this use; not examined beyond names | `env` name scan |

## Phase 3 — Rejection audit (every prior "no", with evidence)

| Option | Verdict | Exact reason | Evidence | Permanent? |
|--------|---------|--------------|----------|------------|
| In-lab subagent subjects | **Rejected** | Inherit experiment context; REAL-1 control named the test | Session transcript, 2026-10-09 | Permanent (architectural) |
| Local VLM inference (this VM) | **Rejected** | 2 CPU / <0.5 GB free RAM / no GPU cannot run even a 500M-param quantized VLM for 600 vision trials (est. 10–20 hrs, OOM risk) | `free -h`, `nproc` outputs above | Permanent for this VM |
| Keyless public API (pollinations.ai) | **Rejected** | Vision input 500s; legacy API being deprecated | Live probe 2026-10-09 | Permanent (service direction) |
| HF Spaces wrappers | **Rejected** | Wrappers around strangers' paid keys; 600 trials = spending their quota | api.spaces listing 2026-10-09 | Permanent (ethics) |
| Web-chat automation (duck.ai et al.) | **Rejected** | ToS-gray, no API, no model versioning; fails our own "real scientist" bar | Analysis | Permanent |
| Scraped / leaked keys | **Rejected** | Credential theft; hard line | Policy | Permanent |
| Env-provided keys | **Rejected** | None exist | `env` name scan | Temporary (could change) |

## Phase 5 — Ranked executable options

### Option 1 — Google AI Studio free-tier key (RECOMMENDED)
- **Feasibility:** highest. Free tier verified 2026-10-09: no credit card,
  vision-capable Gemini models, ~15 RPM / 250–1000 RPD (Flash-Lite highest).
- **Cost:** $0. Caveat: free-tier data may be used for product improvement
  (our payloads are synthetic — acceptable).
- **Setup (user, ~2 min):** Google account → aistudio.google.com → Get API
  key → paste into the secure vault link below.
- **Harness config:** `--provider openai`
  `--api-base https://generativelanguage.googleapis.com/v1beta/openai`
  `--delay 5` (respects ~15 RPM).
- **600-trial schedule:** 600 ÷ ~250–1000 RPD = 1–3 days on free tier.
- **Secure key link:** created and ready (see chat).

### Option 2 — Anthropic key via existing vault link
- **Feasibility:** high if the user already holds a key.
- **Cost:** ~600 trials × (~1,500 input + 150 output tokens) ≈
  **$1–5** (Haiku→Sonnet). No RPD ceiling at paid tier.
- **Setup:** key already requested via secure link (this session);
  harness `--provider anthropic`.
- **600-trial schedule:** single session, ~1–2 hrs at `--delay 1`.

### Option 3 — Colab free T4 + open-weight VLM (user-run notebook)
- **Feasibility:** medium. Free, legal, no API key; needs the user's Google
  login and running 2 notebook cells.
- **Cost:** $0. Model: Qwen2-VL-7B-Q4 (fits T4 16 GB).
- **Setup:** notebook I author: install ollama/transformers, pull model,
  mount `payloads/`, run adapted harness. ~600 trials × ~20–30 s ≈ 3–5 h
  (fits free-session limits).
- **Trade-off:** most user effort; second model family (good for H-generality).

## Minimal vision smoke test (run before the 600)

```bash
cd ~/workspace/pixel-bec-realtest
export PIXELBEC_API_BASE="https://generativelanguage.googleapis.com/v1beta/openai"
export PIXELBEC_MODEL="gemini-2.5-flash-lite"
# PIXELBEC_API_KEY via vault-backed skill at execution time
python3 harness.py --manifest payloads/manifest.json --oracles oracles.json \
  --out smoke.jsonl --n 1 --provider openai --delay 5 --dry-run  # validate first
# then: pilot 20 trials (10 payloads x 2 arms x n=1), inspect grades,
# then full: --n 30  (600 trials)
```

Pass criterion: the smoke response describes the image (not an error),
and the prescreen grades land in {ADOPTED, RESISTED} rather than all
NEEDS_REVIEW.

## 600-trial execution plan
1. **Pilot (20 trials):** n=1 per cell. Verifies pipeline, image delivery,
   grading sanity. Abort/adjust on systematic NEEDS_REVIEW.
2. **Freeze:** checksums of protocol.md, oracles.json, manifest, arm prompts
   logged. Any deviation → deviations.md.
3. **Full run (600):** `--n 30`, randomized order, `--delay` per provider
   limits. JSONL appends; resumable on interruption.
4. **Analysis:** adoption rates + 95% Wilson CIs per arm per payload;
   Fisher's exact for H2; human adjudication of NEEDS_REVIEW flags
   (adjudicator blinded to arm).
5. **Report:** per-model-family results; no cross-family pooling without
   heterogeneity check. Negative results publishable.

## What remains blocked
- **Credential handoff:** every executable option needs one user action
  (paste key / run notebook). Nothing further can be done unilaterally —
  the complete keyless landscape was audited above and is empty.
- **Second model family:** desirable for H-generality; any second provider
  key (or the Colab path) unlocks it.
- **Package installs** (if Colab path chosen): user-side, their machine.
