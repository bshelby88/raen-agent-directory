#!/usr/bin/env python3
"""Apply the machine-buy block repair to all pages.

1. For each of the 80 pages that already carry the block, replace the block
   with the updated block (adds x402-fingerprint meta + cors-note).
2. For the 3 buyable-discovery subdir pages, inject the block.
3. The 8 non-buyable pages are intentionally left untouched (not buyable
   surfaces, so no machine-conversion block is required).
4. Buy-managed pages (raen-managed-dispute, raen-managed-ops) are hosted on
   vercel.app, separate from this GitHub Pages repo — out of scope.
"""
import importlib.util
import os
import sys

REPO = "C:/Users/jaded/GitHub/raen-agent-directory"

# Import the block builder from the inject script (now has fingerprint + cors)
spec = importlib.util.spec_from_file_location(
    "inject", os.path.join(REPO, "scripts", "inject_machine_block.py")
)
inject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inject)

NEW_BLOCK = inject.build_block("\n")
NEW_BLOCK_CRLF = inject.build_block("\r\n")

PAGES_WITH_BLOCK = [
    "a.html", "ag2-agents.html", "agent-devs.html", "agentkit-agents.html",
    "agno-agents.html", "aider-agents.html", "amazon-q-agents.html",
    "amp-agents.html", "autogen-agents.html", "banking-status.html",
    "bedrock-agents.html", "benchmark.html", "browser-use-agents.html",
    "camel-ai-agents.html", "claude-agent-sdk.html", "claude-code-agents.html",
    "cline-agents.html", "codex-cli-agents.html", "cold-start-kit.html",
    "compliance-feed.html",
    "continue-dev-agents.html", "contract-eye-quickstart.html",
    "copilot-agents.html", "credit-recovery.html", "crewai-recipes.html",
    "crewai-agents.html", "cursor-agents.html", "devin-agents.html",
    "crewai-flows.html", "dspy-agents.html", "elizaos-agents.html",
    "faq.html", "freelancers.html", "gemini-cli-agents.html",
    "go-clients.html", "google-adk-agents.html", "goose-agents.html",
    "gpt-actions.html", "haystack-agents.html", "honest-teardown.html",
    "index.html", "jetbrains-agents.html", "kilocode-agents.html",
    "kiro-agents.html", "langchain-agents.html", "ledger-issue-001.html",
    "ledger-issue-004.html", "letta-agents.html", "llamaindex-agents.html",
    "local-llm-legal-eval.html", "mastra-agents.html", "mcp-clients.html",
    "mcp-developers.html", "metagpt-agents.html", "mistral-agents.html",
    "n8n-automation.html", "nft-alpha-quickstart.html",
    "nft-gated-apis-concept.html", "open-letter-crawler-operators.html",
    "openai-agents-sdk.html", "opencode-agents.html", "openhands-agents.html",
    "pydanticai-agents.html", "replit-agents.html", "roo-code-agents.html",
    "royal-ruby-quickstart.html", "rust-mcp-agents.html",
    "semantic-kernel-agents.html", "smolagents-agents.html",
    "spring-ai-agents.html", "strands-agents.html", "trae-agents.html",
    "try-raen.html", "upwork-gig.html", "value-ledger.html",
    "vercel-ai-sdk.html", "visual-builders.html", "windsurf-agents.html",
    "zed-agents.html", "dispute-automation.html",
]

SUBDIR_PAGES = [
    ("directories", "index.html"),
    ("quests", "index.html"),
    ("stats", "index.html"),
]

def block_has_fingerprint(raw):
    return 'x402-fingerprint' in raw

def patch_page(path, new_block):
    with open(path, encoding="utf-8", newline="") as f:
        raw = f.read()
    eol = "\r\n" if "\r\n" in raw else "\n"
    if eol == "\r\n":
        new_block = NEW_BLOCK_CRLF
    else:
        new_block = NEW_BLOCK
    # Replace old block with new block
    old_block_marker = 'id="x402-machine-block"'
    if old_block_marker not in raw:
        print(f"  !! {path}: no block marker (expected?)")
        return False
    # Find block start and end
    idx_start = raw.find('<section id="x402-machine-block"')
    # Find the closing </section>
    idx_end = raw.find("</section>", idx_start)
    if idx_end == -1:
        print(f"  !! {path}: no closing section")
        return False
    idx_end += len("</section>")
    new_raw = raw[:idx_start] + new_block + raw[idx_end:]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_raw)
    print(f"  patched {path}")
    return True

def main():
    # 1. Patch the 80 pages (replace block)
    print("=== Patching 80 pages (replace block) ===")
    patched = 0
    for page in PAGES_WITH_BLOCK:
        path = os.path.join(REPO, page)
        if not os.path.exists(path):
            print(f"  !! {path} missing!"); continue
        with open(path, encoding="utf-8", newline="") as f:
            raw = f.read()
        if block_has_fingerprint(raw):
            print(f"  already patched: {page}"); continue
        if patch_page(path, NEW_BLOCK):
            patched += 1
    print(f"Patched: {patched}/{len(PAGES_WITH_BLOCK)}")

    # 2. Inject block into 3 subdir pages
    print("=== Injecting block into 3 subdir pages ===")
    for d, fn in SUBDIR_PAGES:
        path = os.path.join(REPO, d, fn)
        if not os.path.exists(path):
            print(f"  !! {path} missing!"); continue
        with open(path, encoding="utf-8", newline="") as f:
            raw = f.read()
        if block_has_fingerprint(raw):
            print(f"  already patched: {d}/{fn}"); continue
        # Insert before </body>
        idx = raw.rfind("</body>")
        if idx == -1:
            print(f"  !! {path}: no </body> anchor"); continue
        new_raw = raw[:idx] + NEW_BLOCK + raw[idx:]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_raw)
        print(f"  injected: {d}/{fn}")

if __name__ == "__main__":
    main()
