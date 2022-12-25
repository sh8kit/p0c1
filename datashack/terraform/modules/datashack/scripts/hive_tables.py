import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from time import sleep
from typing import List, Dict

from pyhive.exc import DatabaseError
from sqlalchemy import create_engine
import yaml
import argparse
from pyhive import presto
import sqlalchemy as sa


@lru_cache
def get_presto_engine(catalog, schema="default", host='localhost'):
    return create_engine(f'presto://{host}:8080/{catalog}/{schema}')


@dataclass
class TableDefinition:
    table_name: str
    database: str
    columns: List[Dict[str, str]]
    ts_partitioner: str
    type_mapper = {"string": "varchar",
                   "str": "varchar",
                   "long": "bigint",
                   "datetime": "timestamp"}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('file_path')
    parser.add_argument("bucket_path")
    args = parser.parse_args()
    presto_host = os.getenv("presto_host", "localhost")

    with open(args.file_path) as f:
        table_definition = TableDefinition(**yaml.safe_load(f))

    create_ddl = f"CREATE TABLE IF NOT EXISTS {table_definition.database}.{table_definition.table_name} "

    columns_with_partition = table_definition.columns + [{'name': 'ingestion_date', 'type': 'string'}]

    columns_ddl = f""" ({','.join([f"{col['name']} {TableDefinition.type_mapper.get(col['type'], col['type'])}" for col in columns_with_partition])}) """
    using_format = f" WITH (partitioned_by = ARRAY['{table_definition.ts_partitioner}'],format = 'PARQUET', external_location = 's3a://{args.bucket_path}/{table_definition.database}/{table_definition.table_name}')"

    complete_ddl = create_ddl + columns_ddl + using_format
    cursor = presto.connect(host=presto_host, catalog="minio", schema=table_definition.database).cursor()
    cursor.execute(complete_ddl)
    running_q = True
    while running_q:
        sleep(2)
        try:
            res = cursor.poll()
            status = res['stats']['state']
        except DatabaseError as e:
            print(e.args[0]['errorName'])
            status = "FAILED"

        if status == 'QUEUED':
            continue
        elif status == 'FINISHED':
            running_q = False
        elif status == "FAILED":
            sys.exit(1)
    sys.exit(0)
