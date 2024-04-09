terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file("terraform.json")
  project     = var.project
  region      = "europe-west1"
  zone        = "europe-west1-b"
}