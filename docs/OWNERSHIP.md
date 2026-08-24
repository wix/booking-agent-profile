# USP Agent platform profile - ownership

Canonical profile URI (platform identity; do not change lightly):

`https://profile.booking-agent.dev/platform-profile.json`

| Asset | Owner |
|-------|-------|
| Domain `booking-agent.dev` | Wix DNS / domain registrant for `booking-agent.dev` |
| GitHub repo `booking-agent-profile` | Public org [`wix`](https://github.com/wix/booking-agent-profile) |
| GitHub Pages publisher | `wix/booking-agent-profile` serving the canonical URI (source: `main` / root) |
| Profile document content | Published from the committed `platform-profile.json` in this repository. This repo validates and hosts; it is not a second authoring source. |

## Who can transfer what

- **Domain transfer / registrar changes:** domain registrant for `booking-agent.dev` (Wix Domains).
- **Repo admin / transfer:** `wix` org owners (this repo). Do not recreate; prefer history-preserving moves.
- **DNS for the profile host:** whoever can edit Wix DNS for `booking-agent.dev`. Apex and `www` records serve the live Wix site and must not be used for this profile.
- **GitHub org domain verification:** `wix` org owners, via org Settings -> Pages -> Verified domains.

## Rotation of neither

This document is keyless. There are no profile signing keys to rotate. Proof-of-possession keys are per-credential and ephemeral in the client; they are never published here.
