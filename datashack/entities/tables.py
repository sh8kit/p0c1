import copy
from datetime import timezone, datetime
from abc import ABC, abstractmethod
from typing import Type, Dict, Any
from collections.abc import MutableMapping
from confluent_kafka.avro import AvroProducer
from datashack.entities.utils import AvroConverter


class StateElement(ABC):

    def __init__(self, name):
        self.state_elemt_name = name

    @abstractmethod
    def generate_state(self) -> object:
        raise NotImplemented


class Table(StateElement, MutableMapping):
    def __init__(self, database: str, table_name: str):
        self._sent_messages = 0
        self._schema = dict()
        self._database = database
        self._table_name = table_name
        self._avroProducer = AvroProducer(
            {'bootstrap.servers': 'localhost:9092', 'schema.registry.url': 'http://0.0.0.0:8081'})

        super(Table, self).__init__(f'table_{self._database}.{self._table_name}')

    def __getitem__(self, key):
        return self._schema[key]

    def __hash__(self):
        cols_list = tuple([(c, str(self.columns[c].col_type)) for c in self.columns])
        object_desc = (self.table_name, cols_list)
        return hash(object_desc)

    def __setitem__(self, key: str, value: 'Column'):
        # create a copy of
        value = copy.deepcopy(value)

        if not value.is_assigned_to_table():
            # bind only if not assigned
            value.set_table(self)  # bind this column

        # set the column name
        value.set_col_name(key)

        self._schema[key] = value

    def __delitem__(self, key):
        del self._schema[key]

    def __iter__(self):
        return iter(self._schema)

    def __len__(self):
        return len(self._schema)

    @property
    def table_name(self):
        return self._table_name

    def __str__(self):
        return f'{self._database}.{self._table_name}'

    # def write_data_to_topic(self, topic_name, data):
    #     """
    #     :param topic_name: topic to write the data into
    #     :param data: the data to be written to the topic in topic_name
    #     """
    #     conf = {'bootstrap.servers': "localhost:9093"}
    #     json_data = json.dumps(json.loads(data)).encode()
    #     producer = Producer(conf)
    #     producer.produce(topic_name, json_data)
    #     return "success"

    # def validate_Schema(self):
    #     pass
    @property
    def columns(self):
        return {c[0]: c[1] for c in self.items()}

    def parse_data(self, data):
        parsed_data = copy.deepcopy(data)
        for key, value in data.items():
            if self.columns[key].col_type == datetime:
                parsed_data[key] = parsed_data[key].replace(tzinfo=timezone.utc).timestamp()
        return parsed_data

    def insert(self, data: Dict[str, Any]):
        avro_schema = AvroConverter.get_avro_schema(self)
        # parsed_data = self.parse_data(data)
        self._avroProducer.produce(topic=self.table_name, value=data, value_schema=avro_schema)
        self._sent_messages += 1
        if self._sent_messages == 100:
            self._avroProducer.flush()
            self._sent_messages = 0

    def generate_ddl(self) -> str:
        create_statement = f'''CREATE TABLE IF NOT EXISTS {self}'''
        cols = []
        for col_name, col in self.items():
            cols.append(f'`{col_name}` {str(col.col_type.__name__)}')
        cols_statement = f'({",".join(cols)})'
        # partition_by_statement = f"""PARTITION BY ({",".join(["`{p}`".format(p=p) for p in self.partitions])})""" if self.partitions else ""
        ddl = " ".join([create_statement, cols_statement]) + ";"
        return ddl

    def generate_state(self):
        """
        table_name: "user_events"
        database: "dwh"
        columns:
        - name: "id"
            type: "string"
        - name: "name"
            type: "string"
        - name: "email"
            type: "string"
        - name: "age_now"
            type: "int"
        - name: "event_type"
            type: "string"
        - name: "event_ts"
            type: "timestamp"
        ts_partitioner: "event_ts"
        """
        return dict(
            table_name=self._table_name,
            database=self._database,
            columns=[
                {"name": _col.col_name, "type": _col.col_type.__name__} for _col in self.values()
            ],
            ts_partitioner="ingestion_date"
        )


class Column:

    def __init__(self, col_type: Type):
        self._col_type = col_type
        self._col_name = None
        self._table = None

    def __add__(self, x):
        # tbd
        pass

    def __sub__(self, x):
        # tbd
        pass

    def __mul__(self, x):
        # tbd
        pass

    def __truediv__(self, x):
        # tbd
        pass

    def __eq__(self, x):
        return ConditionEq(self, x)

    def __str__(self):
        return str(self.table) + '.' + self.col_name

    def is_assigned_to_table(self) -> bool:
        return bool(self._table)

    def set_table(self, table: Table):
        self._table = table

    def set_col_name(self, col_name: str):
        self._col_name = col_name

    @property
    def col_type(self):
        return self._col_type

    @property
    def col_name(self):
        return self._col_name

    @property
    def table(self):
        return self._table


class Condition:
    pass


class ConditionEq(Condition):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __str__(self):
        return f'{self._a}={self._b}'


class JoinedTable(Table, MutableMapping):
    def __init__(self, database: str, table_name: str, source_tables: [Table], condition: Condition):
        Table.__init__(self, database, table_name)
        self._source_tables = source_tables
        self._condition = condition

    def generate_evolve(self):
        return f'''INSERT OVERWRITE {self}
SELECT {', '.join(str(c) for c in self.values())}
FROM {', '.join(str(t) for t in self._source_tables)}
WHERE {str(self._condition)}
'''
