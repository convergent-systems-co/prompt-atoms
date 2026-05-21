terraform {
  required_version = ">= 1.6.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }

  # State lives in Cloudflare R2 (S3-compatible API).
  # Credentials are supplied via env vars AWS_ACCESS_KEY_ID and
  # AWS_SECRET_ACCESS_KEY — see core-infra/scripts/bootstrap-tf-state.sh.
  # Key per ~/.ai/memory/reference_terraform_state_keys.md:
  #   bucket/state-bucket/<org>/<project>/<module>.tfstate
  # prompt-atoms anticipates multiple infra modules over time, so the
  # module segment is included from the start.
  backend "s3" {
    bucket = "cs-tfstate"
    key    = "state-bucket/convergent-systems-co/prompt-atoms/pages-project.tfstate"
    region = "auto"
    endpoints = {
      s3 = "https://e1fe0f0ce8ff18da4edc118372c30022.r2.cloudflarestorage.com"
    }
    skip_credentials_validation = true
    skip_region_validation      = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_path_style              = false
    use_lockfile                = true
  }
}
