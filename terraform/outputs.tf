output "eks_cluster_endpoint" {
    value = module.eks.cluster_endpoint
}

output "psql_dev_connection_name" {
    value = google_sql_database_instance.dev.connection_name
}

output "psql_dev_password" {
    value = random_id.db_pass.hex
}


output "k8_dev_cluster_id" {
    value = google_container_cluster.dev.name
}

output "gke_endpoint" {
    value = google_container_cluster.dev.endpoint
}

output "IMAGE_NAME" {
    value = random_pet.image.id
}
