# A Pages project shell. No `source` block — this is a "direct upload"
# project, meaning deployments come from `wrangler pages deploy` runs in
# CI (.github/workflows/deploy.yml), not from a Pages-managed Git
# integration. The CI workflow's CLOUDFLARE_API_TOKEN must have
# "Pages — Edit" scope on this account.
#
# Custom domain attachment (prompt-atoms.com) is intentionally not
# managed here — DNS is in a separate concern and Pages domain
# attachment is currently a one-time dashboard action. If/when a
# cloudflare_pages_domain resource becomes a clean fit, add it as its
# own module under infra/cloudflare/.
resource "cloudflare_pages_project" "this" {
  account_id        = var.cloudflare_account_id
  name              = var.project_name
  production_branch = var.production_branch
}
