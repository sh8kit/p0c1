from dataclasses import dataclass
from typing import Dict


@dataclass
class KafkaConnector:
    path_in_bucket: str
    bucket: str = "data"
    partitioned_by: str = "ingestion_date"
    file_format: str = "parquet"
    compression: str = "snappy"

    @classmethod
    def is_connector(cls, st):
        return ".kafka-connect_connector" in st

    @classmethod
    def get_connector_markdown(cls, table_name):
        return f"""[consumer {table_name}](http://localhost:7070/ui/clusters/local/consumer-groups/connect-s3-sink-{table_name})"""


@dataclass()
class KafkaTopic:
    topic_name: str
    num_partitions: int = 1
    replication_factor: int = 1

    @classmethod
    def is_kafka_topic(cls, st):
        return ".create_kafka_topic" in st

    @classmethod
    def get_kafka_topic_markdown(cls, table_name):
        return f"""[kafka topic {table_name}](http://localhost:7070/ui/clusters/local/topics/{table_name})"""


@dataclass
class PrestoTable:
    table_name: str
    db_name: str

    @classmethod
    def is_presto_table(cls, state):
        return ".create_presto_table" in state

    @classmethod
    def get_presto_table_markdown(cls, db_name, table_name):
        conn_config = cls(table_name=table_name, db_name=db_name)
        return """
            **presto table**

            config:
            1. table_name : {}
            2. db_name : {}

            """.format(conn_config.table_name,
                       conn_config.db_name)

    @classmethod
    def get_minio_data_location(cls, db_name, table_name):
        return f"""[path {db_name} {table_name}](http://localhost:9000/minio/data/datashack/{db_name}/{table_name}/)"""
