output "host" {
  value = module.gke_cluster.host
}

output "cluster_ca_certificate" {
  value = module.gke_cluster.cluster_ca_certificate
}

output "b64_cluster_ca_certificate" {
  value = base64encode(module.gke_cluster.cluster_ca_certificate)
}
