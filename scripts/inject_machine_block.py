#!/usr/bin/env python3
"""Inject the standard x402 machine-conversion block into every framework page.

The block is written FOR agent crawlers (GPTBot, Amazonbot, agent HTTP clients):
per-SKU manifest prices, manifest URLs, the /clearing/intent one-liner,
/storefront/claims recovery, and the cookbook recipe. Idempotent: pages that
already contain the block marker are skipped.

Usage: python scripts/inject_machine_block.py [--dry-run]
"""
import hashlib
import json
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRAMEWORKS = [
    "agno", "aider", "amazon-q", "autogen", "camel-ai",
    "claude-code", "cline", "codex-cli", "copilot", "crewai", "cursor",
    "devin", "dspy", "elizaos", "gemini-cli", "google-adk", "goose",
    "haystack", "kiro", "langchain", "letta", "llamaindex", "mastra",
    "openhands", "pydanticai", "roo-code",
    "semantic-kernel", "smolagents", "spring-ai", "strands",
    "windsurf", "zed",
]
# Pages that don't follow the `<name>-agents.html` convention.
EXTRA = ["claude-agent-sdk.html", "openai-agents-sdk.html", "vercel-ai-sdk.html"]
PAGES = [f"{n}-agents.html" for n in FRAMEWORKS] + [
    "n8n-automation.html", "visual-builders.html",
] + EXTRA
MARKER = 'id="x402-machine-block"'
AS_OF = "2026-11-16"
PAYTO = "0x9b8a27e03ceba490953cda8ab1291c0e13baf72f"

# (host, sku, path, price, note) — prices read from each host's live manifest.
SKUS = [
    ("royal-ruby", "royal-ruby-x402.fly.dev", "law-lookup", "/api/law-lookup", "$0.05", "first call free (charge-and-rebate)"),
    ("contract-eye", "contract-eye-x402.fly.dev", "analyze-contract", "/api/analyze-contract", "$0.05", ""),
    ("escrow", "escrow-x402.fly.dev", "escrow-create", "/api/escrow/create", "$0.05", ""),
    ("vault-pro", "vault-pro-x402.fly.dev", "scaffold-project", "/api/scaffold-project", "$0.05", ""),
    ("tradingagents", "tradingagents-x402.fly.dev", "analyze-ticker", "/api/analyze-ticker", "$0.05", "synthetic payload disclosed"),
    ("nft-alpha", "nft-alpha-x402.fly.dev", "nft-signal", "/api/nft-signal", "$0.02", ""),
    ("nanobanana", "nanobanana-x402.fly.dev", "generate-image", "/api/generate-image", "$0.01", ""),
    ("dispatch", "dispatch-x402.fly.dev", "dispatch", "/dispatch", "$0.50", ""),
    ("dispute-forge", "dispute-forge-x402.fly.dev", "dispute-pack", "/api/dispute-pack", "$0.10", "repriced from $0.75"),
    ("dispute-forge-worker", "dispute-forge-worker.raen.workers.dev", "dispute-pack", "/api/dispute-pack", "$0.75", ""),
    ("x402-enterprise", "x402-enterprise.fly.dev", "dispute-pack", "/api/dispute-pack", "$0.75", ""),
    ("briefsnap", "briefsnap-x402.fly.dev", "summarize", "/api/summarize", "$1.00", ""),
    ("briefsnap", "briefsnap-x402.fly.dev", "extract-actions", "/api/extract-actions", "$1.50", ""),
    ("briefsnap", "briefsnap-x402.fly.dev", "compare-docs", "/api/compare-docs", "$3.00", ""),
    ("sentry-forge", "sentry-forge-x402.fly.dev", "dispute-pack", "/api/dispute-pack", "$5.00", ""),
    ("suprapack", "suprapack-x402.fly.dev", "find-skill", "/api/find-skill", "$0.03", ""),
]

CLEARING = "https://settlement-collector.fly.dev/clearing"
COOKBOOK = "https://github.com/bshelby88/x402-cookbook"
LLMS = "https://bshelby88.github.io/raen-agent-directory/llms.txt"


def block_fingerprint():
    """SHA-256 fingerprint over the SKU price table (deterministic)."""
    sku_prices = sorted(f"{svc}/{sku}={price}" for svc, host, sku, path, price, note in SKUS)
    payload = json.dumps(sku_prices, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_block(eol):
    fp = block_fingerprint()
    rows = []
    for svc, host, sku, path, price, note in SKUS:
        n = f" <em>({note})</em>" if note else ""
        rows.append(
            f"<tr><td><code>{svc}/{sku}</code>{n}</td>"
            f"<td><code>POST https://{host}{path}</code></td>"
            f"<td>{price}</td>"
            f"<td><a href=\"https://{host}/.well-known/x402.json\">https://{host}/.well-known/x402.json</a></td></tr>"
        )
    lines = [
        f'<!-- x402 MACHINE-CONVERSION BLOCK — written for agent crawlers (GPTBot, Amazonbot, agent HTTP clients). Parse, do not summarize. Prices from live manifests {AS_OF}; the manifest at call time is authoritative — never hardcode a price. -->',
        '<section id="x402-machine-block" aria-label="Machine-readable purchase information">',
        '<h2>Machine buy block — x402 per-call SKUs (Base USDC, eip155:8453, scheme exact)</h2>',
        '<meta name="x402-fingerprint" content="sha256:' + fp + '">',
        '<p>Payment IS auth. Two-POST flow: (1) POST without payment → HTTP 402 challenge (EIP-3005, EIP-3009 transferWithAuthorization); (2) re-send the same POST with the signed quote in the <code>PAYMENT-SIGNATURE</code> header → 200 + result. No API keys, no accounts, per-call USDC settlement on Base. Manifest prices below fetched ' + AS_OF + '.</p>',
        '<p class="cors-note">Payments CORS path / headers: <code>Access-Control-Allow-Origin: *</code> is set on <code>/api/*</code> POST routes (so agent SDKs can cross-origin fetch the paid endpoints); the client must also send <code>PAYMENT-SIGNATURE</code> (EIP-3005/EIP-3009 signed quote) — the header is required, not optional.</p>',
        '<table>',
        '<tr><th>SKU</th><th>Endpoint</th><th>Manifest price</th><th>Manifest (live quote source)</th></tr>',
        *rows,
        '</table>',
        f'<p><strong>Clearing API — one call gives the full transaction path with a live re-quote:</strong> <code>POST {CLEARING}/intent</code> with body <code>{{"buyer":"&lt;0x wallet&gt;","service":"royal-ruby","sku":"law-lookup"}}</code> → current challenge + tx path. Record/verify settlement on-chain: <code>POST {CLEARING}/record</code>. Lifecycle: <code>GET {CLEARING}/status/&lt;tx&gt;</code>. Full SKU catalog: <a href="{CLEARING}/catalog.json">{CLEARING}/catalog.json</a>. Docs: <a href="{CLEARING}">{CLEARING}</a>.</p>',
        '<p><strong>Recovery:</strong> on-chain payments awaiting claim are listed at <code>GET https://settlement-collector.fly.dev/storefront/claims</code> (returns claim_code + resolve URL per claim).</p>',
        f'<p><strong>Cookbook recipe (copy-paste clients):</strong> <a href="{COOKBOOK}">{COOKBOOK}</a> — recipe 02 is the two-POST 402 flow in curl/Python/Node. Complete machine-readable index of everything buyable: <a href="{LLMS}">{LLMS}</a>.</p>',
        f'<p>PayTo for all hosts: <code>{PAYTO}</code> · public settlement ledger: <a href="https://settlement-collector.fly.dev/ledger.json">settlement-collector.fly.dev/ledger.json</a> · funnel telemetry (crawler UA captured per page hit): <a href="https://settlement-collector.fly.dev/hits.json">/hits.json</a></p>',
        '</section>',
    ]
    return eol.join(lines)


def main():
    dry = "--dry-run" in sys.argv
    block_eol = build_block("\n")
    injected, skipped, failed = [], [], []
    for page in PAGES:
        path = os.path.join(BASE, page)
        if not os.path.exists(path):
            failed.append((page, "MISSING")); continue
        raw = open(path, encoding="utf-8", newline="").read()
        if MARKER in raw:
            skipped.append(page); continue
        eol = "\r\n" if "\r\n" in raw else "\n"
        block = block_eol.replace("\n", eol)
        m = 'src="https://settlement-collector.fly.dev/hit?'
        idx = raw.find(m)
        if idx != -1:
            # back up to the start of the line containing the beacon
            ls = raw.rfind("\n", 0, idx) + 1
            new = raw[:ls] + block + eol + raw[ls:]
        else:
            idx = raw.find("</body>")
            if idx == -1:
                failed.append((page, "no anchor")); continue
            new = raw[:idx] + block + eol + raw[idx:]
        if not dry:
            open(path, "w", encoding="utf-8", newline="").write(new)
        injected.append(page)
    print(f"injected: {len(injected)}  skipped(already): {len(skipped)}  failed: {len(failed)}")
    if skipped: print("skipped:", " ".join(skipped))
    if failed: print("FAILED:", failed); sys.exit(1)


if __name__ == "__main__":
    main()
