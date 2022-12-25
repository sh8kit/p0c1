terraform {
  backend "s3" {
    bucket = "tf-states"
    key = "local.tfstate"

    endpoint = "http://minio:9000"

    access_key="minio"
    secret_key="minio123"

    region = "main"
    skip_credentials_validation = true
    skip_metadata_api_check = true
    skip_region_validation = true
    force_path_style = true
  }
}

module "datashack_local" {
  presto_host            = var.presto_host
  kafka_connect_host     = var.kafka_connect_host
  minio_host             = var.minio_host
  kafka_bootstarp_server = var.kafka_bootstarp_server
  source                 = "../../modules/datashack"
}