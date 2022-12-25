import json
from dataclasses import dataclass
from datetime import datetime

from confluent_kafka import avro
from dataclasses_avroschema import AvroModel, DateTimeMicro


# @dataclass
# class DatetimeLogicalType(AvroModel):
#     "Datetime logical types"
#     birthday: datetime.datetime
#     meeting_time: typing.Optional[datetime.datetime] = None
#     release_datetime: datetime.datetime = a_datetime
#     release_datetime_micro: DateTimeMicro = a_datetime


class AvroConverter:
    MAPPER = {
        str: "string",
        'str': "string",
        int: "int",
        datetime:  {"type": "long", "logicalType": "timestamp-millis"}
    }

    def __init__(self, namespace, record_name):
        self._record_schema = {
            "type": "record",
            "namespace": namespace,
            "name": record_name,
            "fields": []
        }

    def add_column(self, col_name, col_type):
        typed_col = {"name": col_name, "type": self.MAPPER[col_type]}
        self._record_schema["fields"].append(typed_col)

    @property
    def record_schema(self):
        return self._record_schema

    @classmethod
    def get_avro_schema(cls, table):
        avro_schema = cls(table._table_name, table._table_name)
        for col_name, col in table.items():
            avro_schema.add_column(col_name, col.col_type)
        return avro.loads(json.dumps(avro_schema.record_schema))
