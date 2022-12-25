import argparse
import os
import sqlalchemy as sa
from functools import lru_cache
from requests.exceptions import ConnectionError as CE
from pyhive.exc import DatabaseError
from retrying import retry
from sqlalchemy import create_engine


def retry_if_starting_up_error(e):
    try:
        e = e.orig
    except Exception:
        pass
    if isinstance(e, DatabaseError):
        if e.args[0]['errorCode'] == 65548:
            print(e.args[0]['errorName'])
            return True
        else:
            return False
    elif isinstance(e, CE):
        print("Connection aborted stills setting up presto")
        return True
    else:
        return False


@lru_cache
def get_presto_engine(catalog, schema="default", host='localhost'):
    return create_engine(f'presto://{host}:8080/{catalog}/{schema}')


@retry(retry_on_exception=retry_if_starting_up_error, wrap_exception=True, wait_fixed=10000, stop_max_attempt_number=6)
def create_db_if_not_exists(db):
    engine = get_presto_engine(host=presto_host, catalog="minio")
    existing_databases = sa.inspect(engine).get_schema_names()
    if db not in existing_databases:
        connection = engine.connect()
        connection.execute(f"CREATE SCHEMA IF NOT EXISTS {db}")
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dbs')
    args = parser.parse_args()
    presto_host = os.getenv("presto_host", "localhost")

    databases_list = args.dbs.split(",")
    for db in databases_list:
        create_db_if_not_exists(db)


