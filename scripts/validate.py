#!/usr/bin/env python3
"""Validate every atom, composition, and rule against its schema.

Per-file checks:
  atoms/<type>/<id>.json       → atom-v1.json; id == filename stem; type == parent dir
  prompts/<id>.json            → composition-v1.json; id == filename stem
  rules/<type>/<id>.json       → rule-v1.json; id == filename stem; type == parent dir

Composition references are resolved against the local tree; a missing or
version-mismatched ref is an error.

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
SCHEMAS = {
    "atom":        REPO / "schemas" / "atom-v1.json",
    "composition": REPO / "schemas" / "composition-v1.json",
    "rule":        REPO / "schemas" / "rule-v1.json",
}
ATOMS_DIR       = REPO / "atoms"
COMPOSITIONS_DIR = REPO / "prompts"
RULES_DIR       = REPO / "rules"

REF_PATTERN = "prompt-atoms://atoms/"


def load_validator(kind: str) -> jsonschema.Draft202012Validator:
    schema = json.loads(SCHEMAS[kind].read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def validate_atoms(validator) -> tuple[int, dict]:
    errors = 0
    atom_index: dict[str, dict] = {}
    for path in sorted(ATOMS_DIR.rglob("*.json")):
        rel = path.relative_to(REPO)
        local_errors = _validate_one(path, rel, validator)
        if not local_errors:
            data = json.loads(path.read_text(encoding="utf-8"))
            parent = path.parent.name
            if data.get("type") != parent:
                print(f"✗ {rel}")
                print(f"    type={data.get('type')!r} does not match parent dir {parent!r}")
                local_errors += 1
            else:
                key = f"prompt-atoms://atoms/{parent}/{data['id']}"
                atom_index[key] = data
                print(f"✓ {rel}")
        errors += local_errors
    return errors, atom_index


def validate_compositions(validator, atom_index: dict) -> int:
    errors = 0
    for path in sorted(COMPOSITIONS_DIR.glob("*.json")):
        rel = path.relative_to(REPO)
        local_errors = _validate_one(path, rel, validator)
        if not local_errors:
            data = json.loads(path.read_text(encoding="utf-8"))
            local_errors += _resolve_refs(data, atom_index, rel)
        if local_errors == 0:
            print(f"✓ {rel}")
        errors += local_errors
    return errors


def validate_rules(validator) -> int:
    errors = 0
    for path in sorted(RULES_DIR.rglob("*.json")):
        rel = path.relative_to(REPO)
        local_errors = _validate_one(path, rel, validator)
        if not local_errors:
            data = json.loads(path.read_text(encoding="utf-8"))
            parent = path.parent.name
            if data.get("type") != parent:
                print(f"✗ {rel}")
                print(f"    type={data.get('type')!r} does not match parent dir {parent!r}")
                local_errors += 1
            else:
                print(f"✓ {rel}")
        errors += local_errors
    return errors


def _validate_one(path: Path, rel: Path, validator) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ {rel}: invalid JSON ({e})")
        return 1
    schema_errors = list(validator.iter_errors(data))
    if schema_errors:
        print(f"✗ {rel}")
        for err in schema_errors:
            loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
            print(f"    schema: {err.message} at {loc}")
        return len(schema_errors)
    if data.get("id") != path.stem:
        print(f"✗ {rel}")
        print(f"    id={data.get('id')!r} does not match filename stem {path.stem!r}")
        return 1
    return 0


def _resolve_refs(composition: dict, atom_index: dict, rel: Path) -> int:
    errors = 0
    refs = composition.get("references", {})
    flat: list[dict] = []
    for key, value in refs.items():
        if isinstance(value, list):
            flat.extend(value)
        elif isinstance(value, dict):
            flat.append(value)
    for ref_obj in flat:
        target = ref_obj.get("ref")
        want_version = ref_obj.get("version")
        atom = atom_index.get(target)
        if atom is None:
            print(f"✗ {rel}")
            print(f"    ref unresolved: {target}")
            errors += 1
            continue
        if atom.get("version") != want_version:
            print(f"✗ {rel}")
            print(f"    ref {target} requires version {want_version}; atom is at {atom.get('version')}")
            errors += 1
    return errors


def main() -> int:
    if not SCHEMAS["atom"].exists():
        print(f"missing schema: {SCHEMAS['atom']}", file=sys.stderr)
        return 1

    atom_v = load_validator("atom")
    atom_errors, atom_index = validate_atoms(atom_v)

    composition_errors = 0
    if SCHEMAS["composition"].exists() and COMPOSITIONS_DIR.exists():
        composition_errors = validate_compositions(load_validator("composition"), atom_index)

    rule_errors = 0
    if SCHEMAS["rule"].exists() and RULES_DIR.exists():
        rule_errors = validate_rules(load_validator("rule"))

    total = atom_errors + composition_errors + rule_errors
    if total:
        print(f"\n{total} error(s)")
        return 1
    print(f"\nall valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
