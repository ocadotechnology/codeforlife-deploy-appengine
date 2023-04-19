# Extends https://github.com/googleforgames/agones/blob/v1.26.0/install/terraform/modules/gke/cluster.tf

terraform {
  required_version = ">= 1.0.0"
}

data "google_client_config" "default" {}

# A list of all parameters used in interpolation var.cluster
# Set values to default if not key was not set in original map
locals {
  project                 = lookup(var.cluster, "project", "agones")
  location                = lookup(var.cluster, "location", "us-west1-c")
  zone                    = lookup(var.cluster, "zone", "")
  name                    = lookup(var.cluster, "name", "test-cluster")
  machineType             = lookup(var.cluster, "machineType", "e2-standard-4")
  initialNodeCount        = lookup(var.cluster, "initialNodeCount", "4")
  enableImageStreaming    = lookup(var.cluster, "enableImageStreaming", true)
  network                 = lookup(var.cluster, "network", "default")
  subnetwork              = lookup(var.cluster, "subnetwork", "")
  releaseChannel          = lookup(var.cluster, "releaseChannel", "RAPID")
  kubernetesVersion       = lookup(var.cluster, "kubernetesVersion", "1.26")
  windowsInitialNodeCount = lookup(var.cluster, "windowsInitialNodeCount", "0")
  windowsMachineType      = lookup(var.cluster, "windowsMachineType", "e2-standard-4")
  autoscale               = lookup(var.cluster, "autoscale", false)
  workloadIdentity        = lookup(var.cluster, "workloadIdentity", false)
  minNodeCount            = lookup(var.cluster, "minNodeCount", "1")
  maxNodeCount            = lookup(var.cluster, "maxNodeCount", "5")
}

data "google_container_engine_versions" "version" {
  project        = local.project
  provider       = google-beta
  location       = local.location
  version_prefix = format("%s.",local.kubernetesVersion)
}

# echo command used for debugging purpose
# Run `terraform taint null_resource.test-setting-variables` before second execution
resource "null_resource" "test-setting-variables" {
  provisioner "local-exec" {
    command = <<EOT
    ${format("echo Current variables set as following - name: %s, project: %s, machineType: %s, initialNodeCount: %s, network: %s, zone: %s, location: %s, windowsInitialNodeCount: %s, windowsMachineType: %s, releaseChannel: %s, kubernetesVersion: %s",
    local.name,
    local.project,
    local.machineType,
    local.initialNodeCount,
    local.network,
    local.zone,
    local.location,
    local.windowsInitialNodeCount,
    local.windowsMachineType,
    local.releaseChannel,
    local.kubernetesVersion,
)}
    EOT
  }
}

resource "google_container_cluster" "primary" {
  name       = local.name
  location   = local.zone != "" ? local.zone : local.location
  project    = local.project
  network    = local.network
  subnetwork = local.subnetwork
  enable_shielded_nodes = true
  enable_intranode_visibility = true

#  private_cluster_config {
#    enable_private_nodes = true
#    enable_private_endpoint = true
#  }

  release_channel {
    channel = local.releaseChannel
  }

  min_master_version = local.kubernetesVersion

  network_policy {
    provider = "CALICO"
    enabled = true
  }

  workload_identity_config {
    workload_pool = "decent-digit-629.svc.id.goog"
  }

  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  node_pool {
    name       = "default"
    version    = local.kubernetesVersion

    autoscaling {
      max_node_count = 2
      min_node_count = 0
    }

    management {
      auto_repair = true
      auto_upgrade = local.releaseChannel == "UNSPECIFIED" ? false : true
    }

    node_config {
      machine_type = local.machineType
      image_type = "COS_CONTAINERD"

      oauth_scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/trace.append",
      ]

      tags = ["game-server"]
    }
  }
  node_pool {
    name       = "agones-system"
    node_count = 1
    version    = local.kubernetesVersion

    management {
      auto_repair = true
      auto_upgrade = local.releaseChannel == "UNSPECIFIED" ? false : true
    }

    node_config {
      machine_type = "n1-standard-4"
      image_type = "COS_CONTAINERD"

      oauth_scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/trace.append",
      ]

      labels = {
        "agones.dev/agones-system" = "true"
      }

      taint {
        key    = "agones.dev/agones-system"
        value  = "true"
        effect = "NO_EXECUTE"
      }
    }
  }
  node_pool {
    name       = "agones-metrics"
    node_count = 1
    version    = local.kubernetesVersion

    management {
      auto_repair = true
      auto_upgrade = local.releaseChannel == "UNSPECIFIED" ? false : true
    }

    node_config {
      machine_type = "n1-standard-4"
      image_type = "COS_CONTAINERD"

      oauth_scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/trace.append",
      ]

      labels = {
        "agones.dev/agones-metrics" = "true"
      }

      taint {
        key    = "agones.dev/agones-metrics"
        value  = "true"
        effect = "NO_EXECUTE"
      }
    }
  }
  dynamic "ip_allocation_policy" {
    for_each = tonumber(local.windowsInitialNodeCount) > 0 ? [1] : []
    content {
      # Enable Alias IPs to allow Windows Server networking.
      cluster_ipv4_cidr_block  = "/14"
      services_ipv4_cidr_block = "/20"
    }
  }
  dynamic "node_pool" {
    for_each = tonumber(local.windowsInitialNodeCount) > 0 ? [1] : []
    content {
      name       = "windows"
      node_count = local.windowsInitialNodeCount
      version    = local.releaseChannel == "UNSPECIFIED" ? data.google_container_engine_versions.version.latest_node_version : data.google_container_engine_versions.version.release_channel_latest_version[local.releaseChannel]

      management {
        auto_upgrade = local.releaseChannel == "UNSPECIFIED" ? false : true
      }

      node_config {
        image_type   = "WINDOWS_LTSC_CONTAINERD"
        machine_type = local.windowsMachineType

        oauth_scopes = [
          "https://www.googleapis.com/auth/devstorage.read_only",
          "https://www.googleapis.com/auth/logging.write",
          "https://www.googleapis.com/auth/monitoring",
          "https://www.googleapis.com/auth/service.management.readonly",
          "https://www.googleapis.com/auth/servicecontrol",
          "https://www.googleapis.com/auth/trace.append",
        ]

        tags = ["game-server"]
      }
    }
  }
  dynamic "workload_identity_config" {
    for_each = local.workloadIdentity? [1] : []
    content {
      workload_pool = "${local.project}.svc.id.goog"
    }
  }
  timeouts {
    create = "30m"
    update = "40m"
  }
}

resource "google_compute_firewall" "default" {
  count   = var.udpFirewall ? 1 : 0
  name    = length(var.firewallName) == 0 ? "game-server-firewall-${local.name}" : var.firewallName
  project = local.project
  network = local.network

  allow {
    protocol = "udp"
    ports    = [var.ports]
  }

  target_tags   = ["game-server"]
  source_ranges = [var.sourceRanges]
}
