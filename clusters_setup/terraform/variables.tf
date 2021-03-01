# Agones helm variables, inspired from https://github.com/googleforgames/agones/blob/main/install/terraform/modules/helm3/helm.tf

variable "chart" {
  default = "agones"
}

variable "force_update" {
  default = "true"
}

variable "udp_expose" {
  default = "true"
}

variable "log_level" {
  default = "info"
}

variable "feature_gates" {
  default = ""
}

variable "crd_cleanup" {
  default = "true"
}

variable "image_registry" {
  default = "gcr.io/agones-images"
}

variable "pull_policy" {
  default = "IfNotPresent"
}

variable "always_pull_sidecar" {
  default = "false"
}

variable "image_pull_secret" {
  default = ""
}

variable "ping_service_type" {
  default = "LoadBalancer"
}

variable "values_file" {
  default = ""
}

variable "gameserver_minPort" {
  default = "7000"
}

variable "gameserver_maxPort" {
  default = "8000"
}

variable "gameserver_namespaces" {
  default = ["default"]
  type    = list(string)
}


# Main variables

variable "project" {
  default = "decent-digit-629"
}

variable "machine_type" {
  default = "n2-standard-2"
}

// Note: This is the number of gameserver nodes. The Agones module will automatically create an additional
// two node pools with 1 node each for "agones-system" and "agones-metrics".
variable "node_count" {
  default = "1"
}
variable "zone" {
  default     = "europe-west1-b"
  description = "The GCP zone to create the cluster in"
}

variable "network" {
  default     = "cfl-main-network"
  description = "The name of the VPC network to attach the cluster and firewall rule to"
}

variable "subnetwork" {
  default     = "cfl-main-network"
  description = "The subnetwork to host the cluster in. Required field if network value isn't 'default'."
}

variable "kubernetesVersion" {
  default = "1.17.17-gke.1500"
}

variable "region" {
  default = "europe-west1"
}


locals {
  cluster_name = "aimmo-${terraform.workspace}"

  agones_version = "1.12.0"
}
