resource "minio_s3_bucket" "data_bucket" {
  bucket = "data"
  acl    = "public"
}

resource "null_resource" "create_presto_schemas" {
  depends_on = [minio_s3_bucket.data_bucket]
  triggers = {
    dbs = local.presto_dbs
  }
  provisioner "local-exec" {
    command = "python3 ${path.module}/${local.scripts_prefix}/presto_schema.py ${local.presto_dbs}"

  }

}

resource "null_resource" "create_presto_table" {
  depends_on = [null_resource.create_presto_schemas]
  for_each = local.yamls_list
  triggers = {
    topic_config = filemd5("${local.yamls_loc}/${each.key}")
  }
  provisioner "local-exec" {
    command = "python3 ${path.module}/${local.scripts_prefix}/hive_tables.py ${local.yamls_loc}/${each.key} ${minio_s3_bucket.data_bucket.bucket}/${local.datashack_base_dir}"

  }

}


resource "null_resource" "create_kafka_topic" {
  depends_on = [null_resource.create_presto_table]
  for_each = local.tables_configs
  triggers = {
    topic_config = md5(each.key)
  }
  provisioner "local-exec" {
#    command = "kafka-topics --topic  ${split(".",each.key)[1]} --create --bootstrap-server ${var.kafka_bootstarp_server}"
    command = "python3 ${path.module}/${local.scripts_prefix}/kafka_scripts.py ${split(".",each.key)[1]} ${var.kafka_bootstarp_server}"

  }

}

resource "kafka-connect_connector" "datashack_connect" {
  depends_on = [null_resource.create_kafka_topic]
  for_each = local.tables_configs
  name     = "s3-sink-${each.value["table_name"]}"

  config = {
    "name"                  = "s3-sink-${each.value["table_name"]}"
    "s3.bucket.name"        = minio_s3_bucket.data_bucket.bucket
    "store.url"             = var.minio_internal_url
    "connector.class"       = "io.confluent.connect.s3.S3SinkConnector"
    "tasks.max"             = local.connector_default.tasks_max
    "topics"                = each.value["table_name"]
    "s3.region"             = local.connector_default.s3_region
    "storage.class"         = "io.confluent.connect.s3.storage.S3Storage"
    "format.class"          = "io.confluent.connect.s3.format.parquet.ParquetFormat"
    "parquet.codec"         = "snappy"
    "topics.dir"            = "${local.datashack_base_dir}/${each.value["database"]}"
    "partitioner.class"     = "io.confluent.connect.storage.partitioner.TimeBasedPartitioner"
    "path.format"           = "'ingestion_date'=YYYY-MM-dd"
    "partition.duration.ms" = 1000
    "locale"                = "en-US"
    "timezone"              = "UTC"
    "timestamp.extractor"   = "Wallclock"
    "schema.compatibility"  = "BACKWARD"
    "flush.size"            = 100

    "key.converter"                       = "io.confluent.connect.avro.AvroConverter"
    "key.converter.schema.registry.url"   = var.schema_registry_internal_url
    "value.converter"                     = "io.confluent.connect.avro.AvroConverter"
    "value.converter.schema.registry.url" = var.schema_registry_internal_url
    "value.converter.schemas.enable" = "false"


  }
}




locals {
  datashack_base_dir = "datashack"
  yamls_loc = "${path.module}/yamls"
  yamls_list     = fileset(local.yamls_loc, "*.yaml")
  tables_configs = { for y in local.yamls_list : y => yamldecode(file("${path.module}/yamls/${y}")) }
  connector_default = {
    tasks_max = 1
    s3_region = "us-east-1"
  }
  scripts_prefix = "scripts"
  presto_dbs = join(",",toset([for t in local.yamls_list : yamldecode(file("${path.module}/yamls/${t}"))["database"]]))



}








