terraform {
  required_version = ">= 1.7.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}

# CLOUDFLARE_API_TOKEN from env, never in code. See ~/.ai/Common.md §4.
# Required token scopes:
#   - Account → Cloudflare Pages → Edit
#   - Zone → DNS → Edit (for the prompt-atoms.com zone)
provider "cloudflare" {}

# NOTE: the prompt-atoms Cloudflare Pages project was created out-of-band
# (before terraform was wired). Apex domain attachment + DNS were added
# via direct API call on 2026-05-23. To bring the existing project under
# terraform management, an `import { to = module.pages_project... }` block
# can be added; the resource identifiers exist in Cloudflare today.
module "pages_project" {
  source = "git::https://github.com/convergent-systems-co/core-infra.git//terraform/cloudflare/pages-project?ref=v0.1.0"

  cloudflare_account_id = var.cloudflare_account_id
  project_name          = "prompt-atoms"
  production_branch     = "main"
  custom_domain         = "prompt-atoms.com"
  zone_id               = var.zone_id
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID that owns the Pages project."
  type        = string
}

variable "zone_id" {
  description = "Cloudflare zone ID for prompt-atoms.com."
  type        = string
}

output "project_name" {
  value = module.pages_project.project_name
}

output "subdomain" {
  value       = module.pages_project.subdomain
  description = "Default *.pages.dev hostname for the project."
}

output "custom_domain" {
  value       = module.pages_project.custom_domain
  description = "Custom hostname attached to the Pages project."
}
