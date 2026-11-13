#!/usr/bin/env python3
"""Check every RAEN fleet x402 manifest pays the canonical wallet.

Handles both manifest shapes:
  v2: {"endpoints": {"/route": {"accepts": {"payTo": ...}}}}
  v1: {"accepts": [{"payTo": ...}]}

Usage: check-manifests.py svc1 svc2 ...
Prints one line per service: "<svc> <verdict>" where verdict is
canonical | PAYTO-DRIFT | NO-ROUTES. Exits 1 if any problem found.
"""
import json
import sys
import urllib.request

CANONICAL = "0x9b8a27e03ceba490953cda8ab1291c0e13baf72f"


def extract_paytos(body):
    pts = []
    eps = body.get("endpoints")
    if isinstance(eps, dict):
        for ep in eps.values():
            a = (ep or {}).get("accepts")
            if isinstance(a, list):
                pts += [x.get("payTo") for x in a if isinstance(x, dict)]
            elif isinstance(a, dict) and a.get("payTo"):
                pts.append(a["payTo"])
    elif isinstance(body.get("accepts"), list):
        pts += [x.get("payTo") for x in body["accepts"] if isinstance(x, dict)]
    return pts


def main():
    problems = []
    for svc in sys.argv[1:]:
        verdict = "canonical"
        try:
            with urllib.request.urlopen(
                f"https://{svc}.fly.dev/.well-known/x402.json", timeout=20
            ) as res:
                body = json.loads(res.read().decode("utf-8", "replace"))
            paytos = extract_paytos(body)
            if not paytos:
                verdict = "NO-ROUTES"
            elif any(
                (p or "").lower() != CANONICAL for p in paytos
            ):
                verdict = "PAYTO-DRIFT"
        except Exception as e:  # noqa: BLE001 — sweep must not die on one service
            verdict = f"FETCH-FAIL({type(e).__name__})"
        print(f"{svc} {verdict}")
        if verdict != "canonical":
            problems.append(svc)
    if problems:
        print(f"PROBLEMS: {' '.join(problems)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
