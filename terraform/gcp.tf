resource "random_pet" "image" {}


resource "random_id" "db_pass" {
  byte_length = 16
}

resource "google_sql_database_instance" "dev" {
  name             = "humanitec-psql-dev"
  database_version = "POSTGRES_14"
  region           = "europe-west2"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_user" "users" {
  name     = "humanitec_user"
  instance = google_sql_database_instance.dev.name
  password = random_id.db_pass.hex
}

resource "google_container_cluster" "dev" {
  name               = "humanitec-k8-dev"
  location           = "europe-west2-a"
  initial_node_count = 1
}


