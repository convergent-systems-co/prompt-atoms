# The Cloudflare provider reads its API token from the
# CLOUDFLARE_API_TOKEN environment variable. No token is set in code,
# in tfvars, or in any committed file — per ~/.ai/Common.md §4.
#
# Required token scopes (least-privilege):
#   - Account: Cloudflare Pages (Edit)   on the convergent-systems-co account
provider "cloudflare" {}
