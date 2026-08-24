# booking-agent-profile

Shared, **keyless** USP/UCP platform profile for the USP Agent.

**Canonical URL:** `https://profile.booking-agent.dev/platform-profile.json`

Public hosting repo: [`wix/booking-agent-profile`](https://github.com/wix/booking-agent-profile).

**Publisher of record:** `https://profile.booking-agent.dev/platform-profile.json` (GitHub Pages custom domain on this repo; HTTPS enforced).

`https://wix.github.io/booking-agent-profile/platform-profile.json` 301s to the canonical URL. Personal cutover `https://yahalomran.github.io/booking-agent-profile/platform-profile.json` remains until an explicit retirement.

Wix DNS CNAME host `profile` points at `wix.github.io`. Do not edit apex or `www` A records.

## Source of truth

Content is generated from `platform_profile_doc()` in [`yahalomran/linkusp-cli`](https://github.com/yahalomran/linkusp-cli). This repo **publishes** the committed `platform-profile.json` artifact and validates it (schema + keyless). Do not hand-edit the JSON as a second SoT.

## Validate locally

```bash
python3 tools/build.py
python3 -m pytest -q
```
