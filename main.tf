provider "google" {
  project = var.project_id
  region = var.region
}

resource "google_kubernetes_engine_cluster" "default" {
  name = "my-cluster"
  location = var.region
  node_count = 3

  node_config {
    machine_type = "n1-standard-2"
  }
}

resource "google_kubernetes_engine_deployment" "trading-bot" {
  metadata {
    name = "trading-bot"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "trading-bot"
      }
    }

    template {
      metadata {
        labels = {
          app = "trading-bot"
        }
      }

      spec {
        containers {
          name = "trading-bot"
          image = "my-container-registry/trading-bot:latest"
        }
      }
    }
  }
}