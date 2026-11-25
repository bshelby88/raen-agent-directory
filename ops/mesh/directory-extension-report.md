# Directory Extension & Buy-Path Surface — ops/mesh Report

**Covers:** 5 new machine-payable framework landing pages (agent, etcd-agent, openai-agents, crewai, langgraph)
**Pattern:** Tiffany framework-page pattern (per-SKU manifest, clearing intent, $0.001–$1.00 prices, linked recipes, in-feed cross-links)
**Date:** 2026-11-20
**Source repo:** `bshelby88/raen-agent-directory` (GitHub Pages: `https://bshelby88.github.io/raen-agent-directory/`)
**Commit:** `b7a8c5f` (`feat(directories): add 5 machine-payable framework landing pages`)

---

## 1. New pages (deployed + live)

| Surface | File | URL | HTTP |
|---------|------|-----|------|
| agent | `agent.html` | https://bshelby88.github.io/raen-agent-directory/agent.html | 200 |
| etcd-agent | `etcd-agent.html` | https://bshelby88.github.io/raen-agent-directory/etcd-agent.html | 200 |
| openai-agents | `openai-agents.html` | https://bshelby88.github.io/raen-agent-directory/openai-agents.html | 200 |
| crewai | `crewai.html` | https://bshelby88.github.io/raen-agent-directory/crewai.html | 200 |
| langgraph | `langgraph.html` | https://bshelby88.github.io/raen-agent-directory/langgraph.html | 200 |

Live-mirror repo sync: `/c/Users/jaded/RAEN/raen-agent-directory-live` (branch main @ b7a8c5f, upstream origin/main).

---

## 2. Verification (live, 2026-11-20)

Every page was fetched live and verified:

| Check | agent | etcd-agent | openai-agents | crewai | langgraph |
|-------|-------|------------|---------------|--------|-----------|
| HTTP 200 | ✔ | ✔ | ✔ | ✔ | ✔ |
| x402-machine-block section | ✔ | ✔ | ✔ | ✔ | ✔ |
| manifest URLs (`/well-known/x402.json`) | ✔ (≥1 per SKU row) | ✔ | ✔ | ✔ | ✔ |
| price range $0.001–$1.00 | ✔ | ✔ | ✔ | ✔ | ✔ |
| `payment-required` (402 field) | ✔ | ✔ | ✔ | ✔ | ✔ |
| `X-PAYMENT` (402 field) | ✔ | ✔ | ✔ | ✔ | ✔ |
| two-POST flow described | ✔ | ✔ | ✔ | ✔ | ✔ |
| framework wrapper example | ✔ | ✔ | ✔ | ✔ | ✔ |
| in-feed cross-links | ✔ | ✔ | ✔ | ✔ | ✔ |
| recipe index | ✔ | ✔ | ✔ | ✔ | ✔ |
| page-hit beacon | ✔ | ✔ | ✔ | ✔ | ✔ |

Manifest example (per SKU row):
```html
<tr><td><code>royal-ruby/law-lookup</code></td>
<td><code>POST https://royal-ruby-x402.fly.dev/api/law-lookup</code></td>
<td>$0.05</td>
<td><a href="https://royal-ruby-x402.fly.dev/.well-known/x402.json">/.well-known/x402.json</a></td></tr>
```

Clearing-intent block:
```http
POST https://settlement-collector.fly.dev/clearing/intent   # -> challenge + tx path
POST https://settlement-collector.fly.dev/clearing/record   # -> status: settled
GET  https://settlement-collector.fly.dev/clearing/status/<tx>
```

---

## 3. Buy-path treatment summary

Each page follows the Tiffany framework-page pattern:

1. **Kicker + title** — `RAEN · x402 paid APIs on Base` / `Paid tool calls in <framework> — x402 micro-priced endpoints (Base USDC)`.
2. **A/B harness** — deterministic 50/50 variant bucket (control `a` = mechanism, variant `b` = outcome) with session-persisted localStorage key `raen-ab-<slug>`.
3. **Four-step buy path** (cheapest first):
   - Step 1: `GET /api/ping` — **$0.001** (smallest first purchase, real on-chain settlement).
   - Step 2: `GET /api/udap-citations` — **$0** (10 most-cited state UDAP statutes, free tier).
   - Step 3: `POST /api/law-lookup` (charge-and-rebate, first call free) — **$0.05** challenge → net **$0**.
   - Step 4: bulk law-lookup (100+ citations) — **$0.001/citation** (min 100 = $0.10/call).
4. **Machine buy block** — per-SKU table with `SKU` / `Endpoint` / `Manifest price` / `Manifest URL` (`/.well-known/x402.json`).
5. **Clearing intent** — settlement-collector `/clearing/intent` + `/clearing/record` + `/clearing/status/<tx>`.
6. **Two-POST flow** + framework wrapper example (`@function_tool` for agents, `BaseTool` for CrewAI, etc.).
7. **Why pay-per-call** + **honest caveats** (fleet revenue, synthetic payloads, delivery modes, legal-advice disclaimer).
8. **In-feed cross-links** — `The same 30-line wrapper, other agent runtimes` (links to ag2, langchain, crewai, pydanticai, openai-agents-sdk, langgraph, etcd-agent, agent).
9. **Recipe index** — linked recipes for the framework builder (recipes, flows, recipes pages).
10. **Page-hit beacon** — funnel telemetry (`src=<slug>`, `<slug>-buy-path`, `<slug>-a/b`).

---

## 4. llms.txt updates

5 new entries appended to `llms.txt` (verified present in final file):

- agent.html
- etcd-agent.html
- openai-agents.html
- crewai.html
- langgraph.html

---

## 5. Commits

- `b7a8c5f` — `feat(directories): add 5 machine-payable framework landing pages (agent, etcd-agent, openai-agents, crewai, langgraph)`
  - Files: `agent.html`, `etcd-agent.html`, `openai-agents.html`, `crewai.html`, `langgraph.html`, `llms.txt`
- Rebased + pushed to `origin/main` (upstream of `e3d206d`).

---

## 6. Status & open items

- ✔ Pages deployed to GitHub Pages; live 200-verified.
- ✔ llms.txt entries added.
- ✔ Live mirror (`RAEN/raen-agent-directory-live`) synced.
- ✔ Verification (200 + manifest + price + 402 field) complete.
- ⏳ Benchmarking the A/B variant `b` vs `a` — decision rule at `crewai-ab-lab.html` (≥1.5× A demo rate on ≥100 loads/side).
- ⏳ External payer activity — 0 external payers to date; see live ledger (settlement-collector.fly.dev/ledger).
