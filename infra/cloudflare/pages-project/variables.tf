variable "cloudflare_account_id" {
  description = "Cloudflare account ID that owns the Pages project."
  type        = string
}

variable "project_name" {
  description = "Cloudflare Pages project name. Must be unique within the account. The default Pages URL becomes https://<project_name>.pages.dev."
  type        = string
  default     = "prompt-atoms"
}

variable "production_branch" {
  description = "Branch name that triggers production deployments. Pushes to this branch on the connected GitHub repo (or wrangler deploys from this branch) become the production URL."
  type        = string
  default     = "main"
}
