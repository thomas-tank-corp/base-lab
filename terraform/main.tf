terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.33.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "4.31.0"
    }
    tls = {
      source = "hashicorp/tls"
      version = "4.0.3"
    }
  }
}

provider "aws" {
  region = local.region
}

provider "google" {}

provider "tls" {}


