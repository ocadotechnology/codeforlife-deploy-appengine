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

variable "log_level" {
  default = "info"
}

variable "feature_gates" {
  default = ""
}

variable "region" {
  default = "europe-west1"
}


locals {
  cluster_name = "aimmo-${terraform.workspace}"

  agones_version = "1.10.0"
}
