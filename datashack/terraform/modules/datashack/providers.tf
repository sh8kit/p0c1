terraform {
  required_providers {
    kafka-connect = {
      source  = "Mongey/kafka-connect"
      version = "0.3.0"
    }
    minio = {
      source = "aminueza/minio"
      version = "1.10.0"
    }

  }
}


provider "kafka-connect" {
  url = "http://${var.kafka_connect_host}:28082"
}

provider minio {
  minio_server   = "${var.minio_host}:9000"
  minio_user     = "minio"
  minio_password = "minio123"
}

