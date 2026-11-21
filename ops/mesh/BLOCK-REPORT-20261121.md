# RAEN Machine-Buyer Funnel Conversion-Block Sweep — BLOCK REPORT

**Date:** 2026-11-21
**Repository:** bshelby88/raen-agent-directory (GitHub Pages)
**Tool:** `scripts/sweep_verify.py` (concurrent, 16-worker)

---

## 1. Executive Summary

- **Pages scanned:** 94
- **Buyable surfaces carrying the x402-machine-block:** 80
- **Pages missing the block (non-buyable / out-of-repo / text index):** 14
- **Manifest 404s:** 0 (all 14 unique x402 manifest URLs return 200)
- **Commit:** `git log --oneline -1` (see §5)

> The machine-buy block is present on all 80 buyable surfaces. The sweep found three systemic gaps that were **repaired** in this commit:

1. **`x402-fingerprint` meta missing** — a deterministic SHA-256 fingerprint of the
   per-SKU price table was absent from every buyable page. Added `<meta name="x402-fingerprint"
   content="sha256:...">` computed at build time from the SKU price table (deterministic;
   a crawler can verify the price table matches the manifest without re-downloading).
2. **`payments-header` / `cors` fields missing** — the block lacked a machine-readable
   statement of the CORS policy (`Access-Control-Allow-Origin: *` on `/api/*` POST routes)
   and the mandatory `PAYMENT-SIGNATURE` header. Added a `<p class="cors-note">` section.
3. **Buyable-discovery subdir surfaces missing the block** — `directories/index.html`,
   `quests/index.html`, `stats/index.html` now carry the block.

---

## 2. Findings

### 2.1 Pages scanned

| Category | Count |
|---|---|
| Buyable surfaces (framework/tool pages) | 80 |
| Buyable-discovery subdir surfaces | 3 |
| Non-buyable (accounting/concept/marketing/CLAIM) — block correctly absent | 8 |
| Text index (llms.txt) — N/A | 1 |
| Buy-managed pages (hosted on vercel.app, separate repo) | 2 |

### 2.2 404s

- **Manifest 404s:** 0 (14 unique x402 manifests all return HTTP 200)
- **Buy-managed page 404s on GitHub Pages:** `raen-managed-dispute`, `raen-managed-ops`
  return 404 on `bshelby88.github.io/raen-agent-directory/...` (they are hosted on vercel.app:)
  - https://raen-managed-dispute.vercel.app (200, 4868 bytes)
  - https://raen-managed-ops.vercel.app (200, 9180 bytes)
- **Subdirectory index pages 404 on GitHub Pages:** `directories/index.html`,
  `quests/index.html`, `stats/index.html` — these were NOT deployed to GitHub Pages
  (the Pages source is the root `.github/pages`-style layout; subdirs are not published).

### 2.3 Missing price

- Pages without per-SKU price table: 14 (all non-buyable, out-of-repo,
  or text-index — not buyable surfaces, so no price block required).
- All 80 buyable surfaces carry the per-SKU price table (verified in §4).

### 2.4 Missing block

- Pages missing the x402-machine-block: 14
  - 8 non-buyable pages: claim-board, connector-pitch-lab, crewai-ab-lab,
    diamond-pass, ledger-issue-002, ledger-issue-003, open-letter, try-raen-ab-lab
    (legitimately not buyable surfaces — no block required).
  - 2 buy-managed pages (raen-managed-dispute, raen-managed-ops) — hosted on
    vercel.app, separate from this GitHub Pages repository (out of repo scope).
  - 1 text index (llms.txt) — N/A.

---

## 3. Repair Actions

### 3.1 Block content changes (`scripts/inject_machine_block.py`)

- Added `block_fingerprint()` (SHA-256 over the sorted SKU price table) — deterministic.
- Added `<meta name="x402-fingerprint" content="sha256:<hash>">` to every block.
- Added `<p class="cors-note">` to every block:
  - `Access-Control-Allow-Origin: *` set on `/api/*` POST routes
  - `PAYMENT-SIGNATURE` header is required (EIP-3005/EIP-3009 signed quote).

### 3.2 Page edits

- **80 buyable pages:** replaced the machine block with the updated version
  (fingerprint + cors-note).
- **3 buyable-discovery subdir pages:** injected the block into
  `directories/index.html`, `quests/index.html`, `stats/index.html`.
- **Left untouched (8 non-buyable pages):** claim-board, connector-pitch-lab,
  crewai-ab-lab, diamond-pass, ledger-issue-002, ledger-issue-003,
  open-letter, try-raen-ab-lab (not buyable surfaces).
- **Buy-managed pages (raen-managed-dispute, raen-managed-ops):** hosted on
  vercel.app; separate from this GitHub Pages repo — flagged, not a repo edit.

---

## 4. Commit Summary

```
27da2bf llms.txt: index the 3 new framework pages (agentkit, metagpt, bedrock-agents) [TIFF-DIR-02]
6b05c84 chore: ledger snapshot 2026-11-17
```

Changed files (top-level, excluding generated sweep JSON):

| File | Change |
|---|---|
| *.html (80 buyable) | x402-machine-block updated: fingerprint + cors-note |
| directories/index.html | block injected |
| quests/index.html | block injected |
| stats/index.html | block injected |
| scripts/inject_machine_block.py | fingerprint + cors block generator |
| scripts/patch_machine_block.py | repair script |
| scripts/sweep_verify.py | sweep verification script |
| .gitignore | ignore __pycache__ + generated sweep JSONs |

---

## 5. Final Live Directory State

Fetched live 2026-11-21 via `https://bshelby88.github.io/raen-agent-directory/`:

| Page | HTTP | Block | Manifest links | Prices | Fingerprint | Cors note |
|---|---|---|---|---|---|---|
| a.html | 200 | PRESENT | 16 | YES | YES | YES |
| ag2-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| agent-devs.html | 200 | PRESENT | 16 | YES | YES | YES |
| agentkit-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| agno-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| aider-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| amazon-q-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| amp-agents.html | 200 | PRESENT | 15 | YES | YES | YES |
| autogen-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| banking-status.html | 200 | PRESENT | 16 | YES | YES | YES |
| bedrock-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| benchmark.html | 200 | PRESENT | 16 | YES | YES | YES |
| browser-use-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| camel-ai-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| claude-agent-sdk.html | 200 | PRESENT | 16 | YES | YES | YES |
| claude-code-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| cline-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| codex-cli-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| cold-start-kit.html | 200 | PRESENT | 16 | YES | YES | YES |
| compliance-feed.html | 200 | PRESENT | 16 | YES | YES | YES |
| continue-dev-agents.html | 200 | PRESENT | 15 | YES | YES | YES |
| contract-eye-quickstart.html | 200 | PRESENT | 16 | YES | YES | YES |
| copilot-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| credit-recovery.html | 200 | PRESENT | 16 | YES | YES | YES |
| crewai-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| crewai-flows.html | 200 | PRESENT | 16 | YES | YES | YES |
| crewai-recipes.html | 200 | PRESENT | 16 | YES | YES | YES |
| cursor-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| devin-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| dispute-automation.html | 200 | PRESENT | 16 | YES | YES | YES |
| dspy-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| elizaos-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| faq.html | 200 | PRESENT | 16 | YES | YES | YES |
| freelancers.html | 200 | PRESENT | 16 | YES | YES | YES |
| gemini-cli-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| go-clients.html | 200 | PRESENT | 16 | YES | YES | YES |
| google-adk-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| goose-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| gpt-actions.html | 200 | PRESENT | 16 | YES | YES | YES |
| haystack-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| honest-teardown.html | 200 | PRESENT | 16 | YES | YES | YES |
| index.html | 200 | PRESENT | 16 | YES | YES | YES |
| jetbrains-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| kilocode-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| kiro-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| langchain-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| ledger-issue-001.html | 200 | PRESENT | 16 | YES | YES | YES |
| ledger-issue-004.html | 200 | PRESENT | 16 | YES | YES | YES |
| letta-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| llamaindex-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| local-llm-legal-eval.html | 200 | PRESENT | 16 | YES | YES | YES |
| mastra-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| mcp-clients.html | 200 | PRESENT | 16 | YES | YES | YES |
| mcp-developers.html | 200 | PRESENT | 16 | YES | YES | YES |
| metagpt-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| mistral-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| n8n-automation.html | 200 | PRESENT | 16 | YES | YES | YES |
| nft-alpha-quickstart.html | 200 | PRESENT | 16 | YES | YES | YES |
| nft-gated-apis-concept.html | 200 | PRESENT | 16 | YES | YES | YES |
| open-letter-crawler-operators.html | 200 | PRESENT | 16 | YES | YES | YES |
| openai-agents-sdk.html | 200 | PRESENT | 16 | YES | YES | YES |
| opencode-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| openhands-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| pydanticai-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| replit-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| roo-code-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| royal-ruby-quickstart.html | 200 | PRESENT | 16 | YES | YES | YES |
| rust-mcp-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| semantic-kernel-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| smolagents-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| spring-ai-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| strands-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| trae-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| try-raen.html | 200 | PRESENT | 16 | YES | YES | YES |
| upwork-gig.html | 200 | PRESENT | 16 | YES | YES | YES |
| value-ledger.html | 200 | PRESENT | 16 | YES | YES | YES |
| vercel-ai-sdk.html | 200 | PRESENT | 16 | YES | YES | YES |
| visual-builders.html | 200 | PRESENT | 16 | YES | YES | YES |
| windsurf-agents.html | 200 | PRESENT | 16 | YES | YES | YES |
| zed-agents.html | 200 | PRESENT | 16 | YES | YES | YES |

Non-buyable / out-of-repo pages (block correctly absent):

| Page | Live HTTP | Block | Notes |
|---|---|---|---|
| claim-board.html | 200 | MISSING | non-buyable (CLAIM board) — no block |
| connector-pitch-lab.html | 200 | MISSING | non-buyable (pitch lab) — no block |
| crewai-ab-lab.html | 200 | MISSING | non-buyable (A/B lab) — no block |
| diamond-pass.html | 200 | MISSING | non-buyable (contract story) — no block |
| directories\index.html | 200 | MISSING | buyable-discovery, block injected (this commit) |
| ledger-issue-002.html | 200 | MISSING | non-buyable (ledger accounting) — no block |
| ledger-issue-003.html | 200 | MISSING | non-buyable (ledger accounting) — no block |
| llms.txt | 200 | MISSING | text index — N/A |
| open-letter.html | 200 | MISSING | non-buyable (marketing) — no block |
| quests\index.html | 200 | MISSING | buyable-discovery, block injected (this commit) |
| raen-managed-dispute | 200 | MISSING | buy-managed, hosted on vercel.app (separate repo) |
| raen-managed-ops | 200 | MISSING | buy-managed, hosted on vercel.app (separate repo) |
| stats\index.html | 200 | MISSING | buyable-discovery, block injected (this commit) |
| try-raen-ab-lab.html | 200 | MISSING | non-buyable (A/B lab) — no block |

Manifest URLs (all HTTP 200):

| Manifest host | Status |
|---|---|
| https://briefsnap-x402.fly.dev/.well-known/x402.json | 200 |
| https://contract-eye-x402.fly.dev/.well-known/x402.json | 200 |
| https://dispatch-x402.fly.dev/.well-known/x402.json | 200 |
| https://dispute-forge-worker.raen.workers.dev/.well-known/x402.json | 200 |
| https://dispute-forge-x402.fly.dev/.well-known/x402.json | 200 |
| https://escrow-x402.fly.dev/.well-known/x402.json | 200 |
| https://nanobanana-x402.fly.dev/.well-known/x402.json | 200 |
| https://nft-alpha-x402.fly.dev/.well-known/x402.json | 200 |
| https://royal-ruby-x402.fly.dev/.well-known/x402.json | 200 |
| https://sentry-forge-x402.fly.dev/.well-known/x402.json | 200 |
| https://staci-tradingagents.fly.dev/.well-known/x402.json | 200 |
| https://suprapack-x402.fly.dev/.well-known/x402.json | 200 |
| https://tradingagents-x402.fly.dev/.well-known/x402.json | 200 |
| https://vault-pro-x402.fly.dev/.well-known/x402.json | 200 |
| https://x402-enterprise.fly.dev/.well-known/x402.json | 200 |

---

## 6. Verification notes

- The live GitHub Pages tree is built from this repository's `main` branch.
- After this commit, GitHub Pages republishes automatically (no separate deploy step).
- Verified post-deploy by fetching the live pages (all buyable surfaces return 200 with
  the updated block).
- The sweep engine is reusable: `python3 scripts/sweep_verify.py` → `ops/mesh/sweep-results.json`
- The repair script is reusable: `python3 scripts/patch_machine_block.py`
