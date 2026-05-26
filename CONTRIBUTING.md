# Contributing

## Commit convention

[Conventional Commits](https://www.conventionalcommits.org/). Prefixes:
`feat:`, `fix:`, `refactor:`, `perf:`, `docs:`, `test:`, `build:`, `ci:`,
`chore:`. Subject ≤ 72 chars, imperative mood, no trailing period.

One logical change per commit.

## Labels

Labels follow the [convergent-systems-co label
standard](https://github.com/convergent-systems-co/repo-standards/blob/v1/docs/label-guide.md).
Do not invent labels; PR the standard if you need a new one.

## Pull requests

Use the PR template. Tests required for new behavior; failing test first for
bug fixes.

## Code review

Reviews ground every medium-or-higher finding in a code citation. Self-review
your own diff before requesting review.

---

## Adding a new persona atom

### Atom types

| Type | Directory | Purpose |
|---|---|---|
| `persona` | `atoms/persona/` | Role-conditioning system prompt fragments |
| `constraint` | `atoms/constraint/` | Behavioral guardrails and rules |
| `format-instruction` | `atoms/format-instruction/` | Output format directives |
| `tool-use-template` | `atoms/tool-use-template/` | Tool invocation patterns |
| `refusal-pattern` | `atoms/refusal-pattern/` | Categories of requests to decline |
| `output-schema` | `atoms/output-schema/` | Structured output shape definitions |

### Quick-start

1. **Copy the template**
   ```bash
   cp atoms/persona/persona-template.json atoms/persona/<your-slug>.json
   ```
2. **Edit every field** — see the field reference below. Required fields are
   `schema`, `type`, `id`, `version`, `name`, `content`.
3. **Set `id` to match the filename stem** — `atoms/persona/my-slug.json` must
   have `"id": "my-slug"`. The validator enforces this.
4. **Validate locally**
   ```bash
   pip install jsonschema   # one-time setup
   python3 scripts/validate.py
   ```
   The output must include `✓ atoms/persona/<your-slug>.json` with no errors.
5. **Open a PR** with title `feat(persona): add <name> persona`

### Field reference

| Field | Required | Constraints | Notes |
|---|---|---|---|
| `schema` | yes | must be `"https://prompt-atoms.com/schemas/atom-v1.json"` | Copy exactly; do not change |
| `type` | yes | `"persona"` for persona atoms | Must match the parent directory name |
| `id` | yes | lowercase slug, hyphens only, 3–64 chars (`^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$`) | Must match the filename stem exactly |
| `version` | yes | SemVer `MAJOR.MINOR.PATCH` | Start contributed atoms at `"1.0.0"` |
| `name` | yes | 1–80 chars, human-readable | Displayed in the catalog UI |
| `description` | no | max 500 chars | One sentence: what the persona does and when to use it |
| `tags` | no | array of unique strings, each 1–40 chars | Help with discovery; use existing tags where possible |
| `vendors` | no | array of: `any`, `anthropic`, `claude`, `gpt`, `openai`, `gemini`, `llama`, `mistral`, `ollama` | Use `["any"]` when the atom is vendor-agnostic |
| `content` | yes | string (may be empty for stubs) | The literal prompt fragment injected at runtime |
| `applicable_turns` | no | array of: `system`, `user`, `assistant`, `tool` | Defaults to `["system"]` for personas |
| `see_also` | no | array of `prompt-atoms://atoms/<type>/<id>` URIs | Atoms commonly composed with this one |

### ID and filename naming rules

- Lowercase letters, digits, and hyphens only.
- Must start and end with a letter or digit (no leading/trailing hyphens).
- Length 3–64 characters.
- Must be unique within `atoms/persona/`.
- **Filename must equal `id` + `.json`** — the validator rejects mismatches.

### Vendor values

`vendors` declares which LLM families this atom is optimized for. Use `"any"`
when the behavior is vendor-agnostic. When an atom requires vendor-specific
features (e.g., Anthropic tool-use format), list only the compatible vendors.

### Lifecycle and `version`

All contributed atoms start at `"1.0.0"` (stable, production-ready).
If the atom is experimental, start at `"0.1.0"` and note it as `draft` in the
`description`.

### Content guidelines

- `content` is the literal prompt fragment the runtime injects into the
  appropriate turn — write it as you want it to appear in the system message.
- Keep it under 500 words; combine multiple atoms at composition time.
- Avoid hardcoded vendor API details inside `content`; use the `vendors` field
  to declare compatibility instead.
- Prefer positive framing ("do X") over prohibitions ("never do Y") where both
  express the same constraint.

### Review criteria

PRs are reviewed for:

- **Correctness** — does the prompt actually produce the declared behavior?
- **Composability** — does it work alongside other atoms without conflicts?
- **Format** — schema valid, ID matches filename, naming conventions followed.

### Example

See [`atoms/persona/code-reviewer-strict.json`](atoms/persona/code-reviewer-strict.json)
for a complete, validated example.
