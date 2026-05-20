# prompt-atoms — Goals

> Prompt engineering as a canonical, machine-readable, versioned library — replacing closed vendor libraries and scattered cookbooks with typed personas, constraints, formats, tool-use templates, refusal patterns, and output schemas.

*This document is derived from `aish/ARCHITECTURE.md` (now `xdao/xdao/ARCHITECTURE.md` §The *-Atoms Catalogs). Sections marked **Generated** are pattern-based and are intended as a starting point for revision, not as decided plan.*

---

## What this catalog makes civilization-grade

The prompt engineering space has no canonical, machine-readable, versioned library. Vendor cookbooks (OpenAI, Anthropic, Google) are closed and product-specific. Open repositories are unstructured collections of strings. No one can version a persona, compose constraints, or verify a prompt is well-formed before runtime.

By cataloging the primitives, `prompt-atoms` turns this domain from opaque-and-ephemeral to typed, versioned, composable, machine-readable, and open — the civilization-grade properties the ecosystem requires.

## What it catalogs

### Atom types

- **`persona`** — Voice, expertise, register, and refusal posture for an agent.
- **`constraint`** — Behavioral constraint (e.g., 'output only valid YAML', 'never invent citations').
- **`format-instruction`** — Output format specification (markdown, JSON, plain text, structured table).
- **`tool-use-template`** — Standard scaffolding for tool-using agents.
- **`refusal-pattern`** — How and when to refuse — vendor-policy-shaped patterns.
- **`output-schema`** — Typed output declaration that downstream code can parse.

### Compositions: `prompts`

A prompt composition assembles persona + constraints + format + tools + output schema into a complete system message or agent definition. Versioned, reproducible, swappable.

### Rule types

- **`model-compatibility`** — Which models support a given prompt (token limits, tool-use support, format adherence).
- **`token-length-constraint`** — Token budget bounds.
- **`format-compatibility`** — Whether the output schema is satisfiable under the format-instruction (e.g., JSON schema requires `format: json`).

## Runtime consumers

- **olympus** — Every agentic phase uses prompts. Hermes routing, Mnemosyne queries, Aegis emission, Pantheon Module behavior — all parameterized by prompt-atoms.
- **aish** — Intent classification and cache compilation primitives. The intent cache uses persona + format + output-schema to compile natural language into deterministic invocations.

## Status & priority

**Current status:** `proposed`

**Priority tier:** Tier 2 — Highest priority to build next (runtime pull immediate)

**Trigger / activation condition:** Olympus is already pulling. aish v0.1 intent classification will pull at first cache miss.

## Roadmap *(Generated — milestone shapes mirror aish's roadmap pattern; revise as actual work begins)*

### v0.1 — Bootstrap & spec acceptance

**Goal:** Spec accepted. 50 seed atoms across all six atom types. Olympus consumes for one Pantheon Module.

**Success criterion:** Olympus Pantheon Module driven entirely by prompt-atoms composition; behavior reproducible across sessions.

**Kill criterion:** Composition rules can't capture the variance between vendors (Claude vs GPT vs Llama) without explosion — pivot to per-vendor sub-catalogs.

**Work:**

- [ ] XAIP: prompt composition schema (system + user + tool turns)
- [ ] Define schemas for all 6 atom types
- [ ] Seed 10 personas, 15 constraints, 10 formats, 5 tool templates, 5 refusal patterns, 5 output schemas
- [ ] Integrate with Olympus Hermes routing
- [ ] Publish first signed export

### v0.2 — Adoption & expansion

**Goal:** Community contribution flow. aish consumes for intent classification.

**Work:**

- [ ] Contribution template for new personas
- [ ] aish v0.1 intent classification uses prompt-atoms primitives
- [ ] Add 50 community-contributed atoms

### v1.0 — Operational

**Goal:** Prompt-atoms is the canonical reference. New AI frameworks adopt it as their persona/constraint vocabulary.

## Concrete atom example *(Generated — illustrative, not seed content)*

```yaml
atoms/persona/peer-programmer.yml
---
id: peer-programmer
type: persona
version: 0.2.0
name: Peer Programmer
voice: collaborative, direct, calibrated
expertise: [software-engineering, debugging, refactoring]
register: technical
refusal_posture: explain-and-redirect
opening_disposition: ask-before-acting
model_compatibility: [claude-opus, gpt-4o, llama-3.1-70b]
```

## Adoption strategy *(Generated)*

Olympus pulls immediately. Wider adoption follows reference implementations — once one team's Pantheon Modules are reproducible via prompt-atoms, others adopt.

## Civilization-grade property checklist

Every catalog must satisfy these before v1.0. Failing any blocks a release.

| Property | Mechanism in this catalog |
|---|---|
| Typed | JSON Schema in `schemas/` validates every atom, composition, rule |
| Versioned | Every atom has a semver `version` field; compositions reference atoms by version-pinned ID |
| Machine-readable | `exports/catalog.json` published on every release |
| Composable | Compositions reference atoms by ID; CI verifies references resolve and no circular dependencies |
| Open | Apache-2.0 licensed; LICENSE file present |
| Durable | No external dependencies for primary content (no remote image URLs, no vendor APIs in the hot path) |

## Related

- **Spec:** [atoms-spec](https://github.com/convergent-systems-co/atoms-spec) — the canonical structure every catalog conforms to
- **Tools:** [atoms-tools](https://github.com/convergent-systems-co/atoms-tools) — CLI for validate / export / bootstrap / resolve
- **Federation:** [xdao](https://github.com/convergent-systems-co/xdao) — ecosystem directory and discovery
- **Umbrella:** [atoms](https://github.com/convergent-systems-co/atoms) — every catalog as a git submodule
- **Manifest:** [`ATOMS.yml`](./ATOMS.yml) — this catalog's machine-readable manifest
- **Standard:** [`README.md`](./README.md) — catalog overview and contribution flow
