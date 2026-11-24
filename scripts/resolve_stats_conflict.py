#!/usr/bin/env python3
"""Resolve the stats/index.html conflict."""
fp = "stats/index.html"
with open(fp, encoding="utf-8", newline="") as f:
    raw = f.read()

marker_start = "<<<<<<< HEAD"
marker_end = ">>>>>>> 6458ad0 (fix: apply x402 machine-buy conversion block (fingerprint + CORS) to all buyable surfaces)"
mid_marker = "======="

if marker_start in raw and mid_marker in raw and marker_end in raw:
    idx_start = raw.find(marker_start)
    idx_mid = raw.find(mid_marker, idx_start)
    idx_end = raw.find(marker_end, idx_mid)

    before = raw[:idx_start]

    # HEAD's version section: between marker_start and mid_marker
    head_section = raw[idx_start:idx_mid]

    # Mine's version section: between mid_marker and marker_end
    mine_section = raw[idx_mid:idx_end]

    # Extract the remote's footer (with raen-blog-x402.fly.dev) from head_section
    footer_start = head_section.find('<div style="max-width:560px')
    if footer_start != -1:
        footer = head_section[footer_start:footer_start + 300]
    else:
        footer = ""

    # Extract the machine block from mine_section
    machine_marker = "<!-- x402 MACHINE-CONVERSION BLOCK"
    machine_start = mine_section.find(machine_marker)
    if machine_start != -1:
        # Machine block extends to the end of the section
        machine_block = mine_section[machine_start:]
    else:
        machine_block = ""

    resolved = before + footer + machine_block + "</html>"
    with open(fp, "w", encoding="utf-8", newline="") as f:
        f.write(resolved)
    print("resolved stats/index.html")
    print("conflict markers remaining:", raw.count("<<<<<<<") + raw.count("=======") + raw.count(">>>>>>>"))
    print("footer present:", "raen-blog-x402.fly.dev" in resolved)
    print("machine block present:", "x402-machine-block" in resolved)
else:
    print("conflict markers not found; aborting")
