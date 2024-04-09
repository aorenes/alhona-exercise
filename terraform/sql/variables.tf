variable "gcp_pg_name_primary" {
  type    = string
  default = "alhona"
}

variable "gcp_pg_database_version" {
  type    = string
  default = "POSTGRES_15"
}

variable "gcp_pg_region_primary" {
  type    = string
  default = "europe-west1"
}

variable "project" {
  description = "The project ID where all resources will be launched."
  type        = string
  default     = "alhona-exercise"
}

variable "gcp_pg_tier" {
  type    = string
  default = "db-f1-micro"
}

variable "user" {
  description = "Service account to work with the database"
  type        = string
  default     = "alhona-db@alhona-exercise.iam.gserviceaccount.com"
}