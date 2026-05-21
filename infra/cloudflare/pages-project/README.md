# infra/cloudflare/pages-project

Terraform module that creates the Cloudflare Pages project `prompt-atoms` is deployed to.

## Audience

A contributor bootstrapping prompt-atoms in a fresh Cloudflare account, or recovering the project after deletion.

## What this creates

- A single `cloudflare_pages_project` named `prompt-atoms` with production branch `main`.

That's it. Deployments themselves come from `.github/workflows/deploy.yml` via `wrangler pages deploy web/dist`. Custom domain attachment (`prompt-atoms.com`) is a separate, out-of-band step in the Cloudflare dashboard.

## Prerequisites

- OpenTofu or Terraform `>= 1.6.0` (this repo doesn't pin a specific version).
- AWS-compatible credentials for the Cloudflare R2 state bucket. See `core-infra/scripts/bootstrap-tf-state.sh` (or the equivalent setup in `~/.ai/memory/reference_convergent_systems_env_fifo.md`).
- A Cloudflare API token with `Pages — Edit` scope, exported as `CLOUDFLARE_API_TOKEN`.
- The convergent-systems-co Cloudflare account ID.

## Apply

```bash
cd infra/cloudflare/pages-project
cp terraform.tfvars.example terraform.tfvars
$EDITOR terraform.tfvars   # fill in cloudflare_account_id

tofu init     # downloads provider, configures R2 backend
tofu plan     # expect: one resource to add (cloudflare_pages_project.this)
tofu apply    # confirm 'yes' when prompted
```

After apply, the project is live at `https://prompt-atoms.pages.dev`. The next push to `main` (or PR opened against `main`) will trigger the CI workflow at `.github/workflows/deploy.yml`, which now finds the project and deploys to it.

## State

State key (per [`reference_terraform_state_keys`](https://github.com/convergent-systems-co/atoms/blob/main/.ai-memory-not-checked-in)):

```
s3://cs-tfstate/state-bucket/convergent-systems-co/prompt-atoms/pages-project.tfstate
```

The `pages-project` module segment is included from the start so additional `prompt-atoms` infra modules (DNS, R2 buckets, KV namespaces) can be added later without state-key migration.

## Destroy

```bash
tofu destroy
```

Removes the Pages project. Existing deployments and their preview URLs are deleted. The custom domain attachment must be removed separately in the dashboard.
