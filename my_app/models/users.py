from datetime import datetime
from datashack.entities.tables import Table, Column

Users = Table(database='logs', table_name='user_events')
Users['id'] = Column(str)
Users['name'] = Column(str)
Users['email'] = Column(str)
Users['event_type'] = Column(str)
Users['event_ts'] = Column(datetime)

RegisteredUsers = Table(database='ab', table_name='registered_users')
RegisteredUsers['id'] = Column(str)
RegisteredUsers['name'] = Column(str)
RegisteredUsers['email'] = Column(str)
RegisteredUsers['event_type'] = Column(str)
RegisteredUsers['event_ts'] = Column(datetime)