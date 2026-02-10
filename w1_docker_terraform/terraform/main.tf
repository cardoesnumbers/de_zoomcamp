terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true

   lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "zoomcamp" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

output "gcs_bucket_name" {
  value = google_storage_bucket.demo-bucket.name
}

output "bq_dataset_id" {
  value = google_bigquery_dataset.zoomcamp.dataset_id
}
#name          = "terraform-demo-485312-terra-bucket"
