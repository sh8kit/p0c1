variable "presto_host" {
  default = "localhost"
  type    = string
}

variable "kafka_connect_host" {
  default = "localhost"
  type    = string
}

variable "minio_host" {
  default = "localhost"
  type    = string
}

variable "kafka_bootstarp_server" {
  default = "localhost:9092"
  type    = string
}

variable "schema_registry_internal_url" {
  default = "http://registry:8081"
  type    = string
}
variable "minio_internal_url" {
  default = "http://minio:9000"
  type    = string
}