import importlib
import pkgutil
from augmentd.tables import DSTable

for (module_loader, name, ispkg) in pkgutil.iter_modules(["my_app/new_models"]):
    models = importlib.import_module("my_app.new_models." + name)

ds_tables = dict([(name, cls) for name, cls in models.__dict__.items() if isinstance(cls, DSTable)])

for table in ds_tables:
    ds_tables[table].generate_ddl() #TODO create kafka producer