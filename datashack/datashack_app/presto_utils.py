import os
import pandas as pd
import sqlalchemy as sa
from functools import lru_cache
from typing import Tuple
from pandas import DataFrame
from sqlalchemy import Table, MetaData, select
from sqlalchemy.engine import create_engine


@lru_cache
def get_presto_engine(catalog, schema="default"):
    presto_host = os.environ.get("presto_host", "localhost")
    return create_engine(f'presto://{presto_host}:8080/{catalog}/{schema}')


def execute_query(query):
    engine = get_presto_engine(catalog="minio")
    connection = engine.connect()
    connection.execute(query)
    connection.close()


def create_db_if_not_exists(db):  # TODO consolidate with function in hive_tables.py
    engine = get_presto_engine(catalog="minio")
    existing_databases = sa.inspect(engine).get_schema_names()
    if db not in existing_databases:
        connection = engine.connect()
        connection.execute(f"create SCHEMA {db}")
        connection.close()


def get_tables_from_db(schema="default") -> Tuple:
    engine = get_presto_engine(catalog="minio", schema=schema)
    dbs = [db for db in sa.inspect(engine).get_schema_names() if db != 'information_schema']
    return tuple(f"{db}.{table}" for db in dbs for table in engine.table_names(db))


def refresh_partitions(db,table):
    q = f"""CALL system.sync_partition_metadata('{db}', '{table}', 'FULL')"""
    execute_query(q)

def get_table_sample(db_table: str, limit=20) -> DataFrame:
    # Presto
    db, table_name = db_table.split(".")
    refresh_partitions(db, table_name)
    engine = get_presto_engine(catalog="minio", schema=db)
    connection = engine.connect()
    table = Table(table_name, MetaData(bind=engine), autoload=True)

    columns = [c[0] for c in table.columns.items()]
    stmt = select(table).limit(limit)
    data = connection.execute(stmt).fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df
