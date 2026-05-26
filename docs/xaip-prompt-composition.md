# XAIP: Prompt Composition Schema

**Audience:** Prompt engineers and agent authors composing prompt sequences from prompt-atoms fragments.

## What this defines

A prompt composition in prompt-atoms assembles typed prompt fragments into a
complete, deterministic prompt sequence with defined turn structure.

The XAIP (Cross-Atoms Integration Proposal) model replaces the flat `references`
object with an ordered `turns` array, making the sequence explicit and enabling
multi-turn compositions that include user, tool, and assistant-seed turns — not
just a system message.

## Turn types

| Role | Purpose |
|---|---|
| `system` | Initial system-level instructions (persona, constraints, output format) |
| `user` | The user-facing instruction or task |
| `tool` | Tool definitions injected into the model context |
| `assistant-seed` | Optional assistant response prefix for few-shot seeding |

## Composition structure

A composition references atoms by ID for each turn. Each turn supplies its
content via exactly one of `atom_ref` (a reference to an existing atom) or
`template` (an inline string with `{variable}` placeholders).

```json
{
  "schema": "https://prompt-atoms.com/schemas/composition-v1.json",
  "type": "prompt",
  "id": "code-reviewer-strict",
  "version": "2.0.0",
  "name": "Strict Code Reviewer",
  "description": "Adversarial code-review prompt with turn-sequence structure.",
  "tags": ["code-review", "engineering"],
  "vendors": ["claude", "gpt"],
  "turns": [
    {
      "role": "system",
      "atom_ref": { "ref": "prompt-atoms://atoms/persona/code-reviewer-strict", "version": "1.0.0" }
    },
    {
      "role": "system",
      "atom_ref": { "ref": "prompt-atoms://atoms/constraint/cite-file-line", "version": "1.0.0" }
    },
    {
      "role": "system",
      "atom_ref": { "ref": "prompt-atoms://atoms/constraint/findings-need-evidence", "version": "1.0.0" }
    },
    {
      "role": "tool",
      "atom_ref": { "ref": "prompt-atoms://atoms/tool-use-template/parallel-when-independent", "version": "1.0.0" }
    },
    {
      "role": "user",
      "template": "Review the following diff and return findings:\n\n{diff}"
    }
  ],
  "output_schema_ref": { "ref": "prompt-atoms://atoms/output-schema/findings-list", "version": "1.0.0" }
}
```

## Conformance rules

1. Every composition MUST have at least one `system` turn.
2. `user` turns SHOULD appear after all `system` turns.
3. `tool` turns MUST reference a `tool-use-template` atom via `atom_ref`; inline templates are not permitted for tool definitions.
4. `assistant-seed` turns MUST be the final turn when present; they set the response prefix for few-shot seeding.
5. `output_schema_ref` is recommended for all compositions that produce structured output.
6. Each turn MUST supply exactly one of `atom_ref` or `template` — not both, not neither.

## Migration from the flat `references` model

The legacy `references` object remains valid for existing compositions. New
compositions SHOULD use `turns`. The schema accepts both forms; they MUST NOT
be mixed in a single composition document.

| `references` field | XAIP `turns` equivalent |
|---|---|
| `persona` | `{"role": "system", "atom_ref": ...}` |
| `constraints[]` | One `{"role": "system", "atom_ref": ...}` per constraint, in order |
| `format_instruction` | `{"role": "system", "atom_ref": ...}` after constraints |
| `tool_use_template` | `{"role": "tool", "atom_ref": ...}` |
| `refusal_patterns[]` | `{"role": "system", "atom_ref": ...}` per pattern |
| `output_schema` | Top-level `output_schema_ref` field |

## Relationship to other catalogs

- **persona-atoms**: Persona atoms are the canonical source for `system`-turn identity fragments.
- **policy-atoms**: Policy atoms gate which compositions are permitted in a given deployment context.
- **agent-atoms**: Agent compositions embed prompt-atoms compositions as their system prompt layer, wrapping them in an agent execution envelope.
- **schema-atoms**: Grammar atoms in schema-atoms define the allowed structure of `output_schema_ref` targets.

## See also

- [`schemas/composition-v1.json`](../schemas/composition-v1.json) — JSON Schema for this document format
- [`prompts/`](../prompts/) — Example compositions
- [`docs/adr/`](adr/) — Architecture decisions for the prompt-atoms catalog
