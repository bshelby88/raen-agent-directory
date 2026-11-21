#!/usr/bin/env python3
"""Machine-buyer funnel conversion-block sweep (optimized).

Fetches every top-level page + subdir pages + llms.txt + the two buy-managed
pages live, then verifies each carries:
  - live manifest URL (returning 200)
  - per-SKU x402 price
  - /clearing/intent one-liner
  - recipe links
  - fingerprint
  - payments header / cors path
and lists every 404, missing price, and missing block.
"""
import concurrent.futures
import json
import os
import re
import urllib.request
import urllib.error

REPO = "C:/Users/jaded/GitHub/raen-agent-directory"
LIVE = "https://bshelby88.github.io/raen-agent-directory"
LIVE_SUBDOMAIN = "https://bshelby88.github.io/raen-agent-directory"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
FETCH_TIMEOUT = 15

def fetch(url, timeout=FETCH_TIMEOUT):
    """Return (status, text). status 0 = no connection."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return r.status, data.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, f"FETCH-ERROR: {type(e).__name__}: {e}"

def find_machine_block(html):
    m = re.search(r'<!-- x402 MACHINE-CONVERSION BLOCK.*?-->\s*<section id="x402-machine-block".*?</section>', html, re.S)
    if m:
        return m.group(0)
    return None

def check_page(filename, is_local=False, live_url=None):
    """Return the results dict for one page."""
    res = {"page": filename, "source": "local" if is_local else "live",
           "local_status": 0, "live_status": 0, "size_local": 0, "size_live": 0}
    if is_local:
        path = os.path.join(REPO, filename)
        if not os.path.exists(path):
            res.update({"status": "MISSING-LOCAL"})
            return res
        with open(path, encoding="utf-8", newline="") as f:
            raw = f.read()
        res["local_status"] = 200
        res["size_local"] = len(raw)
        # also fetch live URL for status check
        live_url = (LIVE_SUBDOMAIN + "/" + filename).replace("\\", "/")
        status, _ = fetch(live_url)
        res["live_status"] = status
        res["size_live"] = 0
    else:
        url = live_url if live_url else (LIVE_SUBDOMAIN + "/" + filename if not filename.endswith(".txt") else LIVE + "/" + filename)
        status, raw = fetch(url)
        res["live_status"] = status
        res["size_live"] = len(raw)
        if status == 0:
            res.update({"status": "FETCH-ERROR", "error": raw[:200]})
            return res
        if status != 200:
            res.update({"status": "HTTP-" + str(status)})
            return res

    block = find_machine_block(raw)
    if block is None:
        res.update({"block": "MISSING", "block_reasons": []})
        return res
    res["block"] = "PRESENT"
    res["block_len"] = len(block)

    # 1. live manifest URL links + their http status
    manifest_links = re.findall(r'href="([^"]*\.well-known/x402\.json)"', block)
    res["manifest_links"] = manifest_links
    bad = []
    for ml in manifest_links:
        ms, _ = fetch(ml)
        if ms != 200:
            bad.append({"url": ml, "status": ms})
    res["manifest_404"] = bad

    # 2. per-SKU x402 price
    price_rows = re.findall(r'<tr><td><code>[^<]*</code></td><td><code>POST [^<]*</code></td><td>\$([0-9.]+)</td>', block)
    res["prices"] = price_rows
    res["has_prices"] = len(price_rows) > 0

    # 3. /clearing/intent one-liner
    res["has_clearing_intent"] = "clearing/intent" in block

    # 4. recipe links
    res["has_recipe"] = ("cookbook" in block.lower() or "recipe" in block.lower())

    # 5. fingerprint
    res["has_fingerprint"] = ("fingerprint" in block.lower())

    # 6. payments header / cors path
    res["has_payment_header_cors"] = ("cors" in block.lower() or
                                       "payments header" in block.lower() or
                                       "access-control" in block.lower())
    return res

def main():
    # --- page inventory ---
    top_html = sorted(f for f in os.listdir(REPO) if f.endswith(".html") and not f.startswith("."))
    sub_html = []
    for d in ["directories", "quests", "stats"]:
        p = os.path.join(REPO, d)
        if os.path.isdir(p):
            sub_html += [os.path.join(d, f) for f in sorted(os.listdir(p)) if f.endswith(".html")]
    sub_html.sort()
    top_html.sort()

    # Buy-managed pages live at their Vercel URLs (not GitHub Pages)
    BUY_MANAGED = {
        "raen-managed-dispute": "https://raen-managed-dispute.vercel.app/",
        "raen-managed-ops": "https://raen-managed-ops.vercel.app/",
    }

    target_pages = top_html + sub_html + ["llms.txt"] + list(BUY_MANAGED.keys())

    # Unique manifest URLs (14 hosts across all pages)
    unique_manifests = sorted(set(
        x for f in top_html + sub_html
        if os.path.exists(os.path.join(REPO, f))
        for x in re.findall(r'href="([^"]*\.well-known/x402\.json)"',
                            open(os.path.join(REPO, f), encoding="utf-8", errors="replace").read())
    ))

    # --- fetch pages in parallel ---
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        futures = []
        for fn in target_pages:
            if fn in BUY_MANAGED:
                # buy-managed: fetch live only, from Vercel
                futures.append(ex.submit(check_page, fn, is_local=False, live_url=BUY_MANAGED[fn]))
            elif fn == "llms.txt":
                # llms.txt: fetch live from GitHub Pages
                futures.append(ex.submit(check_page, fn, is_local=False))
            else:
                # local pages: check local file + fetch live for status
                futures.append(ex.submit(check_page, fn, is_local=True))
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())

    # --- manifest checks (once, shared) ---
    manifest_results = {}
    for ml in unique_manifests:
        ms, _ = fetch(ml)
        manifest_results[ml] = ms
    for r in results:
        bad = []
        for ml in r.get("manifest_links", []):
            if manifest_results.get(ml) != 200:
                bad.append({"url": ml, "status": manifest_results.get(ml)})
        r["manifest_404"] = bad

    # --- report ---
    print(f"{'PAGE':44s} {'SRC':5s} {'LIVE':>4s} {'SZ':>6s} {'BLOCK':>9s} {'PRICE':>5s} {'CLR':>3s} {'RCPE':>5s} {'FP':>3s} {'COR':>3s} {'M404':>5s}")
    for r in results:
        print(f"{r['page']:44s} {r['source']:5s} {str(r.get('live_status','-')):>4s} {str(r.get('size_live','-')):>6s} {str(r.get('block','-')):>9s} {str(r.get('has_prices','-')):>5s} {str(r.get('has_clearing_intent','-')):>3s} {str(r.get('has_recipe','-')):>5s} {str(r.get('has_fingerprint','-')):>3s} {str(r.get('has_payment_header_cors','-')):>3s} {str(len(r.get('manifest_404',[]))):>5s}")

    print("\n=== ISSUES ===")
    for r in results:
        for m in r.get("manifest_404", []):
            print(f"404 {r['page']} <- {m['url']} -> {m['status']}")
        if r.get("block") == "MISSING":
            print(f"MISSING BLOCK {r['page']}")
        if not r.get("has_prices"):
            print(f"NO PRICE {r['page']}")
        if not r.get("has_fingerprint"):
            print(f"MISSING fingerprint {r['page']}")
        if not r.get("has_payment_header_cors"):
            print(f"MISSING payments-header/cors {r['page']}")
        if r.get("live_status") == 0:
            print(f"FETCH-ERROR {r['page']} {r.get('error','')}")
        if r.get("live_status") != 200 and r.get("live_status", 200) != 200:
            print(f"HTTP-{r.get('live_status')} {r['page']}")

    # Write JSON
    os.makedirs(os.path.join(REPO, "ops", "mesh"), exist_ok=True)
    with open(os.path.join(REPO, "ops", "mesh", "sweep-results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    with open(os.path.join(REPO, "ops", "mesh", "manifest-checks.json"), "w") as f:
        json.dump(manifest_results, f, indent=2)

    print("\nWrote ops/mesh/sweep-results.json and ops/mesh/manifest-checks.json")

if __name__ == "__main__":
    main()
