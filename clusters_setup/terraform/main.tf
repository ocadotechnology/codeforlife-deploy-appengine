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
      version = "4.62.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "1.10.0"
    }
  }
}

provider "helm" {
  kubernetes {
    host                   = module.gke_cluster.host
    token                  = module.gke_cluster.token
    cluster_ca_certificate = module.gke_cluster.cluster_ca_certificate
    config_path            = "~/.kube/config"
  }
}

provider "kubectl" {
  host                   = module.gke_cluster.host
  token                  = module.gke_cluster.token
  cluster_ca_certificate = module.gke_cluster.cluster_ca_certificate
  config_path            = "~/.kube/config"
}

module "gke_cluster" {
  source = "./modules/gke"

  cluster = {
    "name"              = local.cluster_name
    "zone"              = var.zone
    "machineType"       = var.machine_type
    "initialNodeCount"  = var.node_count
    "project"           = var.project
    "network"           = var.network
    "subnetwork"        = var.subnetwork
    "kubernetesVersion" = var.kubernetesVersion
  }
}

resource "helm_release" "agones" {
  // Inspired from https://github.com/googleforgames/agones/blob/main/install/terraform/modules/helm3/helm.tf
  name             = "agones"
  repository       = "https://agones.dev/chart/stable"
  force_update     = var.force_update
  chart            = var.chart
  timeout          = 420
  version          = local.agones_version
  namespace        = "agones-system"
  create_namespace = true

  # Use terraform of the latest >=0.12 version
  values = [
    length(var.values_file) == 0 ? "" : file(var.values_file),
  ]

  set {
    name  = "agones.metrics.stackdriverEnabled"
    value = "true"
  }

  set {
    name  = "agones.metrics.prometheusEnabled"
    value = "false"
  }

  set {
    name  = "agones.metrics.prometheusServiceDiscovery"
    value = "false"
  }

  set {
    name  = "crds.CleanupOnDelete"
    value = var.crd_cleanup
  }

  set {
    name  = "agones.image.registry"
    value = var.image_registry
  }

  set {
    name  = "agones.image.controller.pullPolicy"
    value = var.pull_policy
  }

  set {
    name  = "agones.image.sdk.alwaysPull"
    value = var.always_pull_sidecar
  }

  set {
    name  = "agones.image.controller.pullSecret"
    value = var.image_pull_secret
  }

  set {
    name  = "agones.ping.http.serviceType"
    value = var.ping_service_type
  }

  set {
    name  = "agones.ping.udp.expose"
    value = var.udp_expose
  }

  set {
    name  = "agones.ping.udp.serviceType"
    value = var.ping_service_type
  }

  set {
    name  = "agones.controller.logLevel"
    value = var.log_level
  }

  set {
    name  = "agones.featureGates"
    value = var.feature_gates
  }

  set {
    name  = "gameservers.namespaces"
    value = "{${join(",", var.gameserver_namespaces)}}"
  }

  set {
    name  = "gameservers.minPort"
    value = var.gameserver_minPort
  }

  set {
    name  = "gameservers.maxPort"
    value = var.gameserver_maxPort
  }
}

data "google_compute_address" "load_balancer_ip" {
  name    = "${terraform.workspace}-aimmo-ingress"
  project = var.project
  region  = var.region
}

resource "helm_release" "nginx_ingress" {
  name = "ingress-nginx"

  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"

  set {
    name  = "controller.service.loadBalancerIP"
    value = data.google_compute_address.load_balancer_ip.address
  }
}

data "kubectl_path_documents" "cluster_roles" {
  pattern = "${path.module}/cluster_roles/*.yaml"
}

resource "kubectl_manifest" "roles" {
  count     = length(data.kubectl_path_documents.cluster_roles.documents)
  yaml_body = element(data.kubectl_path_documents.cluster_roles.documents, count.index)
}
