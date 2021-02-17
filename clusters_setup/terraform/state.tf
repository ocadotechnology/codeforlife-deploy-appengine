// Run:
//  terraform workspace select {dev,staging,default}
//  terraform apply

terraform {
  backend "gcs" {
    bucket = "codeforlife-terraform-states"
    prefix = "terraform/state/aimmo/"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.51.0"
    }
  }
}

module "gke_cluster" {
  // ***************************************************************************************************
  // Update ?ref= to the agones release you are installing. For example, ?ref=release-1.8.0 corresponds
  // to Agones version 1.8.0
  // ***************************************************************************************************
  source = "git::https://github.com/googleforgames/agones.git//install/terraform/modules/gke/?ref=release-1.10.0"

  cluster = {
    "name"             = local.cluster_name
    "zone"             = var.zone
    "machineType"      = var.machine_type
    "initialNodeCount" = var.node_count
    "project"          = var.project
    "network"          = var.network
    "subnetwork"       = var.subnetwork
  }
}

module "helm_agones" {
  // ***************************************************************************************************
  // Update ?ref= to the agones release you are installing. For example, ?ref=release-1.8.0 corresponds
  // to Agones version 1.8.0
  // ***************************************************************************************************
  source = "git::https://github.com/googleforgames/agones.git//install/terraform/modules/helm3/?ref=release-1.10.0"

  agones_version         = local.agones_version
  values_file            = ""
  feature_gates          = var.feature_gates
  host                   = module.gke_cluster.host
  token                  = module.gke_cluster.token
  cluster_ca_certificate = module.gke_cluster.cluster_ca_certificate
  log_level              = var.log_level
}
