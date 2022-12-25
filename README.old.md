# datashack

### build

1. first of all build datashack server image

```commandline
cd datashack
docker build . -t datashack_app
```

2. run docker-compose to raise all the required environment

```commandline 
cd ../datashack_docker
docker-compose up -d
```

### debug
#### terraform
for running plan locally
```commandline
terraform plan --var presto_host=localhost --var kafka_connect_host=localhost --var minio_host=localhost --var kafka_bootstarp_server=localhost:9092
```
for running from server
```commandline
terraform plan --var presto_host=presto --var kafka_connect_host=kafka-connect --var minio_host=minio --var kafka_bootstarp_server=kafka:29092

```