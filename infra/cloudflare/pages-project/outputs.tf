output "project_name" {
  description = "Cloudflare Pages project name. Used by .github/workflows/deploy.yml as the --project-name argument to wrangler."
  value       = cloudflare_pages_project.this.name
}

output "subdomain" {
  description = "Default Pages subdomain, e.g. prompt-atoms.pages.dev. Custom domain (prompt-atoms.com) is attached out-of-band."
  value       = cloudflare_pages_project.this.subdomain
}

output "created_on" {
  description = "Project creation timestamp from the Cloudflare API."
  value       = cloudflare_pages_project.this.created_on
}
