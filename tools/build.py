#!/usr/bin/env python3
"""Validate the committed platform-profile.json (hosting CI; does not own content)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "platform-profile.json"
USP_DIR = ROOT / "schemas" / "usp"
UCP_DIR = ROOT / "schemas" / "ucp"

FORBIDDEN = ("keys", "signing_keys", "webhook_url")
USP_ORIGIN = re.compile(r"^https://usp-protocol\.dev/")
UCP_ORIGIN = re.compile(r"^https://ucp\.dev/")
USP_CAP_PREFIX = "dev.usp-protocol."
LEGACY_USP_MARKERS = ("https://usp.dev", "dev.usp.services")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_keyless(doc: dict) -> None:
    blob = json.dumps(doc)
    for key in FORBIDDEN:
        if f'"{key}"' in blob:
            raise SystemExit(f"FAIL: keyless invariant: found {key!r}")


def _assert_capability_entries(doc: dict) -> None:
    for ns, block_name in (("usp", "usp"), ("ucp", "ucp")):
        block = doc.get(block_name) or {}
        caps = block.get("capabilities") or {}
        if not isinstance(caps, dict) or not caps:
            raise SystemExit(f"FAIL: {block_name}.capabilities must be a non-empty object")
        for name, entries in caps.items():
            if not isinstance(entries, list) or not entries:
                raise SystemExit(f"FAIL: empty capability array for {name}")
            for entry in entries:
                for field in ("version", "spec", "schema"):
                    if not isinstance(entry.get(field), str) or not entry[field]:
                        raise SystemExit(f"FAIL: {name} entry missing {field}")
                if name.startswith(USP_CAP_PREFIX) and not USP_ORIGIN.match(entry["spec"]):
                    raise SystemExit(
                        f"FAIL: {name} spec origin must be https://usp-protocol.dev"
                    )
                if name.startswith(USP_CAP_PREFIX) and not USP_ORIGIN.match(entry["schema"]):
                    raise SystemExit(
                        f"FAIL: {name} schema origin must be https://usp-protocol.dev"
                    )
                if name.startswith("dev.usp.") and not name.startswith(USP_CAP_PREFIX):
                    raise SystemExit(f"FAIL: leftover pre-cutover capability {name}")
                if name.startswith("dev.ucp.") and not UCP_ORIGIN.match(entry["spec"]):
                    raise SystemExit(f"FAIL: {name} spec origin must be ucp.dev")
                if name.startswith("dev.ucp.") and not UCP_ORIGIN.match(entry["schema"]):
                    raise SystemExit(f"FAIL: {name} schema origin must be ucp.dev")


def _assert_rest_only(doc: dict) -> None:
    services = ((doc.get("usp") or {}).get("services") or {})
    for svc, entries in services.items():
        for entry in entries:
            transport = entry.get("transport")
            if transport != "rest":
                raise SystemExit(f"FAIL: {svc} must advertise rest only, got {transport!r}")


def _registry_for(dir_path: Path, base_uri: str):
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    resources = []
    for path in dir_path.rglob("*.json"):
        rel = path.relative_to(dir_path).as_posix()
        uri = urljoin(base_uri, rel)
        contents = _load(path)
        resource = Resource.from_contents(contents, default_specification=DRAFT202012)
        resources.append((uri, resource))
        file_id = contents.get("$id")
        if isinstance(file_id, str) and file_id and file_id != uri:
            resources.append((file_id, resource))
    return Registry().with_resources(resources)


def _validate_usp_platform_profile(doc: dict) -> None:
    from jsonschema import Draft202012Validator

    registry = _registry_for(USP_DIR, "https://usp-protocol.dev/schemas/")
    validator = Draft202012Validator(
        {"$ref": "https://usp-protocol.dev/schemas/profile.json#/$defs/PlatformProfile"},
        registry=registry,
    )
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors[:8])
        raise SystemExit(f"FAIL: USP PlatformProfile: {msgs}")


def _validate_ucp_platform_schema(doc: dict) -> None:
    from jsonschema import Draft202012Validator

    ucp = doc.get("ucp")
    if not isinstance(ucp, dict):
        raise SystemExit("FAIL: missing ucp object")
    # UCP `propertyNames` still rejects hyphens, so `dev.usp-protocol.*` cannot
    # sit in the same map as `dev.ucp.*` under a strict UCP validator. USP-owned
    # keys are origin-bound separately in `_assert_capability_entries`.
    filtered = dict(ucp)
    caps = dict(ucp.get("capabilities") or {})
    filtered["capabilities"] = {
        name: entries
        for name, entries in caps.items()
        if not name.startswith(USP_CAP_PREFIX)
    }
    if not filtered["capabilities"]:
        raise SystemExit("FAIL: ucp.capabilities has no UCP-owned entries after filtering")
    registry = _registry_for(UCP_DIR, "https://ucp.dev/schemas/")
    validator = Draft202012Validator(
        {"$ref": "https://ucp.dev/schemas/ucp.json#/$defs/platform_schema"},
        registry=registry,
    )
    errors = sorted(validator.iter_errors(filtered), key=lambda e: list(e.path))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors[:8])
        raise SystemExit(f"FAIL: UCP platform_schema: {msgs}")


def _assert_cutover(doc: dict) -> None:
    blob = json.dumps(doc)
    for marker in LEGACY_USP_MARKERS:
        if marker in blob:
            raise SystemExit(f"FAIL: leftover pre-cutover marker {marker!r}")
    services = ((doc.get("usp") or {}).get("services") or {})
    if "dev.usp-protocol.services" not in services:
        raise SystemExit("FAIL: usp.services must advertise dev.usp-protocol.services")


def main() -> int:
    if not ARTIFACT.is_file():
        print(f"FAIL: missing {ARTIFACT}", file=sys.stderr)
        return 1
    doc = _load(ARTIFACT)
    _assert_keyless(doc)
    _assert_cutover(doc)
    _assert_capability_entries(doc)
    _assert_rest_only(doc)
    _validate_usp_platform_profile(doc)
    _validate_ucp_platform_schema(doc)
    print("OK: platform-profile.json validates (keyless + USP PlatformProfile + UCP platform_schema)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
