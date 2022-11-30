resource "google_container_cluster" "dev" {
  name               = "humanitec-k8-dev"
  location           = "europe-west2-a"
  initial_node_count = 1
}

output "k8_dev_cluster_id" {
    value = google_container_cluster.dev.name
}

output "gke_endpoint" {
    value = google_container_cluster.dev.endpoint
}