# Extends https://github.com/googleforgames/agones/blob/v1.26.0/install/terraform/modules/gke/variables.tf

# Ports can be overriden using tfvars file
variable "ports" {
  default = "7000-8000"
}

# SourceRanges can be overriden using tfvars file
variable "sourceRanges" {
  default = "0.0.0.0/0"
}

# Set of GKE cluster parameters which defines its name, zone
# and primary node pool configuration.
# It is crucial to set valid ProjectID for "project".
variable "cluster" {
  description = "Set of GKE cluster parameters."
  type        = map

  default = {
    "zone"                    = "us-west1-c"
    "name"                    = "test-cluster"
    "machineType"             = "e2-standard-4"
    "initialNodeCount"        = "4"
    "project"                 = "agones"
    "network"                 = "default"
    "subnetwork"              = ""
    "kubernetesVersion"       = "1.23"
    "windowsInitialNodeCount" = "0"
    "windowsMachineType"      = "e2-standard-4"
  }
}

variable "firewallName" {
  description = "name for the cluster firewall. Defaults to 'game-server-firewall-{local.name}' if not set."
  type        = string
  default     = ""
}
