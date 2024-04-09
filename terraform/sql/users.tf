resource "google_sql_user" "users" {
  name     = "alhona"
  instance = var.gcp_pg_name_primary
  password = "alhona"
}