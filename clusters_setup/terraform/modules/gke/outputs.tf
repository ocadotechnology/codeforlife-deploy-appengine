# Extends https://github.com/googleforgames/agones/blob/v1.31.0/install/terraform/modules/gke/outputs.tf

output "cluster_ca_certificate" {
  value = base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)
}

output "host" {
  value = "https://${google_container_cluster.primary.endpoint}"
}

output "token" {
  value = data.google_client_config.default.access_token
}
