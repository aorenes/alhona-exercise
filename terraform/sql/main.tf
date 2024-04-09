resource "google_project_service" "services" {
  project            = var.project
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "sql-component" {
  project            = var.project
  service            = "sql-component.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "servicenetworking" {
  project            = var.project
  service            = "servicenetworking.googleapis.com"
  disable_on_destroy = false
}

resource "time_sleep" "wait_30_seconds" {
  depends_on = [google_project_service.services, google_project_service.sql-component, google_project_service.servicenetworking]

  create_duration = "30s"
}

resource "google_sql_database_instance" "primary" {
  name                = var.gcp_pg_name_primary
  database_version    = var.gcp_pg_database_version
  region              = var.gcp_pg_region_primary
  deletion_protection = false

  settings {
    tier      = var.gcp_pg_tier
    disk_size = 10
    disk_type = "PD_SSD"
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "all_networks"
        value = "0.0.0.0/0"
      }
    }
  }

  depends_on = [google_project_service.services, time_sleep.wait_30_seconds]

}

resource "google_sql_database" "database" {
  name = "mqtt"
  instance = var.gcp_pg_name_primary
  charset = "utf8"
}

output "instance_primary_ip_address" {
  value = google_sql_database_instance.primary.ip_address
}