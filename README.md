# booking-agent-profile

Shared, **keyless** USP/UCP platform profile for the USP Agent.

**Canonical URL:** `https://profile.booking-agent.dev/platform-profile.json`

Public hosting repo: [`wix/booking-agent-profile`](https://github.com/wix/booking-agent-profile).

**Cutover Pages URLs** (issue [#114](https://github.com/wix-private/universal-scheduling-protocol-spec/issues/114) Step 10):

- Org (target): `https://wix.github.io/booking-agent-profile/platform-profile.json`
- Personal (keep until org serves identical bytes): `https://yahalomran.github.io/booking-agent-profile/platform-profile.json`

Do not bind `profile.booking-agent.dev` until org Pages is serving. CNAME host name `profile` must point at `wix.github.io` only. Do not edit apex or `www` A records.

## Source of truth

Content is generated from `platform_profile_doc()` in [`yahalomran/linkusp-cli`](https://github.com/yahalomran/linkusp-cli). This repo **publishes** the committed `platform-profile.json` artifact and validates it (schema + keyless). Do not hand-edit the JSON as a second SoT.

## Validate locally

```bash
python3 tools/build.py
python3 -m pytest -q
```
