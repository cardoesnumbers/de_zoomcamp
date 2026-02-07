terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = "terraform-demo-485312"
  region      = "europe-west1"


}

resource "google_storage_bucket" "demo-bucket" {
  name          = "dezc-485312"
  location      = "EU"
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

output "gcs_bucket_name" {
  value = google_storage_bucket.demo-bucket.name
}
#name          = "terraform-demo-485312-terra-bucket"