output "host" {
  value = module.gke_cluster.host
}
output "token" {
  value = module.gke_cluster.token
}
output "cluster_ca_certificate" {
  value = module.gke_cluster.cluster_ca_certificate
}
