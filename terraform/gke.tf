resource "google_container_cluster" "dev" {
  name               = "humanitec-k8-dev"
  location           = "europe-west2-a"
  initial_node_count = 1
}
