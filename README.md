# Welcome to Datashack POC 👋

Thank you for participating in our POC ❤

## Pre-requisites
- Zip
- installed x-code(mac)
- Docker with 7gm ram at least
- Docker-compose
- python 3.8+ with pip
- IDE
- git

## Getting Started

### Step 1
Run in your Terminal

```#bash
git clone https://github.com/sh8kit/p0c1.git
cd p0c1

# install datashack cli
pip install . --upgrade

# provision docker-compose environment
cd local_docker && make up
```

### Step 2
Write your model in "my_app/models" in python
```python
from datetime import datetime
from datashack.entities.tables import Table, Column

Users = Table(database='logs', table_name='user_events')
Users['id'] = Column(str)
Users['name'] = Column(str)
Users['email'] = Column(str)
Users['event_type'] = Column(str)
Users['event_ts'] = Column(datetime)
```

### Step3 
run `datashack apply my_app/models local_docker/yamls` in your terminal

## Step 4
visit http://localhost:8501 to see the datalake

## Step 5
now, you can send events to the tables from a python script.
open `my_app/generate.py`
you can keep it as is or edit and run it with
`python my_app/generate.py`

