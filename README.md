      # prompt-atoms

      > Prompt engineering as a canonical, machine-readable, versioned library — replacing closed vendor libraries and scattered cookbooks with typed personas, constraints, formats, tool-use templates, refusal patterns, and output schemas.

      `prompt-atoms` is a `*-Atoms` catalog in the [Convergent Systems](https://xdao.co) ecosystem. It defines what exists in its domain — typed, versioned, machine-readable, composable, and open — so runtimes (and humans) can stand on shared infrastructure instead of reinventing it.

      ## Structure

      ```
      prompt-atoms/
      ├── ATOMS.yml              # Catalog manifest
      ├── atoms/                 # Reusable building blocks
      ├── prompts/        # Compositions assembled from atoms
      ├── rules/                 # Typed constraint vocabulary
      ├── schemas/               # Catalog-specific JSON Schemas
      ├── exports/               # CI-generated machine-readable exports
      └── docs/                  # Human-readable documentation
      ```

      ### Atom types

        - `persona`
- `constraint`
- `format-instruction`
- `tool-use-template`
- `refusal-pattern`
- `output-schema`

      ### Rule types

        - `model-compatibility`
- `token-length-constraint`
- `format-compatibility`

      ### Runtime consumers

      `aish`, `olympus`

      ## How to consume

      Machine-readable exports are published in [`exports/`](./exports/) on every release:

      - `exports/manifest.json` — lightweight discovery (name, version, counts)
      - `exports/catalog.json` — full catalog dump (every atom, composition, rule)

      Exports are deterministic, signed, and versioned. See [`ATOMS.yml`](./ATOMS.yml) for the manifest and the conformance spec.

      ## How to contribute

      1. Read [`ATOMS.yml`](./ATOMS.yml) to understand the catalog's atom types, compositions, and rules.
      2. Add a new atom under `atoms/<type>/` or a composition under `prompts/<name>/`.
      3. Open a PR. CI validates the schema, references, and exports.
      4. Larger structural changes go through the [XAIP process](https://github.com/convergent-systems-co/xaips).

      ## Ecosystem

      - **Federation:** [xdao.co](https://xdao.co) · [github.com/convergent-systems-co/xdao](https://github.com/convergent-systems-co/xdao)
      - **Spec:** [github.com/convergent-systems-co/atoms-spec](https://github.com/convergent-systems-co/atoms-spec)
      - **Tools:** [github.com/convergent-systems-co/atoms-tools](https://github.com/convergent-systems-co/atoms-tools)
      - **Umbrella:** [github.com/convergent-systems-co/atoms](https://github.com/convergent-systems-co/atoms) — all catalogs as submodules
      - **Other catalogs:** brand-atoms, service-atoms, prompt-atoms, policy-atoms, identity-atoms, compliance-atoms, workflow-atoms, agent-atoms, knowledge-atoms, event-atoms, plugin-atoms

      ## License

      Apache-2.0 — see [`LICENSE`](./LICENSE).
