# Extends https://github.com/googleforgames/agones/blob/v1.31.0/install/terraform/modules/gke/variables.tf

# Set of GKE cluster parameters which defines its name, zone
# and primary node pool configuration.
# It is crucial to set valid ProjectID for "project".
variable "cluster" {
  description = "Set of GKE cluster parameters."
  type        = map(any)

  default = {
    "location"                = "us-west1-c"
    "name"                    = "test-cluster"
    "machineType"             = "e2-standard-4"
    "initialNodeCount"        = "4"
    "project"                 = "agones"
    "network"                 = "default"
    "subnetwork"              = ""
    "releaseChannel"          = "RAPID"
    "kubernetesVersion"       = "1.26"
    "windowsInitialNodeCount" = "0"
    "windowsMachineType"      = "e2-standard-4"
    "autoscale"               = false
    "workloadIdentity"        = false
    "minNodeCount"            = "1"
    "maxNodeCount"            = "5"
  }
}

# udpFirewall specifies whether to create a UDP firewall named
# `firewallName` with port range `ports`, source range `sourceRanges`
variable "udpFirewall" {
  default = true
}

# Ports can be overriden using tfvars file
variable "ports" {
  default = "7000-8000"
}

# SourceRanges can be overriden using tfvars file
variable "sourceRanges" {
  default = "0.0.0.0/0"
}

variable "firewallName" {
  description = "name for the cluster firewall. Defaults to 'game-server-firewall-{local.name}' if not set."
  type        = string
  default     = ""
}
