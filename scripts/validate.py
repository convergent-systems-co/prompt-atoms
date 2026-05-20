#!/usr/bin/env python3
"""Validate every atoms/<type>/*.json against schemas/atom-v1.json.

Per-atom checks: (1) JSON Schema validation; (2) `id` matches the filename
stem; (3) `type` matches the parent directory name.

Exit 0 on full pass; exit 1 on any failure.
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "atom-v1.json"
ATOMS_DIR = REPO / "atoms"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    files = sorted(ATOMS_DIR.rglob("*.json"))
    if not files:
        print(f"no atoms found under {ATOMS_DIR}", file=sys.stderr)
        return 1

    total_errors = 0
    for path in files:
        rel = path.relative_to(REPO)
        errors: list[str] = []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"✗ {rel}: invalid JSON ({e})")
            total_errors += 1
            continue

        for err in validator.iter_errors(data):
            loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
            errors.append(f"schema: {err.message} at {loc}")

        stem = path.stem
        if data.get("id") != stem:
            errors.append(f"id={data.get('id')!r} does not match filename stem {stem!r}")

        parent = path.parent.name
        if data.get("type") != parent:
            errors.append(f"type={data.get('type')!r} does not match parent dir {parent!r}")

        if errors:
            print(f"✗ {rel}")
            for e in errors:
                print(f"    {e}")
            total_errors += len(errors)
        else:
            print(f"✓ {rel}")

    if total_errors:
        print(f"\n{total_errors} error(s) across {len(files)} atom(s)")
        return 1
    print(f"\nall {len(files)} atom(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
