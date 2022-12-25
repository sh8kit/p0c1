from datashack.entities.tables import Table, Column

Products = Table(database='logs', table_name='products')
Products['id'] = Column(str)
Products['name'] = Column(str)
Products['code'] = Column(str)
