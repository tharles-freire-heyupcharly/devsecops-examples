# Mock AWS Provider Configuration for Examples
# This allows terraform plan to work without real AWS credentials

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "sa-east-1" # São Paulo - Brasil

  # Mock credentials for examples/testing
  # In production, use AWS credentials from environment or IAM roles
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}
