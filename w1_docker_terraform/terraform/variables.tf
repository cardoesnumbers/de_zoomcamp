variable "credentials" {
  description = "My Credentials"
  default     = "w1_docker_terraform/pipeline/gcp_key.json"
  sensitive   = true #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "terraform-demo-485312"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "EU"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "zoomcamp"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "dezc-485312" #TODO make sure it's globally unique!
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}