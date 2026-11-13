# RAEN ALWAYS-ON ARCHITECTURE (Nov 13, 2026)

Mission: remove the laptop single-point-of-failure from RAEN's brain. The
laptop Hermes cron jobs (10 in `AppData/Local/hermes/cron/jobs.json`) are
agent-reasoning loops; their MECHANICAL sweeps now also run laptop-free.

## Layer 1 — raen-brain (Fly, always-on)

App `raen-brain` (https://raen-brain.fly.dev), one shared-cpu-1x machine in
`ord`, `auto_stop_machines = "off"`, source in `~/RAEN/raen-brain/`.

- Scripted sweep endpoints (POST): `/cron/fleet-health` (14 endpoints, Steward
  cadence 4h), `/cron/ledger-check` (2h), `/cron/reply-poll` (2h, IMAP via
  GMAIL_USER/GMAIL_APP_PASSWORD Fly secrets), `/cron/manifest-check` (12h,
  payTo integrity vs canonical 0x9b8a...f72f). `GET /cron/status` = last runs.
- Scheduling: supercronic in the image (`crontab` file) hitting localhost.
  NOTE: Fly.io has NO `[cron]` section in fly.toml — supercronic IS the
  Fly-native cron pattern (docs.fly.io/blueprints/supercronic).
- Keep EXACTLY ONE machine: two machines = every job fires twice
  (`fly scale count 1 -a raen-brain`).
- Manual trigger any job: `curl -X POST https://raen-brain.fly.dev/cron/<job>`.
- reply-poll is a watchtower (unseen count + subjects); real-lead escalation
  and outbound replies stay with the laptop Franklin cycle.

## Layer 2 — GitHub Actions (bshelby88/raen-agent-directory, free)

Independent second opinion; both layers must fail before a sweep is lost.

- `fleet-health.yml` (every 4h): curls the same 14 endpoints, files a
  deduplicated issue on any 000, fails the run.
- `ledger-truth.yml` (daily 06:10 UTC): fetches settlement-collector
  `/ledger.json`, commits `stats/ledger/snapshot-<date>.json` to the repo —
  revenue truth survives every outage. Files an issue if unreachable.
- `marketplace-watch.yml` (daily 07:25 UTC): x402scan + AgentCash reachable,
  all 11 fleet manifests pay the canonical wallet (`scripts/check-manifests.py`).
  PAYTO-DRIFT = money misrouting — fix from source and REDEPLOY (secrets set
  does not refresh a running machine).

## Still laptop-bound (agent reasoning, not scriptable yet)

Steward judgment/repairs, Bean backlog execution, Tiffany/CROWN creative +
backlog cycles, Franklin outbound sending, Archaeologist discovery, Closer
sweep, JuanTerry leads, A2A commerce cycle, monthly competitive digest.

## Upgrade path

1. Move A2A cycle script to raen-brain (it is already `node a2a-cycle.mjs`).
2. On-chain USDC balance watch as a 5th /cron job (public Base RPC eth_call).
3. Trigger laptop agent jobs from raen-brain via a Hermes webhook when the
   laptop is up (brain becomes primary, laptop becomes optional).
4. If raen-brain itself must not be a SPOF: add a second region/machine with
   leader-lock, or accept Layer 2 as the fallback (current state).
