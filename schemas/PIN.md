# Schema pins

Vendored copies under `schemas/` are what hosting CI validates against.

| Schema | Pin |
|--------|-----|
| USP `profile.json` / `usp.json` | [`wix/universal-scheduling-protocol`](https://github.com/wix/universal-scheduling-protocol) commit `b0ccef6e9501162f97f505880d6c72a05e475517` (`master` as of 2026-09-11). This pin includes the `propertyNames` alphabet that admits `dev.usp-protocol.*` (public PR #14 / spec issue #239). |
| UCP `ucp.json` (plus capability / payment_handler / service) | tag `v2026-04-08` (`a2d8bf0b8f5a6fc790f677899c2c7da0684fe33d`) |

This repository validates the committed `platform-profile.json`. It does not author the document. Content is generated from `platform_profile_doc()` in `yahalomran/linkusp-cli`.

UCP `platform_schema` `propertyNames` still rejects hyphens, so hosting CI validates `dev.ucp.*` entries against that schema and origin-binds `dev.usp-protocol.*` keys separately. Do not revert `paid_bookings` to `dev.usp.services.paid_bookings` to satisfy the UCP regex.
