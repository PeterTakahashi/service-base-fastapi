output "gke_cluster_name" {
  value = google_container_cluster.primary.name
}

output "gke_cluster_location" {
  value = google_container_cluster.primary.location
}

output "cloud_sql_instance_connection_name" {
  value = google_sql_database_instance.default.connection_name
}
